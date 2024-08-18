
import boto3
import os
import streamlit as st

s3_client = boto3.client(
        's3',
        aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
        region_name=st.secrets["AWS_DEFAULT_REGION"],
    )

bucket_name = st.secrets["BUCKET_NAME"]

response = s3_client.list_objects_v2(Bucket=bucket_name)

if 'Contents' in response:
    files = sorted(response['Contents'], key=lambda x: x['LastModified'], reverse=True)
    most_recent_file = files[0]
    file_key = most_recent_file['Key']

    local_file_path = os.path.join('', os.path.basename(file_key))
    s3_client.download_file(bucket_name, file_key, local_file_path)
    print(f"Downloaded {file_key} to {local_file_path}")
else:
    print("No files found in the bucket.")