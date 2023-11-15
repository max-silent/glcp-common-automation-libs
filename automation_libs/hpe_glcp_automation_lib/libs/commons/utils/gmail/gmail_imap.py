import email
import imaplib
import logging
import time
from builtins import range

import requests

log = logging.getLogger(__name__)

SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993
INBOX_FOLDER = "inbox"
TRASH_FOLDER = "[Gmail]/Trash"


class GmailOps:
    def __init__(self):
        # Intializing mail object
        self.mail = None

    def _gmail_login(self, username, password):
        # Login into Gmail Account
        self.mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        self.mail.login(username, password)
        self.mail.select(INBOX_FOLDER)
        log.info("Login into Gmail")

    def _gmail_logout(self):
        # Logout from Gmail Account
        self.mail.logout()
        log.info("Logout from Gmail")

    def read_email_from_gmail(self, to_mail_address_format="ALL", date_from=None):
        """
        This function helps to fetch unread email from Inbox
        :param to_mail_address_format: the id to which email is sent, formatted as '(TO "sample@mail.com")'
        :type to_mail_address_format: str
        :param date_from: the strf date from which email to be fetched, formatted as '(SENTSINCE {"25-may-2023"})'
        :type date_from: str
        :return: list of email data
        :rtype: list
        """
        # Read all the emails from Inbox
        email_to_list = []
        if date_from is None:
            type, data = self.mail.search(None, to_mail_address_format)
        else:
            type, data = self.mail.search(None, to_mail_address_format, date_from)
        mail_ids = data[0]
        id_list = mail_ids.split()
        latest_ten_email_id = id_list[::-1]
        keys = map(int, latest_ten_email_id)
        news_keys = sorted(keys, reverse=True)
        str_keys = [str(e) for e in news_keys]
        for i in str_keys:
            typ, data = self.mail.fetch(i, "(RFC822)")
            email_to = None
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(
                        response_part[1].decode("unicode_escape")
                    )
                    email_to = msg["to"]
            email_to_list.append({"email_to": email_to, "data": data, "message_id": i})
        return email_to_list

    def mark_mail_as_unread(self, message_id):
        log.info("******* Mark Unread Message ID: {} *******".format(message_id))
        return self.mail.store(message_id, "-FLAGS", "\\SEEN")

    def delete_the_mail(self, message_id):
        log.info("******* Delete Message ID: {} *******".format(message_id))
        return self.mail.store(message_id, "+FLAGS", "\\Deleted")

    def check_verification_mail_in_gmail_inbox(
        self, to_email, gmail_username, gmail_password, date_from=None
    ):
        # Check whether mail is received in Inbox for the user to_email
        response = None
        email_data = ""
        # loop for overall check email
        for i in range(5):
            # Login to gmail loop. If login fails, retry 2 more times
            for j in range(3):
                try:
                    self._gmail_login(username=gmail_username, password=gmail_password)
                    break
                except Exception as e:
                    log.exception(
                        "Unexpected error in logging in to gmail: {}. Sleeping 20 seconds and "
                        "retrying Login to gmail".format(e.args[0])
                    )
                    time.sleep(30)
                    continue

            to_mail_address_format = '(TO "{}")'.format(to_email)
            # Check in INBOX first
            email_to_list = self.read_email_from_gmail(to_mail_address_format, date_from)
            for mail in email_to_list:
                if to_email in mail["email_to"]:
                    log.info("******* Email Found for {} *******".format(to_email))
                    response = True
                    email_data = mail["data"]
                    log.info("Deleting the email for {}".format(to_email))
                    for k in range(3):
                        status, id = self.delete_the_mail(mail["message_id"])
                        if status == "OK":
                            log.debug(
                                "******* Deleting the email is successful - {} *******".format(
                                    to_email
                                )
                            )
                            break
                        else:
                            log.error(
                                "******* Deleting the email is not successful. Retry after 10 seconds - {} *******".format(
                                    to_email
                                )
                            )
                            time.sleep(30)
                            continue
                    return response, email_data
                else:
                    continue
            """
            log.warning('Email not found for {} in Inbox, checking in trash'.format(to_email))            
            # if mail is not found in inbox, switch to trash box and check there
            self.mail.select(TRASH_FOLDER)
            log.info('Switched to trash folder'.format(to_email))
            email_to_list_trash = self.read_email_from_gmail(to_mail_address_format)
            for mail in email_to_list_trash:
                if to_email in mail["email_to"]:
                    log.info('Email Found for {} in TRASH FOLDER'.format(to_email))
                    response = True
                    email_data = mail["data"]
                    return response, email_data
                else:
                    continue
            """
            log.warning(
                "******* Still email not found for {} in INBOX, trying again in 30 seconds *******".format(
                    to_email
                )
            )
            self._gmail_logout()
            time.sleep(30)
            continue
        return response, email_data

    def get_verification_hash(self, url):
        # As sendgrid has enabled click tracking, this function will be used to get the redirected url and
        # verification hash
        ver_hash = "None"
        try:
            requests.get(url)
        except Exception as e:
            str = e.__str__()
            str_list = str.split()
            for j in str_list:
                if j.__contains__("verification_hash="):
                    print(j)
                    hash = j.split("=")
                    ver_hash = hash[1]
            log.info("******* VERIFICATION HASH {} *******".format(ver_hash))
        return ver_hash

    def get_verification_link(
        self, my_email, gmail_username="hcloud203@gmail.com", gmail_password="aruba123"
    ):
        url_list = []
        verification_hash = "None"
        try:
            url = None
            response, data = self.check_verification_mail_in_gmail_inbox(
                my_email, gmail_username, gmail_password
            )

            if not response:
                raise Exception("Email not found for user: {}".format(my_email))
            # Unpacking email data and getting link
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(
                        response_part[1].decode("unicode_escape")
                    )
                    email_to = msg["to"]
                    if my_email in email_to:
                        email_body = data[0][1]  # getting the mail content
                        # raw_email_string = email_body.decode('utf-8' or 'ISO-2022' or 'UTF-16' or 'UTF-32'
                        #                                      or 'ISO-8859-8-i', errors='ignore')
                        raw_email_string = email_body.decode("UTF-8", errors="ignore")
                        # Converts byte literal to string removing b''
                        try:
                            email_message = email.message_from_string(raw_email_string)
                        except:
                            raw_email_string = email_body.decode("ascii", errors="ignore")
                            email_message = email.message_from_string(raw_email_string)
                        # This will loop through all the available multiparts in mail
                        for part in email_message.walk():
                            if (
                                part.get_content_type() == "text/html"
                                or part.get_content_type() == "text/plain"
                            ):  # ignore attachments/html
                                my_msg = part.get_payload(decode=True)
                                my_msg = my_msg.decode("unicode_escape")
                                t1 = my_msg.split()
                                for values in t1:
                                    if (
                                        "/onboarding/" in values
                                        and 'href="https:' in values
                                    ):
                                        url = values.split('"')[1]
                                        log.info(
                                            "******** URL from email is: {} *******".format(
                                                url
                                            )
                                        )
                                        split_url = url.split("=")
                                        verification_hash = split_url[1]
                                    elif "/click?" in values and 'href="https:' in values:
                                        url = values.split('"')[1]
                                        url_list.append(url)
                                        log.info(
                                            "******** URL from email is: {} *******".format(
                                                url
                                            )
                                        )
                                        if ">" or "</span>" in url:
                                            url = (
                                                values.split(">")
                                                and values.split("</span>")
                                                and values.split('"')[1]
                                            )
                                            url_list.append(url)
                                    elif "/click?" in values and '">https://' in values:
                                        url = values.split('">')[1]
                                        url_list.append(url)
                                        log.info(
                                            "******* URL from email is: {} *******".format(
                                                url
                                            )
                                        )
                                    elif "/click?" in values and values.split("https://"):
                                        url = values
                                        url_list.append(url)
                    else:
                        continue
            # This if block works only if SendGrid enables click tracking
            if verification_hash == "None":
                log.info(
                    "******* SendGrid URL with Verification Hash: {} *******".format(
                        url_list[0]
                    )
                )
                verification_hash = self.get_verification_hash(url_list[0])

            return verification_hash
        except Exception as e:
            log.exception(
                "Unexpected error in getting verification link from gmail: {}".format(
                    e.args[0]
                )
            )
            return "None"

    def _filter_email_for_report_url(self, email_message):
        """
        This will loop through all the available multiparts in mail
        :param email_message: the email message after unicode decoding
        :type email_message:
        :return: url
        :rtype: string
        """

        url = None
        for part in email_message.walk():
            if (
                part.get_content_type() == "text/html"
                or part.get_content_type() == "text/plain"
            ):  # ignore attachments/html
                my_msg = part.get_payload(decode=True)
                my_msg = my_msg.decode("unicode_escape")
                t1 = my_msg.split()
                for values in t1:
                    if ".csv" in values or ".txt" in values:
                        # url = re.findall(r'"https:[\S]+.csv"', values)[0]
                        url = values[6:-1]
                        log.info("******** URL from email is: {} *******".format(url))
                        break
                    elif "ct.sendgrid.net" in values:
                        sendgrid_url = values.split('href="')[1]
                        url = self.get_report_url_from_sendgrid_url(sendgrid_url[:-1])
                        break
        return url

    def get_report_url_from_sendgrid_url(self, sendgrid_url):
        url = requests.get(sendgrid_url).url
        return url

    def get_report_csv_download_link(
        self, my_email, gmail_username=None, gmail_password=None, date_from=None
    ):
        """
        This function waits for a Report Email and fetches the CSV download link
        :param my_email: Email to which the report is sent
        :type my_email: str
        :param gmail_username: Gmail username
        :type gmail_username: str
        :param gmail_password: Gmail password
        :type gmail_password: str
        :param date_from: THe ddate from which this needs to be checked
        :type date_from: strf_time.datetime
        :return: url link
        :rtype: str
        """
        try:
            url = None
            response, data = self.check_verification_mail_in_gmail_inbox(
                my_email, gmail_username, gmail_password, date_from
            )

            if not response:
                raise Exception("Email not found for user: {}".format(my_email))
            # Unpacking email data and getting link
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(
                        response_part[1].decode("unicode_escape")
                    )
                    email_to = msg["to"]
                    if my_email in email_to:
                        email_body = data[0][1]  # getting the mail content
                        # raw_email_string = email_body.decode('utf-8' or 'ISO-2022' or 'UTF-16' or 'UTF-32'
                        #                                      or 'ISO-8859-8-i', errors='ignore')
                        raw_email_string = email_body.decode("UTF-8", errors="ignore")
                        # Converts byte literal to string removing b''
                        try:
                            email_message = email.message_from_string(raw_email_string)
                        except:
                            raw_email_string = email_body.decode("ascii", errors="ignore")
                            email_message = email.message_from_string(raw_email_string)
                        # This will loop through all the available multiparts in mail
                        url = self._filter_email_for_report_url(email_message)
                        if url is not None:
                            break
                    else:
                        continue

            return url
        except Exception as e:
            log.exception(
                "Unexpected error in getting CSV link from gmail: {}".format(e.args[0])
            )
            return "None"


if __name__ == "__main__":
    gmail_session = GmailOps()
    verification_link = gmail_session.get_verification_link(
        my_email="ccsqa2020+prem1@gmail.com",
        gmail_username="ccsqa2020@gmail.com",
        gmail_password="Aruba@123",
    )
    log.info("Verification Link: {}".format(verification_link))
