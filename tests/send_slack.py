import logging
import os
import re
import shutil
from collections import namedtuple
import requests
import boto3
import json


logger = logging.getLogger(__name__)

REPORTS = ("test_baseline_container", "test_tracer_container")
OUTPUT_DIR = os.environ["OUTPUT_DIR"]
BRANCH_NAME_CLEAN = os.environ["BRANCH_NAME_CLEAN"]
SLACK_URL = "https://slack.com/api/chat.postMessage"
SLACK_ANUN_CHANNEL = "C02TQAG6BC4"


def get_slack_token():
    ssm = boto3.client("ssm")
    creds = ssm.get_parameter(Name="slack_creds", WithDecryption=True)
    return json.loads(creds["Parameter"]["Value"])["token"]


class SlackData:
    def __init__(self, total=0, passed=0, skipped=0, failed=0, errors=0) -> None:
        self.total = total
        self.passed = passed
        self.skipped = skipped
        self.failed = failed
        self.errors = errors

    def __add__(self, other):

        total_summary = self.total + other.total
        passed_summary = self.passed + other.passed
        skipped_summary = self.skipped + other.skipped
        failed_summary = self.failed + other.failed
        errors_summary = self.errors + other.errors

        return SlackData(
            total_summary,
            passed_summary,
            skipped_summary,
            failed_summary,
            errors_summary,
        )

    def slack_data_dict(self, status, emoji):

        return {
            "summary": f"{self.total} total tests, {self.passed} passed, {self.skipped} skipped, "
            f"{self.failed} failed and {self.errors} errors",
            "project_name": os.environ["PROJECT_NAME"],
            "env": os.environ["STAGE"],
            "status": status,
            "emoji": emoji,
            "report_url": "",
            "branch": BRANCH_NAME_CLEAN,
        }


def post_message_to_slack(blocks=None):
    return requests.post(
        SLACK_URL,
        {
            "token": get_slack_token(),
            "channel": SLACK_ANUN_CHANNEL,
            "blocks": json.dumps(blocks) if blocks else None,
        },
    )


def post_to_slack(test_data):
    logging.info("Post data to slack.")

    try:
        web_hook_url = ""
        report_url = _build_report_url()
        test_data["report_url"] = report_url
        message = _build_web_hook_msg(test_data)
        logger.info(message)
        slack_data = json.dumps(message)
        response = requests.post(
            web_hook_url, data=slack_data, headers={"Content-Type": "application/json"}
        )

        if response.status_code != 200:
            raise ValueError(
                "Request to slack returned an error %s, the response is:\n%s"
                % (response.status_code, response.text)
            )
    except NameError:
        logger.info(
            "User provided secrets are missing, No Slack notification is available"
        )


def _build_web_hook_msg(test_data):
    return {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": test_data["emoji"] + " " + test_data["project_name"],
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "branch:" + " " + test_data["branch"],
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "env:" + " " + test_data["env"],
                    "emoji": True,
                },
            },
            {
                "type": "context",
                "elements": [
                    {"type": "plain_text", "text": test_data["status"], "emoji": True}
                ],
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": test_data["summary"],
                    "emoji": True,
                },
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Test Report",
                            "emoji": True,
                        },
                        "url": test_data["report_url"],
                    }
                ],
            },
            {"type": "divider"},
        ]
    }


def _build_report_url():
    return f"{os.environ['BUILD_URL']}testReport"


def get_value(data, pattern):
    result = re.findall(pattern, data)
    if isinstance(result[0], tuple):
        return " ".join(result[0])

    return result[0]


def read_file(file_name, mode):
    try:
        with open(file_name, mode) as file:
            return file.read()

    except (FileNotFoundError, IOError):
        logging.error("Could not open/read file:", file_name)
        return None


def write_file(result_file, file_name):
    with open(os.path.join(OUTPUT_DIR, file_name), "w+") as file:
        file.write(result_file)
        logging.info(f"Written results to {result_file}. ")


def get_test_data(data):
    logging.info("Getting test data.")
    results_data = namedtuple("results_data", "total, passed, skipped, failed, errors")
    return results_data(
        get_value(data, "\\d+ tests ran"),
        get_value(data, "\\d+ passed"),
        get_value(data, "\\d+ skipped"),
        get_value(data, "\\d+ failed"),
        get_value(data, "\\d+ errors"),
    )


def get_test_result_percentage(total, test):
    """ """
    if test and total:
        return float(format(test / total * 100, ".2f"))
    return 0


def get_test_status(passed_percentage, failed_percentage):
    """ """
    if passed_percentage == 100 and failed_percentage == 0:
        return "Success", ":sunny:"
    if passed_percentage >= 80 and failed_percentage < 10:
        return "Unstable", ":partly_sunny_rain:"

    return "Failed", ":rain_cloud:"


def parse_html_report(report_name):
    """
    Parse pytest html report.
    """

    slack_data = SlackData()
    html_result = read_file(f"{OUTPUT_DIR}/{report_name}-report.html", "r")
    logger.info(f"Reading results from {report_name}-report.html")

    if html_result:
        logger.info(f"Got results from {report_name}-report.html")
        test_data = get_test_data(html_result)

        slack_data.total = int(test_data.total.split(" ")[0])
        slack_data.passed = int(test_data.passed.split(" ")[0])
        slack_data.skipped = int(test_data.skipped.split(" ")[0])
        slack_data.failed = int(test_data.failed.split(" ")[0])
        slack_data.errors = int(test_data.errors.split(" ")[0])

        write_file(html_result, f"{report_name}-report.html")

        if slack_data.total <= 0 or not slack_data.total:
            logger.warning(
                f"Total number of tests ran is: {slack_data.total}. Collecting output.log"
            )
    else:
        logger.error(f"No results in {report_name}-report.html. collecting output.log.")

    logger.info("Making an archive with collected logs.")
    shutil.make_archive("logs", "zip", OUTPUT_DIR)

    return slack_data


def main():
    slack_data_summary = SlackData()
    for report_name in REPORTS:
        slack_data_summary += parse_html_report(report_name)

    passed_percentage = get_test_result_percentage(
        slack_data_summary.total, slack_data_summary.passed
    )
    failed_percentage = get_test_result_percentage(
        slack_data_summary.total, slack_data_summary.failed + slack_data_summary.errors
    )
    status, emoji = get_test_status(passed_percentage, failed_percentage)

    post_to_slack(slack_data_summary.slack_data_dict(status=status, emoji=emoji))


if __name__ == "__main__":
    main()
