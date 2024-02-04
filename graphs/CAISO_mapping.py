import matplotlib.pyplot as plt
import numpy as np
import boto3
import pandas as pd
from io import StringIO
import io
import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

load_dotenv(Path(".env"))

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

resp_p_per_kWh = s3_client.get_object(Bucket="dermod", Key='price_per_kWh.csv')
price_data = resp_p_per_kWh['Body'].read().decode('utf-8')
price_df = pd.read_csv(io.StringIO(price_data))

california_data = price_df[price_df['Name'] == 'California']

fig, ax = plt.subplots(figsize=(10, 8))  # Increase the height of the figure

bar_positions = np.arange(len(california_data.columns[1:]))
bar_height = california_data.iloc[0, 1:].astype(float)

bars = ax.barh(bar_positions, bar_height, color='skyblue')

ax.set_xlabel('Values')
ax.set_ylabel('Categories')
ax.set_title('California Energy Data')
ax.set_yticks(bar_positions)
ax.set_yticklabels(california_data.columns[1:])
ax.invert_yaxis()  

# Display values on the bars in scientific notation
for i, value in enumerate(bar_height):
    ax.text(value, i, f'{value:.2e}', va='center', fontsize=10)

# Adjust x-axis limits
ax.set_xlim(0, max(bar_height) * 1.1)  # Set limits to accommodate the text labels

plt.show()
