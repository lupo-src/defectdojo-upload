"""
 * @author Idris Adeniji (alvacoder)
 * @email idrisadeniji01@gmail.com
 * @create date 2025-03-18 22:01:56
"""

import requests
import os
import sys
import logging

class Defectdojo:

    def __init__(self):
        # Required Secrets for this awesome code to function.
        self.defectdojo_api_key = os.environ["defectdojo_api_key"]
        self.defectdojo_username = os.environ["defectdojo_username"]
        self.defectdojo_password = os.environ["defectdojo_password"]
        self.defectdojo_service_account = os.environ["defectdojo_service_account"]

        # Required Defectdojo Variables.
        self.defectdojo_url = os.environ["defectdojo_url"]
        self.defectdojo_product_type = os.environ["defectdojo_product_type"]
        self.defectdojo_product = os.environ["defectdojo_product"]
        self.defectdojo_environment_type = os.environ["defectdojo_environment_type"]
        self.defectdojo_scan_type = os.environ["defectdojo_scan_type"]
        self.defectdojo_engagement_name = os.environ["defectdojo_engagement_name"]
        self.scan_results_file_path = os.environ["scan_results_file_path"]

    def import_scan_results_to_defectdojo(
        self,
        logger: logging.Logger,
        client_certificate_file_path=None,
        client_key_file_path=None
    ) -> int:

        api_endpoint = f"{self.defectdojo_url}/api/v2/import-scan/"
        headers = {"Authorization": f"Token {self.defectdojo_api_key}"}
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

        try:
            with open(self.scan_results_file_path, "rb") as scan_file:
                files = {"file": scan_file}

                if client_certificate_file_path and client_key_file_path:
                    r = requests.post(
                        api_endpoint,
                        headers=headers,
                        files=files,
                        data=data,
                        verify=True,
                        cert=(client_certificate_file_path, client_key_file_path),
                        timeout=180
                    )
                else:
                    r = requests.post(
                        api_endpoint,
                        headers=headers,
                        files=files,
                        data=data,
                        verify=True,
                        timeout=180
                    )

                if r.status_code == 201:
                    return r.status_code
                else:
                    logger.error(f"Upload of results failed with status code {r.status_code}")
                    sys.exit(1)
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during scan upload: {e}")
            sys.exit(1)

    def run(self):
        try:
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.INFO)
            self.import_scan_results_to_defectdojo(logger)
        except Exception as e:
            print(f"Exception: {e}")
            sys.exit(1)

if __name__ == "__main__":
    Defectdojo().run()
