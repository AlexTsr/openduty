
__author__ = 'deathowl'

import smtplib
from django.template.defaultfilters import truncatechars

class EmailNotifier:
    def __init__(self, config):
        self.__config = config
    def notify(self, notification):
        smtp_user = self.__config['user']
        smtp_pwd = self.__config['password']
        smtp_host = self.__config['host']
        smtp_port = self.__config['port']
        truncate_length = int(self.__config.get('max_subject_length', 100))
        FROM = self.__config['from']
        TO = [notification.user_to_notify.email]
        try:
            SUBJECT = "Openduty Incident Report - {0}".format(notification.incident.description)
        except:
            SUBJECT = notification.message
        if truncate_length:
            SUBJECT = truncatechars(SUBJECT, truncate_length)
        TEXT =  notification.message
        try:
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
            server.ehlo()
            server.login(smtp_user, smtp_pwd)
            server.sendmail(FROM, TO, TEXT)
            server.close()
            print 'successfully sent the mail'
        except:
            print "failed to send mail"
