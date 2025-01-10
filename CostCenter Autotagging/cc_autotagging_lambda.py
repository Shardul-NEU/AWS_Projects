import boto3
import os
import logging
from botocore.exceptions import BotoCoreError, ClientError

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def search_resources_with_tag(region, tag_key, tag_value):
    client = boto3.client('resource-explorer-2', region_name='us-east-1')
    
    query_string = f'-tag:{tag_key}={tag_value} -service:ssm'
    
    paginator = client.get_paginator('search')
    response_iterator = paginator.paginate(
        QueryString=f'region:{region} {query_string}',
        PaginationConfig={
            'PageSize': 50
        }
    )

    resources = []
    for page in response_iterator:
        for resource in page['Resources']:
            resources.append(resource['Arn'])
    total_count = len(resources)
    logger.info(f"Total Resources in {region} : {total_count}")
    return resources

def tag_resources(region, resource_arns, tag_key, tag_value):
    if region == 'global':
        region = 'us-east-1'
    
    client = boto3.client('resourcegroupstaggingapi', region_name=region)
    
    success_count = 0
    error_count = 0
    
    for arn in resource_arns:
        try:
            client.tag_resources(
                ResourceARNList=[arn],
                Tags={tag_key: tag_value}
            )
            success_count += 1
        except ClientError as e:
            error_count += 1
            logger.error(f"Error tagging resource {arn} in region {region}: {str(e)}")
    
    return success_count, error_count

def lambda_handler(event, context):
    # Fetch tag key and value from environment variables
    tag_key = os.getenv('TAG_KEY', 'CostCenter')
    tag_value = os.getenv('TAG_VALUE')
    regions = os.getenv('REGIONS', 'us-east-1,global').split(',')

    total_resources_found = 0
    total_successfully_tagged = 0
    total_errors = 0

    for region in regions:
        logger.info(f"Processing region: {region}")

        # Search for resources with the given tag key and value
        resources = search_resources_with_tag(region, tag_key, tag_value)
        resource_count = len(resources)
        total_resources_found += resource_count

        if resources:
            # Tag resources if found
            success_count, error_count = tag_resources(region, resources, tag_key, tag_value)
            total_successfully_tagged += success_count
            total_errors += error_count
        else:
            logger.info(f"No resources found without the specified tag in region {region}.")
    
    # Return the counts of all resources found, successfully tagged, and errors
    return {
        'TotalResourcesFound': total_resources_found,
        'TotalSuccessfullyTagged': total_successfully_tagged,
        'TotalErrors': total_errors
    }
