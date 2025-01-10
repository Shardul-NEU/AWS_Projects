import json
import boto3
from botocore.exceptions import ClientError

# Initialize AWS clients
iam_client = boto3.client('iam')
codepipeline_client = boto3.client('codepipeline')
sns_client = boto3.client('sns')
s3_client = boto3.client('s3')

# Configuration variables
admin_policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
sns_topic_arn = "arn:aws:sns:us-east-1:905418079887:CI-CD-test-Notifications"  # Corrected SNS topic ARN
bucket_name = 'ci-cd-test-output'
prefix = 'project/'

def get_latest_tfplan_link(bucket, prefix=''):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        print("S3 list_objects_v2 response:", response)
        objects = sorted(response.get('Contents', []), key=lambda obj: obj['LastModified'], reverse=True)
        if objects:
            latest_object_key = objects[0]['Key']
            s3_console_link = f"https://s3.console.aws.amazon.com/s3/object/{bucket_name}?prefix={latest_object_key}"
            presigned_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': latest_object_key}, ExpiresIn=172800)
            print(f"Generated presigned URL: {presigned_url}")
            return presigned_url
        else:
            print("No objects found in S3 bucket with the specified prefix.")
            return None
    except ClientError as e:
        print(f"Error fetching the latest tfplan file from S3: {e}")
        return None

def get_latest_tfplan_console_link(bucket, prefix=''):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        print("S3 list_objects_v2 response:", response)
        objects = sorted(response.get('Contents', []), key=lambda obj: obj['LastModified'], reverse=True)
        if objects:
            latest_object_key = objects[0]['Key']
            s3_console_link = f"https://s3.console.aws.amazon.com/s3/object/{bucket_name}?prefix={latest_object_key}"
            return s3_console_link
        else:
            print("No objects found in S3 bucket with the specified prefix.")
            return None
    except ClientError as e:
        print(f"Error fetching the latest tfplan file from S3: {e}")
        return None

def grant_admin_access(role_name):
    print(f"Attempting to attach AdministratorAccess policy to role: {role_name}")
    iam_client.attach_role_policy(RoleName=role_name, PolicyArn=admin_policy_arn)
    print("AdministratorAccess policy attached successfully.")
    return "AdministratorAccess policy attached"

def revoke_admin_access(role_name):
    print(f"Attempting to detach AdministratorAccess policy from role: {role_name}")
    iam_client.detach_role_policy(RoleName=role_name, PolicyArn=admin_policy_arn)
    print("AdministratorAccess policy detached successfully.")
    return "AdministratorAccess policy detached"

def send_approval_notification(s3_plan_link, s3_console_link):
    console_link = "https://console.aws.amazon.com/codesuite/codepipeline/pipelines/CI-CD-Pipeline-test/view?region=us-east-1"
    message = f"Approval Required: Please review the Terraform plan before applying.\nTerraform Plan: {s3_plan_link}\n Terraform Plan Console Link {s3_console_link}\n Approve or Reject Pipeline: {console_link} "
    try:
        response = sns_client.publish(TopicArn=sns_topic_arn, Message=message)
        print("SNS publish response:", response)
    except ClientError as e:
        print(f"Failed to send SNS notification. Error: {e}")

def signal_codepipeline_success(job_id):
    codepipeline_client.put_job_success_result(jobId=job_id)
    print("Signaled success to CodePipeline.")

def signal_codepipeline_failure(job_id, message):
    codepipeline_client.put_job_failure_result(jobId=job_id, failureDetails={'message': message, 'type': 'JobFailed'})
    print("Signaled failure to CodePipeline.")

def lambda_handler(event, context):
    print("Received event:", json.dumps(event, indent=2))
    role_name = None
    
    try:
        job_id = event["CodePipeline.job"]["id"]
        user_params_str = event["CodePipeline.job"]["data"]["actionConfiguration"]["configuration"]["UserParameters"]
        user_params = json.loads(user_params_str)

        role_name = user_params.get('role_name')
        pipeline_stage = user_params.get('pipeline_stage')
        
        print(f"Processing pipeline stage: {pipeline_stage}")
        if pipeline_stage == 'grant_access':
            grant_admin_access(role_name)
        elif pipeline_stage == 'revoke_access':
            revoke_admin_access(role_name)
        elif pipeline_stage == 'Approval':
            s3_plan_link = get_latest_tfplan_link(bucket_name, prefix)
            s3_console_link = get_latest_tfplan_console_link(bucket_name, prefix)
            if s3_plan_link and s3_console_link:
                send_approval_notification(s3_plan_link, s3_console_link)
            else:
                raise ValueError('Failed to fetch the latest tfplan file link.')
        else:
            raise ValueError("Invalid pipeline stage")

        signal_codepipeline_success(job_id)
    except Exception as e:
        print(f"Error occurred: {e}")
        if role_name:
            try: revoke_admin_access(role_name)
            except Exception as revoke_exception:
                print(f"Failed to a revoke admin access :{revoke_exception}")
        if 'job_id' in locals():
            signal_codepipeline_failure(job_id, str(e))
        return {'statusCode': 400, 'body': json.dumps(f"Error occurred: {e}")}

    return {'statusCode': 200, 'body': json.dumps("Lambda function completed successfully.")}
