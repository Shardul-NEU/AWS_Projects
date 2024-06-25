import boto3
import json
import logging
from botocore.exceptions import ClientError
from botocore.config import Config
# Define a custom retry configuration with adaptive mode
custom_retry_config = Config(
    retries={
        'max_attempts': 10,
        'mode': 'adaptive'
    }
)
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Adjust as needed

def create_client(service_name):
    # Create an AWS service client with the custom retry configuration
    return boto3.client(service_name, config=custom_retry_config)

# Initialize AWS SDK clients with custom retry configuration
services = [
    's3', 'ec2', 'rds', 'lambda', 'dynamodb', 'efs', 'fsx', 'ecs', 'ecr', 'elbv2', 'autoscaling','kendra','iam',
    'route53', 'route53resolver', 'backup', 'cloudwatch', 'sns',
]
clients = {service: create_client(service) for service in services}

def convert_tags(tags_dict):
    return [{'Key': key, 'Value': value} for key, value in tags_dict.items()]

service_info = {
    's3': {
            'CreateBucket': lambda event: [event['detail']['requestParameters']['bucketName']],
    },
    'ec2': {
         
            'RunInstances': lambda event: [item['instanceId'] for item in event['detail']['responseElements']['instancesSet']['items']],
            'CreateVolume': lambda event: [event['detail']['responseElements']['volumeId']],
            'CreateSnapshot': lambda event: [event['detail']['responseElements']['snapshotId']],
            'CreateNetworkInterface': lambda event: [event['detail']['responseElements']['networkInterface']['networkInterfaceId']],
            'CreateSecurityGroup': lambda event: [event['detail']['responseElements']['groupId']],
            'CreateImage': lambda event: [event['detail']['responseElements']['imageId']],
            'CreatePlacementGroup': lambda event: [],  # Placement groups don't have a direct ID in the event; may need to handle differently
            'CreateNatGateway': lambda event: [event['detail']['responseElements']['natGateway']['natGatewayId']],
            'CreateInternetGateway': lambda event: [event['detail']['responseElements']['internetGateway']['internetGatewayId']],
            'CreateRouteTable': lambda event: [event['detail']['responseElements']['routeTable']['routeTableId']],
            'CreateDhcpOptions': lambda event: [event['detail']['responseElements']['dhcpOptions']['dhcpOptionsId']],
            'CreateVpc': lambda event: [event['detail']['responseElements']['vpc']['vpcId']],
            'CreateSubnet': lambda event: [event['detail']['responseElements']['subnet']['subnetId']],
            'CreateVpnConnection': lambda event: [event['detail']['responseElements']['vpnConnection']['vpnConnectionId']],
            'CreateVpnGateway': lambda event: [event['detail']['responseElements']['vpnGateway']['vpnGatewayId']],
            'CreateTransitGateway': lambda event: [event['detail']['responseElements']['transitGateway']['transitGatewayId']],
            'CreateTransitGatewayAttachment': lambda event: [event['detail']['responseElements']['transitGatewayAttachment']['transitGatewayAttachmentId']],
            'CreateVpcPeeringConnection': lambda event: [event['detail']['responseElements']['vpcPeeringConnection']['vpcPeeringConnectionId']],
            'CreateLaunchTemplate': lambda event: [event['detail']['responseElements']['CreateLaunchTemplateResponse']['launchTemplate']['launchTemplateId']],
            'CreateEgressOnlyInternetGateway': lambda event: [event['detail']['responseElements']['egressOnlyInternetGateway']['egressOnlyInternetGatewayId']],
            'CreateCustomerGateway': lambda event: [event['detail']['responseElements']['customerGateway']['customerGatewayId']],
            'CreateTrafficMirrorTarget': lambda event: [event['detail']['responseElements']['trafficMirrorTarget']['trafficMirrorTargetId']],
            'CreateTrafficMirrorSession': lambda event: [event['detail']['responseElements']['trafficMirrorSession']['trafficMirrorSessionId']],
            'CreateTrafficMirrorFilter': lambda event: [event['detail']['responseElements']['trafficMirrorFilter']['trafficMirrorFilterId']],
            'AllocateAddress': lambda event: [event['detail']['responseElements']['allocationId']],
    },

    'autoscaling': {
            'CreateAutoScalingGroup': lambda event: [event['detail']['requestParameters']['autoScalingGroupName']],
    },
   
    'elasticloadbalancing': {
            'CreateLoadBalancer': lambda event: [event['detail']['responseElements']['loadBalancers'][0]['loadBalancerArn']],  # Applies to both Application and Network Load Balancers
            'CreateTargetGroup': lambda event: [event['detail']['responseElements']['targetGroups'][0]['targetGroupArn']],
    },
    'rds': {
            'CreateDBInstance': lambda event: [f"arn:aws:rds:{event['region']}:{event['account']}:db:{event['detail']['requestParameters']['dBInstanceIdentifier']}"],
            'CreateDBSnapshot': lambda event: [event['detail']['responseElements']['dBSnapshot']['dBSnapshotArn']],
            'CreateDBCluster': lambda event: [event['detail']['responseElements']['dBCluster']['dBClusterArn']],
            'CreateDBClusterSnapshot': lambda event: [event['detail']['responseElements']['dBClusterSnapshot']['dBClusterSnapshotArn']],
            'CreateDBClusterEndpoint': lambda event: [event['detail']['responseElements']['dBClusterEndpoint']['dBClusterEndpointArn']],
            'CreateDBParameterGroup': lambda event: [f"arn:aws:rds:{event['region']}:{event['account']}:pg:{event['detail']['requestParameters']['dBParameterGroupName']}"],
            'CreateDBOptionGroup': lambda event: [f"arn:aws:rds:{event['region']}:{event['account']}:og:{event['detail']['requestParameters']['dBOptionGroupName']}"],
            'CreateDBSecurityGroup': lambda event: [f"arn:aws:rds:{event['region']}:{event['account']}:secgrp:{event['detail']['requestParameters']['dBSecurityGroupName']}"],
            'CreateDBSubnetGroup': lambda event: [f"arn:aws:rds:{event['region']}:{event['account']}:subgrp:{event['detail']['requestParameters']['dBSubnetGroupName']}"],
    # Note: Custom event handlers might be required for resources that do not directly provide an ARN in the event response.
    },
    'lambda': {
        
            'CreateFunction20150331': lambda event: [event['detail']['responseElements']['functionArn']],
    },
    'dynamodb': {
            'CreateTable': lambda event: [event['detail']['responseElements']['tableDescription']['tableArn']],
    },
    'elasticfilesystem': {
            'CreateFileSystem': lambda event: [event['detail']['responseElements']['fileSystemId']],
    },
    'ecs': {
            'CreateCluster': lambda event: [event['detail']['responseElements']['cluster']['clusterArn']],
    },
    'ecr': {
            'CreateRepository': lambda event: [event['detail']['responseElements']['repository']['repositoryArn']]
    },
    'iam': {
            'CreateUser': lambda event: [event['detail']['responseElements']['user']['arn']],
            'CreateRole': lambda event: [event['detail']['responseElements']['role']['arn']],
    },
    'kendra': {
            'CreateIndex': lambda event: [event['detail']['responseElements']['indexArn']],
            'CreateDataSource': lambda event: [event['detail']['responseElements']['id']], # This is yet to be tested and has errors
            'CreateFaq': lambda event: [event['detail']['responseElements']['id']], # This is yet to be tested and has errors
    },
    'route53':{
        
            'CreateHostedZone': lambda event: ['/hostedzone/' + event['detail']['responseElements']['hostedZone']['id']],
            'CreateHealthCheck': lambda event: ['/healthcheck/' + event['detail']['responseElements']['healthCheck']['id']],
    },
    'route53resolver': {
            'CreateResolverEndpoint': lambda event: [event['detail']['responseElements']['resolverEndpoint']['arn']],
    },
    'backup': {
            'CreateBackupVault': lambda event: [event['detail']['responseElements']['backupVaultName']],
    },
    'cloudwatch': {
            'PutMetricAlarm': lambda event: [event['detail']['requestParameters']['alarmName']],
    # Note: Adapt these based on your event structure or scheduling mechanism
    },
    'sns': {
            'CreateTopic': lambda event: [event['detail']['responseElements']['topicArn']],
    },
    # Add other services as necessary
}
def find_event_extractor(serviceName, eventName):
    service = service_info.get(serviceName)
    if service:
        return service.get(eventName, None)
    return None

