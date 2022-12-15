import json
import logging
import boto3
import time
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class SnsWrapper:
    def __init__(self):
        self.sns_resource = boto3.client('sns')
        self.email = ''
        self.email_seen = []
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
            self.email = endpoint
            if endpoint not in self.email_seen:
                self.email_seen.append(endpoint)
                self.sns_resource.subscribe(TopicArn=self.topic_arn,
                                            Protocol='email',
                                            Endpoint=endpoint,
                                            ReturnSubscriptionArn=False)

    def publish_msg(self, message):
        """
        Publishes a message to a topic.
        :param message: The message to publish.
        """
        self.sns_resource.publish(TopicArn=self.topic_arn,
                                  Message=message)

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
                # subs_iter = self.sns_resource.subscriptions.all()
                subs_iter = self.sns_resource.list_subscriptions()
            else:
                subs_iter = self.sns_resource.list_subscriptions_by_topic(topic=topic)
            logger.info("Got subscriptions.")
        except ClientError:
            logger.exception("Couldn't get subscriptions.")
            raise
        else:
            return subs_iter


# class SnsWrapper:
#     """Encapsulates Amazon SNS topic and subscription functions."""
#     def __init__(self, sns_resource):
#         """
#         :param sns_resource: A Boto3 Amazon SNS resource.
#         """
#         self.sns_resource = sns_resource
#         self.email_address = ''
#         self.phone_number = ''
#         self.lambda_function = ''
#         self.message_content = ''
#
#     def create_topic(self, name):
#         """
#         Creates a notification topic.
#         :param name: The name of the topic to create.
#         :return: The newly created topic.
#         """
#         try:
#             topic = self.sns_resource.create_topic(Name=name)
#             logger.info("Created topic %s with ARN %s.", name, topic.arn)
#         except ClientError:
#             logger.exception("Couldn't create topic %s.", name)
#             raise
#         else:
#             return topic
#
#     def list_topics(self):
#         """
#         Lists topics for the current account.
#         :return: An iterator that yields the topics.
#         """
#         try:
#             topics_iter = self.sns_resource.topics.all()
#             logger.info("Got topics.")
#         except ClientError:
#             logger.exception("Couldn't get topics.")
#             raise
#         else:
#             return topics_iter
#
#     @staticmethod
#     def delete_topic(topic):
#         """
#         Deletes a topic. All subscriptions to the topic are also deleted.
#         """
#         try:
#             topic.delete()
#             logger.info("Deleted topic %s.", topic.arn)
#         except ClientError:
#             logger.exception("Couldn't delete topic %s.", topic.arn)
#             raise
#
#     @staticmethod
#     def subscribe(topic, protocol, endpoint):
#         """
#         Subscribes an endpoint to the topic. Some endpoint types, such as email,
#         must be confirmed before their subscriptions are active. When a subscription
#         is not confirmed, its Amazon Resource Number (ARN) is set to
#         'PendingConfirmation'.
#         :param topic: The topic to subscribe to.
#         :param protocol: The protocol of the endpoint, such as 'sms' or 'email'.
#         :param endpoint: The endpoint that receives messages, such as a phone number
#                          (in E.164 format) for SMS messages, or an email address for
#                          email messages.
#         :return: The newly added subscription.
#         """
#         try:
#             subscription = topic.subscribe(
#                 Protocol=protocol, Endpoint=endpoint, ReturnSubscriptionArn=True)
#             logger.info("Subscribed %s %s to topic %s.", protocol, endpoint, topic.arn)
#         except ClientError:
#             logger.exception(
#                 "Couldn't subscribe %s %s to topic %s.", protocol, endpoint, topic.arn)
#             raise
#         else:
#             return subscription
#
#     def list_subscriptions(self, topic=None):
#         """
#         Lists subscriptions for the current account, optionally limited to a
#         specific topic.
#         :param topic: When specified, only subscriptions to this topic are returned.
#         :return: An iterator that yields the subscriptions.
#         """
#         try:
#             if topic is None:
#                 subs_iter = self.sns_resource.subscriptions.all()
#             else:
#                 subs_iter = topic.subscriptions.all()
#             logger.info("Got subscriptions.")
#         except ClientError:
#             logger.exception("Couldn't get subscriptions.")
#             raise
#         else:
#             return subs_iter
#
#     @staticmethod
#     def add_subscription_filter(subscription, attributes):
#         """
#         Adds a filter policy to a subscription. A filter policy is a key and a
#         list of values that are allowed. When a message is published, it must have an
#         attribute that passes the filter or it will not be sent to the subscription.
#         :param subscription: The subscription the filter policy is attached to.
#         :param attributes: A dictionary of key-value pairs that define the filter.
#         """
#         try:
#             att_policy = {key: [value] for key, value in attributes.items()}
#             subscription.set_attributes(
#                 AttributeName='FilterPolicy', AttributeValue=json.dumps(att_policy))
#             logger.info("Added filter to subscription %s.", subscription.arn)
#         except ClientError:
#             logger.exception(
#                 "Couldn't add filter to subscription %s.", subscription.arn)
#             raise
#
#     @staticmethod
#     def delete_subscription(subscription):
#         """
#         Unsubscribes and deletes a subscription.
#         """
#         try:
#             subscription.delete()
#             logger.info("Deleted subscription %s.", subscription.arn)
#         except ClientError:
#             logger.exception("Couldn't delete subscription %s.", subscription.arn)
#             raise
#
#     def publish_text_message(self, phone_number, message):
#         """
#         Publishes a text message directly to a phone number without need for a
#         subscription.
#         :param phone_number: The phone number that receives the message. This must be
#                              in E.164 format. For example, a United States phone
#                              number might be +12065550101.
#         :param message: The message to send.
#         :return: The ID of the message.
#         """
#         try:
#             response = self.sns_resource.meta.client.publish(
#                 PhoneNumber=phone_number, Message=message)
#             message_id = response['MessageId']
#             logger.info("Published message to %s.", phone_number)
#         except ClientError:
#             logger.exception("Couldn't publish message to %s.", phone_number)
#             raise
#         else:
#             return message_id
#
#     @staticmethod
#     def publish_message(topic, message, attributes):
#         """
#         Publishes a message, with attributes, to a topic. Subscriptions can be filtered
#         based on message attributes so that a subscription receives messages only
#         when specified attributes are present.
#         :param topic: The topic to publish to.
#         :param message: The message to publish.
#         :param attributes: The key-value attributes to attach to the message. Values
#                            must be either `str` or `bytes`.
#         :return: The ID of the message.
#         """
#         try:
#             att_dict = {}
#             for key, value in attributes.items():
#                 if isinstance(value, str):
#                     att_dict[key] = {'DataType': 'String', 'StringValue': value}
#                 elif isinstance(value, bytes):
#                     att_dict[key] = {'DataType': 'Binary', 'BinaryValue': value}
#             response = topic.publish(Message=message, MessageAttributes=att_dict)
#             message_id = response['MessageId']
#             logger.info(
#                 "Published message with attributes %s to topic %s.", attributes,
#                 topic.arn)
#         except ClientError:
#             logger.exception("Couldn't publish message to topic %s.", topic.arn)
#             raise
#         else:
#             return message_id
#
#     @staticmethod
#     def publish_multi_message(
#             topic, subject, default_message, sms_message, email_message):
#         """
#         Publishes a multi-format message to a topic. A multi-format message takes
#         different forms based on the protocol of the subscriber. For example,
#         an SMS subscriber might receive a short, text-only version of the message
#         while an email subscriber could receive an HTML version of the message.
#         :param topic: The topic to publish to.
#         :param subject: The subject of the message.
#         :param default_message: The default version of the message. This version is
#                                 sent to subscribers that have protocols that are not
#                                 otherwise specified in the structured message.
#         :param sms_message: The version of the message sent to SMS subscribers.
#         :param email_message: The version of the message sent to email subscribers.
#         :return: The ID of the message.
#         """
#         try:
#             message = {
#                 'default': default_message,
#                 'sms': sms_message,
#                 'email': email_message
#             }
#             response = topic.publish(
#                 Message=json.dumps(message), Subject=subject, MessageStructure='json')
#             message_id = response['MessageId']
#             logger.info("Published multi-format message to topic %s.", topic.arn)
#         except ClientError:
#             logger.exception("Couldn't publish message to topic %s.", topic.arn)
#             raise
#         else:
#             return message_id
#
# class Test_sns:
#     def __init__(self):
#         email = 'jt3302@columbia.edu'
#         phone_number = '+19177423181'
#         phone_sub = None
#
#         sns_wrapper = SnsWrapper(boto3.resource('sns'))
#         sns_wrapper.email_address = 'jt3302@columbia.edu'
#         sns_wrapper.phone_number = '+19177423181'
#
#         topic_name = f'Course_System-{time.time_ns()}'
#         print(f"Creating topic {topic_name}.")
#         topic = sns_wrapper.create_topic(topic_name)
#
#         if phone_number != '':
#             print(f"Subscribing {phone_number} to {topic_name}. Phone numbers do not "
#                   f"require confirmation.")
#             phone_sub = sns_wrapper.subscribe(topic, 'sms', phone_number)
#             print(f"Sending an SMS message directly from SNS to {phone_number}.")
#             sns_wrapper.publish_text_message(phone_number, 'Hello from the SNS demo!')
#
#         if sns_wrapper.email_address != '':
#             print(f"Subscribing {email}.")
#             email_sub = sns_wrapper.subscribe(topic, 'email', email)
#             # answer = input(
#             #     f"Confirmation email sent to {email}. To receive SNS messages, "
#             #     f"follow the instructions in the email. When confirmed, press "
#             #     f"Enter to continue.")
#             # while (email_sub.attributes['PendingConfirmation'] == 'true'
#             #        and answer.lower() != 's'):
#             #     answer = input(
#             #         f"Email address {email} is not confirmed. Follow the "
#             #         f"instructions in the email to confirm and receive SNS messages. "
#             #         f"Press Enter when confirmed or enter 's' to skip. ")
#             #     email_sub.reload()
#
#         if phone_sub is not None:
#             mobile_key = 'mobile'
#             friendly = 'friendly'
#             print(f"Adding a filter policy to the {phone_number} subscription to send "
#                   f"only messages with a '{mobile_key}' attribute of '{friendly}'.")
#             sns_wrapper.add_subscription_filter(phone_sub, {mobile_key: friendly})
#             print(f"Publishing a message with a {mobile_key}: {friendly} attribute.")
#             sns_wrapper.publish_message(
#                 topic, "Hello! This message is used to test whether this function works.", {mobile_key: friendly})
#             not_friendly = 'not-friendly'
#             print(f"Publishing a message with a {mobile_key}: {not_friendly} attribute.")
#             sns_wrapper.publish_message(
#                 topic,
#                 "Hey. THANK YOU SNS without lambda test clear :)",
#                 {mobile_key: not_friendly})
#
#         print(f"Getting subscriptions to {topic_name}.")
#         topic_subs = sns_wrapper.list_subscriptions(topic)
#         for sub in topic_subs:
#             print(f"{sub.arn}")
#
#         print(f"Deleting subscriptions and {topic_name}.")
#         for sub in topic_subs:
#             if sub.arn != 'PendingConfirmation':
#                 sns_wrapper.delete_subscription(sub)
#         sns_wrapper.delete_topic(topic)


