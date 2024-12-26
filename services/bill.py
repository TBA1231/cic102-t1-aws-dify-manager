
class Bill:
    def __init__(self, client):
        self.client = client

    def get_billing_info(start_date, end_date, granularity="MONTHLY"):
        try:
            response = self.client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date.strftime("%Y-%m-%d"),
                    'End': end_date.strftime("%Y-%m-%d"),
                },
                Granularity=granularity,
                Metrics=["UnblendedCost"],
            )

            return response
        except Exception as e:
            print(f"Error occurred: {e}")