def tag_resources(service,resource_ids,tags):
    if not resource_ids:
        logger.info(f"No resource IDs extracted for service {service}.")
        return False
    
    client = clients.get(service)
    logger.info(f"returned client : {client} for service : {service}")
    converted_tags = convert_tags(tags)

    def tag_ecompute(): clients['ec2'].create_tags(Resources=resource_ids, Tags=converted_tags)

    def tag_elb(): clients['elbv2'].add_tags(ResourceArns=resource_ids, Tags=converted_tags)
    
    def tag_resource():
        for resource_id in resource_ids:
                if service == 'lambda': client.tag_resource(Resource=resource_id, Tags=tags)
                elif service == 'elasticfilesystem': clients['efs'].tag_resource(ResourceId=resource_id, Tags=converted_tags)
                elif service in ['kendra','cloudwatch']: client.tag_resource(ResourceARN=resource_id, Tags=converted_tags)
                elif service == 'backup' : client.tag_resource(ResourceARN=resource_id, Tags=tags)
                else: client.tag_resource(ResourceArn=resource_id, Tags=converted_tags)

    def tag_econtainer():
        for resource_id in resource_ids:
                if service== 'ecs':
                    ecs_tags = [{'key': key, 'value': value} for key, value in tags.items()]
                    tag = ecs_tags
                else:
                    tag = converted_tags
                client.tag_resource(resourceArn=resource_id, tags=tag)

    def tag_s3():
        for bucket_name in resource_ids:
                client.put_bucket_tagging(Bucket=bucket_name, Tagging={'TagSet': converted_tags})
    
    def tag_rds():
        for resource_id in resource_ids:
                client.add_tags_to_resource(ResourceName=resource_id, Tags=converted_tags)
    
    def tag_iam():

        for usernameARN in resource_ids:
            resource_name = usernameARN.split('/')[-1]

    # Apply tags based on whether the resource is a user or a role
        if 'user/' in usernameARN:
            client.tag_user(UserName=resource_name, Tags=converted_tags)
        elif 'role/' in usernameARN:
            client.tag_role(RoleName=resource_name, Tags=converted_tags)
        else:
            print(f"Unsupported IAM resource type for ARN: {resource_ids}")
         

    def tag_auto_scaling_group():  # Ensure 'autoscaling' client is initialized
        for resource_id in resource_ids:
            try:
                 # Format tags according to the Auto Scaling API requirements
                formatted_tags = [{
                    'ResourceId': resource_id,
                    'ResourceType': 'auto-scaling-group',
                    'Key': key,
                    'Value': value,
                    'PropagateAtLaunch': True
                } for key, value in tags.items()]
            
            # Apply tags to the Auto Scaling group
                client.create_or_update_tags(Tags=formatted_tags)
                logger.info(f"Successfully tagged Auto Scaling group '{resource_id}' with {tags}.")
            except ClientError as e:
                logger.error(f"Failed to tag Auto Scaling group '{resource_id}': {e}")
                return False
        return True
    
    def tag_route53():
        for resource_id in resource_ids:
            if resource_id.startswith('/hostedzone/'):
                resource_type = 'hostedzone'
            elif resource_id.startswith('/healthcheck/'):
                resource_type = 'healthcheck'
            else:
                raise ValueError("Unsupported Route 53 resource type")
            
        resource_id = resource_id.split('/')[-1]
        clients['route53'].change_tags_for_resource(ResourceType=resource_type.upper(),ResourceId=resource_id,AddTags=converted_tags)

    service_actions = {
        'ec2': tag_ecompute, 'elasticloadbalancing': tag_elb, 'autoscaling': tag_auto_scaling_group,
        'elasticfilesystem': tag_resource, 'dynamodb': tag_resource, 'cloudwatch': tag_resource,
        'fsx': tag_resource, 'lambda': tag_resource, 'backup': tag_resource, 'sns': tag_resource,
        'ecs': tag_econtainer, 'ecr': tag_econtainer, 'iam': tag_iam, 'route53':tag_route53,
        's3': tag_s3, 'rds': tag_rds, 'kendra': tag_resource, 'route53resolver': tag_resource,
    }
    
    try:
         if service in service_actions:
            service_actions[service]()
            logger.info(f"Successfully tagged {len(resource_ids)} resource(s) in {service} with {tags}")
            return True
         else:
            logger.error(f"Service {service} not supported for tagging.")
            return False 
    except ClientError as e:
        logger.error(f"Failed to tag {service} resource {resource_ids}: {e}")
        return False