# def test_all():
#     sns_wrapper = SnsWrapper(boto3.client('sns'))
#     sns_wrapper.email_address = 'jt3302@columbia.edu'
#     sns_wrapper.phone_number = '+19177423181'
#     topic_arn = 'arn:aws:sns:us-east-1:494505086554:Course_System'
# #   add subscription
#     email_sub = sns_wrapper.sns_resource.subscribe(TopicArn=topic_arn,
#                                                    Protocol='email',
#                                                    Endpoint=sns_wrapper.email_address,
#                                                    ReturnSubscriptionArn=True)
#     phone_sub = sns_wrapper.sns_resource.subscribe(TopicArn=topic_arn,
#                                                    Protocol='sms',
#                                                    Endpoint=sns_wrapper.phone_number,
#                                                    ReturnSubscriptionArn=True)
#     sns_wrapper.sns_resource.publish(TopicArn=topic_arn,
#                                     Message="Hello! This message is used to test whether this function works.")
    # sns_wrapper.publish_message(
    #     topic, "Hello! This message is used to test whether this function works.", {mobile_key: friendly})


if __name__ == '__main__':
    email_address = 'jt3302@columbia.edu'
    msg = "Hello! This message is used to test whether this function works."
    sns_wrapper = SnsWrapper()
    sns_wrapper.subscribe('email', email_address)
    sns_wrapper.publish_msg(msg)
    sub_iter = sns_wrapper.list_subscriptions(sns_wrapper.topic_arn)
    print(sub_iter)

