import requests
from robocorp import workitems
from robocorp.tasks import task

INSURANCE_SYSTEM_URL = "https://robocorp.com/inhuman-insurance-inc/sales-system-api"


@task
def consume_traffic_data():
    """
    Inhuman Insurance, Inc. Artificial Intelligence System robot.
    Consumes traffic data work items.
    """
    for item in workitems.inputs:
        traffic_data = item.payload["traffic_data"]
        # Marking item as done if data is valid and response's status code is 200
        if is_valid_traffic_data(traffic_data):
            status, return_json = post_traffic_data_to_sales_system(traffic_data)
            if status == 200:
                item.done()
            else: 
                item.fail(
                    exception_type="APPLICATION",
                    code="TRAFFIC_DATA_POST_FAILED",
                    message=return_json["message"],
                )
        else:
            item.fail(
                exception_type="BUSINESS",
                code="INVALID_TRAFFIC_DATA",
                message=item.payload,
            )

def is_valid_traffic_data(traffic_data):
    return len(traffic_data["country"]) == 3

def post_traffic_data_to_sales_system(traffic_data):
    response = requests.post(INSURANCE_SYSTEM_URL, json=traffic_data)    
    return response.status_code, response.json()
