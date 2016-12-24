# -*- coding: utf-8 -*-
from zerver.lib.test_classes import WebhookTestCase

class MessengerHookTests(WebhookTestCase):
    STREAM_NAME = 'messenger'
    URL_TEMPLATE = u"/api/v1/external/messenger?stream={stream}&api_key={api_key}"
    FIXTURE_DIR_NAME = 'messenger'

    def test_message_sent(self):
        # type: () -> None
        expected_subject = 'CAT_WORLD'
        expected_message = (u"A message was sent to John Appleseed from CAT_WORLD\n>[image](https://static.xx.fbcdn.net/rsrc.php/v3/yc/r/xFmW1tcxsyL.png)")
        self.send_and_test_stream_message('message_sent',
                                          expected_subject, expected_message)

    def test_message_received(self):
        # type: () -> None
        expected_subject = 'PAGE_ID'
        expected_message = (u"PAGE_ID has received a new message from USER_ID:\n>[image](IMAGE_URL)")
        self.send_and_test_stream_message('message_received',
                                          expected_subject, expected_message)
