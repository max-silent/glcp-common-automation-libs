import json
import logging
import os

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class ContinuousMonitoringUtils:
    def __init__(self):
        self.secret_name = "glcps3automation"
        self.region_name = "eu-west-3"
        self.bucket_name = "glcp-automation"

    def get_secret(self, secret_name, region_name):
        """
        Get the secret from GLCP Automation
        :param secret_name: Secret name
        :param region_name: Region name
        :return: secret
        """

        if secret_name:
            self.secret_name = secret_name
        if region_name:
            self.region_name = region_name

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name="secretsmanager", region_name=self.region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(SecretId=self.secret_name)
        except ClientError as client_error:
            logger.error(
                "Exception while retrieving secrets from Secrets Manager: %s ",
                client_error,
            )

        # Catching for general Exception
        except Exception as error:
            logger.error("General Exception caught : %s", error)

        # Decrypts secret using the associated KMS key.
        secret = get_secret_value_response["SecretString"]

        return secret

    def get_cluster_info_from_s3(self, cluster_name, bucket_name, target_path):
        """
        Download the cluster information from S3
        :param cluster_name: Cluster name
        :param bucket_name: S3 bucket name
        :param target_path: Path in which file should be downloaded to
        """
        base_path = "akuc/common/clusterinfo/legacy"

        cluster_files = {
            "polaris": "polaris-us-west-2.json",
            "mira": "mira-us-east-2.json",
            "pavo": "pavo-us-west-2.json",
            "aquila": "aquila-us-west-2.json",
        }
        file_name = cluster_files.get(cluster_name)
        if file_name:
            self.download_file_from_s3(
                bucket_name, os.path.join(base_path, file_name), target_path
            )
        else:
            logger.error(f"Cluster info is not available for cluster {cluster_name}")

    def download_file_from_s3(self, bucket_name, object_key, target_path):
        """
        Download the file from S3 and copy to target path provided
        :param bucket_name: S3 bucket name
        :param object_key: Object key to be downloaded
        :param target_path: Path in which file should be downloaded to
        """
        if bucket_name:
            self.bucket_name = bucket_name
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        secret = self.get_secret("glcps3automation", "eu-west-3")
        secret_json = json.loads(secret)

        aws_access_key_id = secret_json.get("aws_access_key_id")
        aws_secret_access_key = secret_json.get("aws_secret_access_key")

        s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name="us-west-2",
        )

        try:
            s3_client.download_file(
                self.bucket_name,
                object_key,
                target_path,
            )
            logger.info(
                f"Successfully downloaded file {object_key} from S3 and copied to target path {target_path}"
            )
        except Exception as exception:
            logger.error(exception)
