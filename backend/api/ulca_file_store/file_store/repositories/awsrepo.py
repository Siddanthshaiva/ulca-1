import logging
from utilities.response import post_error
import boto3 
from config import aws_access_key, aws_secret_key, aws_bucket_name,aws_link_prefix,download_folder
import os

log = logging.getLogger('file')

class AwsFileRepo():

    #uploading file to S3 bucket
    def upload_file_to_s3(self,file_path, file_name,folder):
        s3_file_name =folder+"/"+ file_name
        s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
        try:
            log.info(f'Pushing {file_path} to S3 at {s3_file_name} ......')
            s3_client.upload_file(file_path, aws_bucket_name, s3_file_name)
            return f'{aws_link_prefix}{s3_file_name}'
        except Exception as e:
            log.exception(f'Exception while pushing to s3: {e}', e)
            return post_error("Service Exception",f"Exception occurred:{e}")

    #downloading file from S3 bucket
    def download_file_from_s3(self, s3_file_name):
        s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
        output_filepath = os.path.join( download_folder, s3_file_name)
        try:
            log.info("\nDownloading file to \n\t" + output_filepath)
            s3_client.download_file(aws_bucket_name, s3_file_name,output_filepath)
            return output_filepath
        except Exception as e:
            log.exception(e)
            return post_error("Service Exception",f"Exception occurred:{e}")
            
    #removing file from S3 bucket
    def remove_file_from_s3(self, s3_file_name):
        log.info(f'Deleting {s3_file_name} from S3......')
        s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
        try:
            objects = [{"Key": s3_file_name}]
            response = s3_client.delete_objects(Bucket=aws_bucket_name, Delete={"Objects": objects})
            return response
        except Exception as e:
            log.exception(e)
            return False