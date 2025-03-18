"""
 * @author Idris Adeniji (alvacoder)
 * @email idrisadeniji01@gmail.com
 * @create date 2025-03-18 22:01:56
"""

import requests
import os 
import sys
import logging
#implement grepping dependabot alerts through graphql
class Defectdojo(object):

    def __init__(self):

        # Required Secrets for this awesome code to function.
        self.github_token=os.environ["INPUT_GITHUB_PERSONAL_TOKEN"]
        self.defectdojo_api_key=os.environ["INPUT_DEFECTDOJO_API_KEY"]
        self.defectdojo_username=os.environ["INPUT_DEFECTDOJO_USERNAME"]
        self.defectdojo_password=os.environ["INPUT_DEFECTDOJO_PASSWORD"]
        self.defectdojo_service_account=os.environ["INPUT_DEFECTDOJO_SERVICE_ACCOUNT"]

        # Required Defectdojo Variables.
        self.defectdojo_url=os.environ["INPUT_DEFECTDOJO_URL"]
        self.defectdojo_product_type=os.environ["INPUT_DEFECTDOJO_PRODUCT_TYPE"]
        self.defectdojo_product=os.environ["INPUT_DEFECTDOJO_PRODUCT"]
        self.defectdojo_environment_type=os.environ["INPUT_DEFECTDOJO_ENVIRONMENT_TYPE"]
        self.defectdojo_scan_type=os.environ["INPUT_DEFECTDOJO_SCAN_TYPE"]
        self.defectdojo_engagement_name=os.environ["INPUT_DEFECTDOJO_ENGAGEMENT_NAME"]
        self.scan_results_file_path=os.environ["INPUT_RESULTS_FILE_PATH"]
        self.scan_results_file_path=os.environ["INPUT_RESULTS_FILE_PATH"]
        self.scan_results_file_path=os.environ["INPUT_RESULTS_FILE_PATH"]
        self.client_certificate_file_path=os.environ["INPUT_CLIENT_CERTIFICATE_FILE_PATH"]
        self.client_key_file_path=os.environ["INPUT_CLIENT_KEY_FILE_PATH"]

    def import_scan_results_to_defectdojo(
        self,
        logger: logging.Logger,
    ) -> int:

        requests_timeout = 180

        headers = {
            "Authorization": f"Token {self.defectdojo_api_key}",
        }

        api_endpoint = f"{self.defectdojo_url}/api/v2/import-scan/"

        files = {}
        files["file"] = open(self.scan_results_file_path)

        data = {
            "product_type_name": self.defectdojo_product_type,
            "product_name": self.defectdojo_product,
            "environment": self.defectdojo_environment_type,
            "scan_type": self.defectdojo_scan_type,
            "engagement_name": self.defectdojo_engagement_name,
            "auto_create_context": True,
            "close_old_findings": True,
            "verified": False,
        }
        if self.client_certificate_file_path and self.client_key_file_path:
            r = requests.post(
                api_endpoint,
                headers=headers,
                files=files,
                data=data,
                verify=True,
                cert=(client_certificate_file_path, client_key_file_path),
                timeout=requests_timeout,
            )
        elif not self.client_certificate_file_path and not self.client_key_file_path:
            r = requests.post(
                api_endpoint,
                headers=headers,
                files=files,
                data=data,
                verify=True,
                timeout=requests_timeout,
            )
        else:
            logger.error(
                "either the client certificate or client key file paths were not set correctly"
            )
            sys.exit(1)
        if r.status_code == 201:
            return r.status_code
        else:
            logger.error(f"upload of results to {self.defectdojo_url} failed")
            sys.exit(1)
   
    def run(self):
        try:
            self.import_scan_results_to_defectdojo()

        except Exception as e:
            print("Exception:{}".format(e))
            sys.exit(1)


Defectdojo().run()

