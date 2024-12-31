class Cloudwatch:
    def __init__(self, client):
        self.client = client

# get all EC2 instances
    def get_ec2_info(self):
        try:
            response = self.client.describe_instances()
            return response
        except Exception as e:
            print(f"Error occurred: {e}")

# Get CPU metrics for an instance in the given period of time
    def get_ec2_cpu_usage(self, instance_id, start_date, end_date):
        try:
            response = self.client.get_metric_data(
                MetricDataQueries=[
        {
            'Id': instance_id,
            'MetricStat': {
                'Metric': {
                    'Namespace': 'cic102-t1/EC2',
                    'MetricName': 'CPUusage',
                    'Dimensions': [
                        {
                            'Name': 'instance Id',
                            'Value': instance_id
                        }
                    ]
                },
                'Period': 3600,
                'Stat': 'avarage',
                'Unit': 'Percent'
            }
        }
    ],
    StartTime=start_date,
    EndTime=end_date,
    LabelOptions={
        'Timezone': '+0800'
    }
)
            return response
        except Exception as e:
            print(f"Error occurred: {e}")
