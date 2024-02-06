import matplotlib.pyplot as plt
import numpy as np
import boto3
import pandas as pd
from io import StringIO
import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path


load_dotenv(Path(".env"))

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

response = s3_client.get_object(Bucket="dermod", Key='price_per_kWh.csv')
price_data = response['Body'].read().decode('utf-8')
price_df = pd.read_csv(StringIO(price_data))


california_data = price_df[price_df['Name'] == 'California']

column_names = california_data.columns[1:]
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10,  10))

all_axes = axs.flatten()

for i, ax in enumerate(all_axes):
    ax.plot(california_data.index, california_data[column_names[i]])
    ax.set_title(column_names[i])  
    ax.set_xlabel('Index')
    ax.set_ylabel('Value')

for ax in axs.flat:
    ax.label_outer()
plt.tight_layout()


plt.show()
