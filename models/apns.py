from flask import current_app
from shared import db
from sqlalchemy.dialects.mysql import INTEGER
from datetime import datetime
from config import apns_cert_path, apns_key_path
from models import Subscription, Message
from apns2.client import APNsClient
from apns2.payload import Payload

class Apns(db.Model):
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    uuid = db.Column(db.VARCHAR(40), nullable=False)
    device_token = db.Column(db.TEXT, nullable=False)
    timestamp_created = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def __init__(self, uuid, token):
        self.uuid = uuid
        self.device_token = token

    def __repr__(self):
        return '<Apns {}>'.format(self.uuid)

    def as_dict(self):
        data = {
            "uuid": self.service.as_dict(),
            "device_token": self.device_token,
            "timestamp": int((self.timestamp_created - datetime.utcfromtimestamp(0)).total_seconds()),
        }
        return data

    @staticmethod
    def send_message(message):
        """

        :type message: Message
        """
        subscriptions = Subscription.query.filter_by(service=message.service).all()
        if len(subscriptions) == 0:
            return 0
        apns_devices = Apns.query.filter(Apns.uuid.in_([l.device for l in subscriptions])).all()

        if len(apns_devices) > 0:
            Apns.apns_send([r.device_token for i in apns_devices], message.as_dict())
            uuids = [g.uuid for g in apns_devices]
            apns_subscriptions = Subscription.query.filter_by(service=message.service).filter(Subscription.device.in_(uuids)).all()
            last_message = Message.query.order_by(Message.id.desc()).first()
            for l in apns_subscriptions:
                l.timestamp_checked = datetime.utcnow()
                l.last_read = last_message.id if last_message else 0
            db.session.commit()
        return len(apns_devices)

    @staticmethod
    def apns_send(tokens, data):
        if current_app.config['TESTING'] is True:
            current_app.config['TESTING_APNS'].append(data)
            return
        payload = Payload(alert="Pushjet Notification", sound="default", badge=1)
        notifications = [Notification(token=token, payload=payload) for token in tokens]
        topic = 'me.elrod.iPushjet'
        client = APNsClient('key.pem', use_sandbox=False, use_alternative_port=False)
        client.send_notification_batch(notifications, topic)
