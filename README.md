# DefectDojo Upload v1.0.0

This GitHub Action uploads a supported scan report generated from your pipeline to a DefectDojo instance. A list of supported reports can be found here - https://documentation.defectdojo.com/integrations/parsers/file/

alvacoder/defectdojo-upload@v1.0.0


## About DefectDojo

[DefectDojo](https://github.com/DefectDojo/django-DefectDojo) is a security orchestration and vulnerability management platform. DefectDojo allows you to manage your application security program, maintain product and application information, triage vulnerabilities and push findings to systems like JIRA and Slack. DefectDojo enriches and refines vulnerability data using a number of heuristic algorithms that improve with the more you use the platform.

## Inputs

NB: The defectdojo_username and defectdojo_password should be passed if you are using basic authentication, and if you are using API key authentication, then you should pass in the defectdojo_api_key.

| Input Name                   | Required |
| ---------------------------- | -------- | 
| defectdojo_username          | False     |
| defectdojo_password          | False     |
| defectdojo_service_account   | False     |
| defectdojo_api_key           | False     |
| defectdojo_url               | True     |
| defectdojo_product_type      | True     |
| defectdojo_product           | True     |
| defectdojo_environment_type  | True     |
| defectdojo_scan_type         | True     |
| defectdojo_engagement_name   | True     |
| scan_results_file_name       | True     |

## Examples

### Using this action with with semgrep

#### About semgrep

[Semgrep](https://github.com/returntocorp/semgrep) is a fast, open-source, static analysis engine for finding bugs, detecting vulnerabilities in third-party dependencies, and enforcing code standards.

In this example we run a Semgrep SAST scan and then use this action to import it into a defectdojo instance.

```
name: semgrep-sast-scan-and-import-to-defectdojo
on:
  push
jobs:
  semgrep-sast-scan:
    name: semgrep sast scan
    runs-on: ubuntu-latest
    container:
      image: returntocorp/semgrep
    if: (github.actor != 'dependabot[bot]')
    steps:
      - name: checkout
        id: checkout
        uses: actions/checkout@v3
      - name: semgrep scan
        id: semgrep-scan
        run: |
          mkdir -p semgrep/results
          semgrep --config auto --error --json --output=semgrep/results/semgrep.json
      - name: upload semgrep results
        id: upload-semgrep-results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: semgrep-results
          path: semgrep/results/

  import-semgrep-report:
    name: import semgrep report
    runs-on: ubuntu-latest
    steps:
      - name: download scan results artifact
        id: download-scan-results-artifact
        uses: actions/download-artifact@v4
        with:
          name: semgrep-results
      - name: import scan results into defectdojo
        id: import-scan-results-into-defectdojo
        uses: alvacoder/defectdojo-upload@v1.0.0
        with:
          defectdojo_url: https://defectdojo.example.con
          defectdojo_username: ${{ secrets.defectdojo_username }}
          defectdojo_password: ${{ secrets.defectdojo_password }}
          defectdojo_password: ${{ secrets.defectdojo_api_key }}
          defectdojo_product_type: example_product_type
          defectdojo_product: example_product
          defectdojo_environment_type: Production
          defectdojo_scan_type: Semgrep JSON Report
          defectdojo_engagement_name: Github Actions Initiated SAST Scan
          scan_results_file_name: semgrep.json
```