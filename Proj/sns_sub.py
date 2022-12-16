import json
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class SnsWrapper:
    def __init__(self):
        self.sns_resource = boto3.client('sns')
        self.topic_arn = 'arn:aws:sns:us-east-1:494505086554:Course_System'

    def subscribe(self, protocol, endpoint):
        """
        Subscribes an endpoint to the topic. Some endpoint types, such as email,
        must be confirmed before their subscriptions are active. When a subscription
        is not confirmed, its Amazon Resource Number (ARN) is set to
        'PendingConfirmation'.
        :param protocol: The protocol of the endpoint, such as 'sms' or 'email'.
        :param endpoint: The endpoint that receives messages, such as a phone number
                         (in E.164 format) for SMS messages, or an email address for
                         email messages.
        """
        if protocol == 'email':
            subs_iter = self.sns_resource.list_subscriptions_by_topic(TopicArn=self.topic_arn)
            for sub in subs_iter['Subscriptions']:
                if sub['SubscriptionArn'] == 'PendingConfirmation':
                    continue
                if sub['Endpoint'] == endpoint:
                    return
            self.sns_resource.subscribe(TopicArn=self.topic_arn,
                                        Protocol='email',
                                        Endpoint=endpoint,
                                        ReturnSubscriptionArn=False)
            logger.info("A new user has been added, please check his/her email and confirm the subscription")

    def publish_msg(self, message):
        """
        Publishes a message to a topic.
        :param message: The message to publish.
        """
        self.sns_resource.publish(TopicArn=self.topic_arn,
                                  Message=message)
        logger.info("The user should receive an email. The developers should get a slack message")

    def list_topics(self):
        """
        Lists topics for the current account.
        :return: An iterator that yields the topics.
        """
        try:
            topics_iter = self.sns_resource.list_topics()
            logger.info("Got topics.")
        except ClientError:
            logger.exception("Couldn't get topics.")
            raise
        else:
            return topics_iter

    def list_subscriptions(self, topic=None):
        """
        Lists subscriptions for the current account, optionally limited to a
        specific topic.
        :param topic: When specified, only subscriptions to this topic are returned.
        :return: An iterator that yields the subscriptions.
        """
        try:
            if topic is None:
                subs_iter = self.sns_resource.list_subscriptions()
            else:
                subs_iter = self.sns_resource.list_subscriptions_by_topic(TopicArn=topic)
            logger.info("Got subscriptions.")
        except ClientError:
            logger.exception("Couldn't get subscriptions.")
            raise
        else:
            return subs_iter


if __name__ == '__main__':
    email_address = 'jt3302@columbia.edu'
    msg = "Hello! This message is used to test whether this function works."
    sns_wrapper = SnsWrapper()
    sns_wrapper.subscribe('email', email_address)
    sns_wrapper.publish_msg(msg)
    logger.info("The user should receive an email. The developers should get a slack message")
    # sub_iter = sns_wrapper.list_subscriptions(sns_wrapper.topic_arn)
    # print(sub_iter)
    # print(sns_wrapper.list_topics())

