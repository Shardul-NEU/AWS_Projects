import boto3
from botocore.exceptions import BotoCoreError, ClientError
import os

DYNAMODB_TABLE_NAME_FAILED_ARNS = 'FailedResourceARNs'
DYNAMODB_TABLE_NAME_SUCCESS_ARNS = 'SuccessfulGlobalARN'
dynamodb_resource = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')
tag_key = os.environ.get('TAG_KEY')
tag_value = os.environ.get('TAG_VALUE')
query_string = f'-tag:{tag_key}={tag_value} -service:ssm'
regions = ['us-east-1', 'global', 'us-west-1', 'eu-west-1', 'us-west-2', 'us-east-2', 'af-south-1', 'ap-east-1', 'ap-south-1', 'ap-northeast-3', 'ap-northeast-2', 'ap-southeast-2', 'ap-southeast-1', 'ap-northeast-1', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-south-1', 'eu-west-3', 'eu-north-1', 'me-south-1', 'sa-east-1']

MAX_BATCH_SIZE = 10000

def create_dynamodb_table(table_name):
    """Create the DynamoDB table if it doesn't exist."""
    try:
        dynamodb_client.create_table(
            TableName=table_name,
            AttributeDefinitions=[{'AttributeName': 'Arn', 'AttributeType': 'S'}],
            KeySchema=[{'AttributeName': 'Arn', 'KeyType': 'HASH'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        print(f"Table {table_name} is being created...")
        dynamodb_resource.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        print(f"Table {table_name} created successfully.")
    except ClientError as e:
        if e.response['Error']['Code'] != 'ResourceInUseException':
            raise

def check_or_create_table():
    """Check if the DynamoDB table exists, and create it if it doesn't."""
    for table_name in [DYNAMODB_TABLE_NAME_FAILED_ARNS, DYNAMODB_TABLE_NAME_SUCCESS_ARNS]:

        try:
            dynamodb_client.describe_table(TableName=table_name)
            print(f"Table {table_name} already exists.")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                create_dynamodb_table(table_name)
            else:
                raise

def log_failed_arn(arn, reason, region):
    """Log failed ARN with reason to DynamoDB."""
    table = dynamodb_resource.Table(DYNAMODB_TABLE_NAME_FAILED_ARNS)
    table.put_item(Item={'Arn': arn, 'Reason': reason, 'Region': region})

def log_successful_global_arns(arn, region):
    table = dynamodb_resource.Table(DYNAMODB_TABLE_NAME_SUCCESS_ARNS)
    table.put_item(Item={'Arn': arn, 'Region': region})

def should_skip_arn(arn, region):
    """Check if an ARN should be skipped based on past failures."""
    failed_arn_table = dynamodb_resource.Table(DYNAMODB_TABLE_NAME_FAILED_ARNS)
    response_failed = failed_arn_table.get_item(Key={'Arn': arn})
    if 'Item' in response_failed:
        return True
    if region == 'global':
        successful_arn_table = dynamodb_resource.Table(DYNAMODB_TABLE_NAME_SUCCESS_ARNS)
        response_successful = successful_arn_table.get_item(Key={'Arn': arn})
        return 'Item' in response_successful
    return False

def search_and_tag_resources(regions):
    for region in regions:
        print(f"Processing region: {region}")
        client = boto3.client('resource-explorer-2')

        tagged_resources = set()
        

        while True:
            resources = []
            next_token = None
            skipped_due_to_failure = 0 
            while True:
                response = client.search(
                    QueryString=f'region:{region} {query_string}',
                    MaxResults=1000
                )
                resources.extend(response['Resources'])
                next_token = response.get('NextToken')

                if not next_token:
                    break

            arns = [resource['Arn'] for resource in resources if resource['Arn'] not in tagged_resources]
            arns_to_tag = []
            for arn in arns:
                if not should_skip_arn(arn,region):
                    arns_to_tag.append(arn)
                else:
                    skipped_due_to_failure += 1

            result = tag_resources(arns_to_tag, region)
            successful = result['successful']
            failed = result['failed']

            tagged_resources.update(successful)

            print(f"Successfully tagged {len(successful)} resources in {region}.")
            print(f"Failed to tag {len(failed)} resources in {region}, details logged to DynamoDB.")
            print(f"Skipped {skipped_due_to_failure} resources based on previous failures.")

            if not arns_to_tag:
                print("No taggable resources found or all remaining resources were previously skipped.")
                break

            print(f"Total resources found in {region}: {len(resources)}")
            print(f"Total Resources to tag in {region}: {len(arns_to_tag)}")


def arn_list_chunk(input_list, chunk_size):
    """Yield successive chunk_size chunks from input_list."""
    for i in range(0, len(input_list), chunk_size):
        yield input_list[i:i + chunk_size]

import time

def tag_resources(arns, region, max_retries=3):
    if region == 'global':
        region_to_consider = 'us-east-1'
    else: region_to_consider = region 
    client = boto3.client('resourcegroupstaggingapi', region_name=region_to_consider)
    chunk_size = 20
    successfully_tagged_arns = []
    failed_to_tag_arns = []

    for arn_chunk in arn_list_chunk(arns, chunk_size):
        retries = 0
        while retries <= max_retries:
            try:
                response = client.tag_resources(
                    ResourceARNList=arn_chunk,
                    Tags={tag_key: tag_value}
                )

                failed_arns = response.get('FailedResourcesMap', {})
                for arn in arn_chunk:
                    if arn not in failed_arns:
                        successfully_tagged_arns.append(arn)
                        if region == 'global':
                            log_successful_global_arns(arn, region)
                    else:
                        error_message = failed_arns[arn].get('ErrorMessage', '')
                        if 'Rate exceeded' not in error_message or retries == max_retries:
                            log_failed_arn(arn, error_message, region)
                            failed_to_tag_arns.append(arn)
                            print(f"Failed to tag {arn}: {error_message}")

                break  # Exit the retry loop on successful response
            except ClientError as e:
                if e.response['Error']['Code'] == 'ThrottlingException' and retries < max_retries:
                    wait_time = 2 ** retries  # Exponential backoff
                    print(f"Rate exceeded, retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    retries += 1
                else:
                    print(f"Failed to tag resources in chunk due to {e}, not retrying.")
                    for arn in arn_chunk:
                        failed_to_tag_arns.append(arn)
                    break

    return {
        'successful': successfully_tagged_arns,
        'failed': failed_to_tag_arns
    }

def main():
        check_or_create_table()
    # List of regions to search and tag resources in
        search_and_tag_resources(regions)
    

if __name__ == '__main__':
    main()
