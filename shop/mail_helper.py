from django.conf import settings
from django.core.mail.message import (
    DEFAULT_ATTACHMENT_MIME_TYPE, BadHeaderError, EmailMessage,
    EmailMultiAlternatives, SafeMIMEMultipart, SafeMIMEText,
    forbid_multi_line_headers, make_msgid,
)

def user_query_mail(username,msgHtml, msgTxt, reply_to):
    try:
        msg = EmailMultiAlternatives(
            'Django Query: '+username,
            msgTxt,
            username+" <"+reply_to+">",
            [settings.EMAIL_HOST_USER, ],
            reply_to =[reply_to],
            headers = {'Message-ID': 'foo'},
        )
        msg.attach_alternative(msgHtml, "text/html")
        # msg.send()
    except BadHeaderError:
        return {'success': 0,'error': 1, 'msg':'Invalid header found.'}
    return {'success': 1,'error': 0, 'msg':'Mail sent.'}