def lambda_handler(event, context):
    try:
        eventName= event['detail']['eventName']
        serviceName = event['detail']['eventSource'].split('.')[0]
        if serviceName == 'monitoring': serviceName = 'cloudwatch'

        extractor_func = find_event_extractor(serviceName, eventName)
        if not extractor_func:
            logger.info(f"Unsupported event {eventName} for service {serviceName}.")
            return {'statusCode': 400, 'body': json.dumps(f"Unsupported event {eventName} for service {serviceName}.")}
        
        user_name = event['detail']['userIdentity']['arn'].split('/')[-1]

        logger.info(f"Processing event from service: {serviceName}. Event name: {eventName}. Triggered by user: {user_name}")
        tags = {'CreatedBy': user_name, 'CostCenter': '100082_itinfra'}
        
        # In case of Kendra
        region = event["detail"]["awsRegion"]
        accountId = event["detail"]['recipientAccountId']
        
        if serviceName == "kendra" and eventName == "CreateDataSource":
            # Construct the ARN for Kendra DataSource
            indexId = event['detail']['requestParameters']['indexId']
            dataSourceId = event['detail']['responseElements']['id']
            ARN = [f"arn:aws:kendra:{region}:{accountId}:index/{indexId}/data-source/{dataSourceId}"]
            resource_ids = ARN

        elif serviceName == 'cloudwatch':
            alarmName = event['detail']['requestParameters']['alarmName']
            ARN = [f"arn:aws:cloudwatch:{region}:{accountId}:alarm:{alarmName}"]
            resource_ids = ARN

        else: resource_ids = extractor_func(event)    #for other resources

        # Tag resources using the unified tagging function
        success = tag_resources(serviceName, resource_ids, tags)  # Simplified call

        message = f"Resource(s): {eventName.upper()} for {serviceName.upper()} tagged successfully!" if success else f"Failed to tag resources for {serviceName}."
        status_code = 200 if success else 400

        logger.info(message)
    except ClientError as e:
        error_code = e.response['Error']['Code']
        message = f"ClientError occurred: {error_code}"
        status_code = 500
        logger.exception(message)
    except Exception as e:
        message = f"Error: {str(e)}"
        status_code = 500
        logger.exception(message)

    return {
        'statusCode': status_code,
        'body': json.dumps(message)
    }