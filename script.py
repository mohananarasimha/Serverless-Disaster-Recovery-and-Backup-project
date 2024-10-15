import boto3
import datetime

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    rds_client = boto3.client('rds')
    sns_client = boto3.client('sns')
    # Get current date to add to snapshot names
    current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    # Backup RDS instances
    rds_instances = rds_client.describe_db_instances()['DBInstances']
    for instance in rds_instances:
        instance_id = instance['DBInstanceIdentifier']
        snapshot_id = f"rds-snapshot-{instance_id}-{current_time}"
        print(f"Creating RDS snapshot for {instance_id}")
        rds_client.create_db_snapshot(DBSnapshotIdentifier=snapshot_id, DBInstanceIdentifier=instance_id)

    # Backup EBS volumes
    ec2_instances = ec2_client.describe_instances()['Reservations']
    for reservation in ec2_instances:
        for instance in reservation['Instances']:
            for volume in instance['BlockDeviceMappings']:
                volume_id = volume['Ebs']['VolumeId']
                snapshot_id = f"ebs-snapshot-{volume_id}-{current_time}"
                print(f"Creating EBS snapshot for {volume_id}")
                ec2_client.create_snapshot(VolumeId=volume_id, Description=f"Snapshot of {volume_id} at {current_time}")
    
    sns_client.publish(
        TopicArn='arn:aws:sns:us-east-1:<account_id>:mytopic',
        Message=f"Backup completed for instance {instance_id} at {current_time}",
        Subject='EBS Snapshot Backup Complete'
    )


    return {"statusCode": 200, "body": f"Backups started successfully at {current_time}"}

    # (existing code...)
    
# Serverless Disaster Recovery and Backup project
