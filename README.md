# Serverless-Disaster-Recovery-and-Backup-project

This project requires Lambda,Cloudwatch,IAM,EventBridge Rule,EC2(instance),Snapshots,SNS.

Here whenever a new ec2_instance or rds_instance is created , this lambda function will trigger and creates a snapshot (We can also create timely snapshots) and will send and message to sns topic which inturn publishes to a mail.
