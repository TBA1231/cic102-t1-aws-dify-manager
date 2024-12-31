class Cloudwatch:
    def __init__(self, ec2_client, cloudwatch_client):
        self.ec2_client = ec2_client
        self.cloudwatch_client = cloudwatch_client

# get all EC2 instances
    def get_ec2_info(self):
        try:
            response = self.ec2_client.describe_instances()
            return response
        except Exception as e:
            print(f"Error occurred: {e}")

# Get CPU metrics for an instance in the given period of time
    def get_ec2_cpu_usage(self, instance_id, start_date, end_date):
        instance_id = "i-05380600ada372b26"
        try:
            response = self.cloudwatch_client.get_metric_statistics(
                Namespace= 'EC2',
                MetricName= 'CPUUtilization',
                Dimensions=[
                    {
                        'Name': 'instanceId',
                        'Value': instance_id
                    },
                ],
                StartTime=start_date,
                EndTime=end_date,
                Period= 3600,
                Statistics=['Average'],
                Unit= 'Percent'
            )

            print(response)
            return response
        except Exception as e:
            print(f"Error occurred: {e}")
