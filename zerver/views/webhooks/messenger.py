# Webhooks for external integrations.
from __future__ import absolute_import

from django.utils.translation import ugettext as _
from django.http import HttpRequest, HttpResponse
from typing import Any

from zerver.lib.actions import check_send_message
from zerver.lib.response import json_success, json_error
from zerver.decorator import REQ, has_request_variables, api_key_only_webhook_view
from zerver.models import UserProfile, Client

import ujson

@api_key_only_webhook_view('Messenger')
@has_request_variables
def api_messenger_webhook(request, user_profile, client, payload=REQ(argument_type='body'),
                         stream=REQ(default='messenger')):
    # type: (HttpRequest, UserProfile, Client, Dict[str, Any], str) -> HttpResponse

    try:
        BODY_TEMPLATE, subject = get_message_subject_template(payload)
        body = BODY_TEMPLATE.format(**format_message(payload))
    except KeyError as e:
        return json_error(_("Missing key {} in JSON").format(str(e)))

    check_send_message(user_profile, client, 'stream', [stream], subject, body)
    return json_success()

def get_message_subject_template(payload):
    # type: (Dict[str, Any]) -> str
    if 'is_echo' in payload['message']:
        return 'A message was sent to {recipient} from {sender}\n>{message}', payload['sender']['id']
    else:
        return '{recipient} has received a new message from {sender}:\n>{message}', payload['recipient']['id']

def format_message(payload):
    # type: (Dict[str, Dict[str, Any]]) -> Dict[str, Any]
    result = {'recipient': payload['recipient']['id']}
    result['sender'] = payload['sender']['id']
    if 'text' in payload['message']:
        result['message'] = payload['message']['text']
    elif 'attachments' in payload['message']:
        attachments = payload['message']['attachments']
        for item in attachments:
            attachment_type = item['type']
            attachment_url = item['payload']['url']
            result['message'] = '[{name}]({link})'.format(name=attachment_type, link=attachment_url)
    return result
