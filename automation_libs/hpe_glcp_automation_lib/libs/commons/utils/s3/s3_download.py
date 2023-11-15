import base64
import json
import logging
import os
import shutil
import subprocess
import sys

from hpe_glcp_automation_lib.libs.commons.utils.s3.s3_utils import S3Utils

log = logging.getLogger(__name__)

if len(sys.argv) > 1:
    repo_path: str = sys.argv[1]


def s3_details():
    kube_output_bytes = subprocess.check_output(
        "kubectl get secret -n cloudops glcps3automation -o json", shell=True
    )
    kube_output_string = kube_output_bytes.decode("utf-8")
    output_dict = json.loads(kube_output_string)
    bucket_name = base64.b64decode(
        output_dict.get("data", {}).get("bucket_name", "")
    ).decode("utf-8")
    aws_access_key_id = base64.b64decode(
        output_dict.get("data", {}).get("aws_access_key_id", "")
    ).decode("utf-8")
    aws_secret_access_key = base64.b64decode(
        output_dict.get("data", {}).get("aws_secret_access_key", "")
    ).decode("utf-8")
    return bucket_name, aws_access_key_id, aws_secret_access_key


def decrypt_file(cert, enc_filename, s3_obj, dec_filename):
    try:
        get_cwd = os.getcwd()
        os.system(
            "kubectl -n cloudops get secrets glcps3automation -o json | jq -r .data.%s | base64 --decode > use_cert"
            % cert
        )
        os.system(
            "openssl smime -decrypt -in %s -inform DER -inkey use_cert > %s"
            % (s3_obj, dec_filename)
        )
        shutil.copy(f"{get_cwd}/%s" % dec_filename, s3_obj.split("%s" % enc_filename)[0])
    except Exception as e:
        log.error(f"not able to decrypt user_creds.json.enc file: {e}")


def download_file(s3_file):
    b_name, access_key, secret_key = s3_details()
    (
        bucket_name,
        aws_access_key_id,
        aws_secret_access_key,
    ) = s3_details()
    s3 = S3Utils(
        bucket_name=b_name,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    bucket = s3.s3conn.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=s3_file):
        os.makedirs(os.path.dirname(obj.key), exist_ok=True)
        s3.download_file(obj.key, obj.key)
        if "user_creds.json.enc" in obj.key:
            try:
                with open(os.path.join(obj.key)) as fd:
                    json.load(fd)
            except:
                log.info("file %s is encrypted, will decrypt it" % obj.key)
                decrypt_file(
                    "glcp_automation_s3_dec",
                    "user_creds.json.enc",
                    obj.key,
                    "user_creds.json",
                )

        if "user_creds_aquila.json.enc" in obj.key:
            try:
                with open(os.path.join(obj.key)) as fd:
                    json.load(fd)
            except:
                log.info("file %s is encrypted, will decrypt it" % obj.key)
                decrypt_file(
                    "glcp_automation_s3_dec_prod",
                    "user_creds_aquila.json.enc",
                    obj.key,
                    "user_creds_aquila.json",
                )


if __name__ == "__main__":
    download_file(repo_path)
