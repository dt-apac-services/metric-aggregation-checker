import os
import requests

dt_url = os.environ.get('dt_url','')
dt_api_token = os.environ.get('dt_api_token','')
metric_id = os.environ.get('dt_metric_id','')
display=os.environ.get('dt_display','all')  # all, unit, defaultAggregation or aggregations. Default = all
logging=os.environ.get('dt_logging','')

if logging:
    print(f"DT URL: {dt_url}")
    print(f"DT Metric ID: {metric_id}")
    print(f"DT Display Choice: {display}")
    
if dt_url == '':
    print('Environment variable dt_url is missing. Should be like: https://abc12345.live.dynatrace.com. Please set. Exiting')
    exit()

if dt_api_token == '':
    print('Environment variable dt_api_token is missing. API token requires v2 read metrics permission. Please set. Exiting')
    exit()

if metric_id == '':
    print('Environment variable dt_metric_id is missing. Please set. Exiting')
    exit()

headers = {
    "Authorization": f"Api-token {dt_api_token}"
}

response = requests.get(
    url=f"{dt_url}/api/v2/metrics/{metric_id}",
    headers=headers
)

result = {}

if logging:
    print(f"DT Status Code: {response.status_code}")

if response.status_code != 200: # Call to DT failed. Print error.
    result = {
        "status": "error",
        "status_code": response.status_code,
        "response": response.text
    }
else: # Call to DT worked. Print response.
    metric_json = response.json()
    
    # Every result includes the displayName
    result = {
        "displayName": metric_json['displayName']
    }
    
    if display == "all":
        result['unit'] = metric_json['unit']
        result['aggregations'] = metric_json['aggregationTypes']
        result['defaultAggregation'] = metric_json['defaultAggregation']
    elif display == "unit":
        result['unit'] = metric_json['unit']
    elif display == "defaultAggregation":
        result['defaultAggregation'] = metric_json['defaultAggregation']
    elif display == "aggregations":
        result['aggregations'] = metric_json['aggregationTypes']

# Print final result (error or successful output) back to user
print(result)
