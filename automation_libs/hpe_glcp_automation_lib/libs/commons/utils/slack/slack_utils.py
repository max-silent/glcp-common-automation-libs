"""
Slack utility
"""
import logging
import os

import requests

from hpe_glcp_automation_lib.libs.commons.utils.testrail.testrail import TestRailResult

log = logging.getLogger(__name__)


class SlackNotification:
    """
    A class for sending notifications to Slack.
    """

    def __init__(self):
        """
        Initialize the SlackNotification instance.

        """
        self.headers = {"contentType": "application/json"}

    def send_notification(self, name, date, data):
        """
        Send a notification to Slack.

        Args:
            name (str): The name of the test project.
            date (str): The date of the notification.
            data (dict): The data to be included in the notification.

        Raises:
            SystemExit: If the Slack webhook is not provided or the notification
            fails to send.
        """
        try:
            parsed_result = self._parse_notification_data(data)
            run_data = {
                "Passed": parsed_result[0],
                "Failed": parsed_result[1],
                "Untested": parsed_result[2],
            }
            run_data["Total"] = (
                run_data["Passed"] + run_data["Failed"] + run_data["Untested"]
            )

            webhook = os.getenv("SLACK_WEBHOOK")
            if webhook is None:
                log.error("No Slack Webhook Found.")
                exit(-1)
            else:
                color = "#F4FF48"
                if run_data["Total"] == run_data["Passed"]:
                    color = "#07BB51"
                elif run_data["Total"] == run_data["Untested"] + run_data["Passed"]:
                    color = "#F4FF48"
                elif run_data["Failed"] > 0:
                    color = "#FF0000"
                else:
                    pass
                message = (
                    "*Test Results:*\n*_Total Tests :_* {Total}\n\n*_Passed:_* "
                    "{Passed}      *_Failed :_* {Failed}      *_Untested :_* {"
                    "Untested}\n*_TestRail Run :_* {TestRail Run}\n".format(**run_data)
                )
                payload = {
                    "attachments": [
                        {
                            "color": color,
                            "blocks": [
                                {
                                    "type": "header",
                                    "text": {
                                        "type": "plain_text",
                                        "text": name,
                                        "emoji": True,
                                    },
                                },
                                {"type": "divider"},
                                {
                                    "type": "section",
                                    "text": {"type": "mrkdwn", "text": date},
                                },
                                {
                                    "type": "section",
                                    "text": {"type": "mrkdwn", "text": message},
                                },
                                {"type": "divider"},
                            ],
                        }
                    ]
                }
                response = requests.post(webhook, headers=self.headers, json=payload)
                if response.status_code == 200:
                    log.info("Notification sent to Slack.")
                else:
                    log.error("Failed to send notification to Slack.")
        except Exception as err:
            log.error(err)
            exit(-1)

    @staticmethod
    def _parse_notification_data(data):
        """
        Method to parse notification data
        :param data: session data from testrail_plugin class
        :return: pass_count, fail_count, untested_count as a tuple
        """
        pass_count = 0
        fail_count = 0
        skip_count = 0
        for item in data:
            if data[item]["status"] == TestRailResult.PASSED.value:
                pass_count += 1
            elif data[item]["status"] == TestRailResult.FAILED.value:
                fail_count += 1
            elif data[item]["status"] == TestRailResult.UNTESTED.value:
                skip_count += 1
        return pass_count, fail_count, skip_count
