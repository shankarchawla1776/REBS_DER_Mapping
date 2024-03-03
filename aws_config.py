import boto3, io, pandas as pd, os
from dotenv import load_dotenv
from pathlib import Path

ds_count = 10
act_count = 3
checkboxes = []
load_dotenv(Path(".env"))

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

bucket_name = 'der-data-rebs'
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

keys = ['DER_data/battery_storage.csv', 'DER_data/distributed_solar.csv', 'DER_data/utility_solar.csv']
keys_1 = ['battery_storage.csv', 'distributed_solar.csv', 'utility_solar.csv']
datasets = {}
for i in range(act_count):
    var_name = f"dataset_{i+1}"
    resp_data = s3_client.get_object(Bucket=bucket_name, Key=keys[i])
    data = resp_data['Body'].read().decode('utf-8')

    datasets[var_name] = pd.read_csv(io.StringIO(data), on_bad_lines='skip')

print(datasets[0])