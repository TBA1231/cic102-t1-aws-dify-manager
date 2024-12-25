
def get_billing_info(client, start_date, end_date, granularity="MONTHLY"):
    try:
        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date,
            },
            Granularity=granularity,
            Metrics=["UnblendedCost"],
        )

        return response
    except Exception as e:
        print(f"Error occurred: {e}")