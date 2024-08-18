from altair import Config
import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def upload_to_s3(file, bucket, object_name=None):
    if object_name is None:
        object_name = file.name

    s3_client = boto3.client(
        's3',
        aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
        region_name=st.secrets["AWS_DEFAULT_REGION"],
    )

    try:
        s3_client.upload_fileobj(file, bucket, object_name)
        st.success(f"File {file.name} uploaded to {bucket}/{object_name}")
    except NoCredentialsError:
        st.error("Credentials not available")
    except ClientError as e:
        st.error(f"Client error: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.title("Upload a class recording to analyze")

uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    bucket_name = st.secrets["BUCKET_NAME"]
    if st.button("Upload to S3"):
        st.info("Uploading file to S3...")
        upload_to_s3(uploaded_file, bucket_name)

    