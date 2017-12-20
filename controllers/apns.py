from flask import Blueprint, request, jsonify
from utils import has_uuid, Error
from models import Apns
from shared import db

apns = Blueprint('apns', __name__)

@apns.route("/apns", methods=["POST"])
@has_uuid
def apns_register(client):
    '''This is called in iPushjet's
    application:didRegisterForRemoteNotificationsWithDeviceToken: override.

    We send the UUID along, which PushJet uses for everything internally.
    However, the (variable length) token that Apple sends us is what we must
    send notifs to later on.

    In other words, the handshake looks like this:
      1. The iDevice registers with Apple
      2. When (1) is successful, the device hits this endpoint and sends its
         UUID along with the token it received from Apple in (1).
      3. Both are stored in the `apns` table.

    When subscribing to something, we look attach the subscription to the UUID.

    When sending, we grab all UUIDs subscribed, then key on them to map them to
    device_tokens which get sent to.

    This is basically the same way the GCM one works, except that it's documented.
    '''
    token = request.form.get('device_token', False)

    if not token:
        return Error.ARGUMENT_MISSING('device_token')
    regs = Apns.query.filter_by(uuid=client).all()
    for u in regs:
        db.session.delete(u)
    reg = Apns(client, token)
    db.session.add(reg)
    db.session.commit()
    return Error.NONE


@apns.route("/apns", methods=["DELETE"])
@has_uuid
def apns_unregister(client):
    regs = Apns.query.filter_by(uuid=client).all()
    for u in regs:
        db.session.delete(u)
    db.session.commit()
    return Error.NONE
