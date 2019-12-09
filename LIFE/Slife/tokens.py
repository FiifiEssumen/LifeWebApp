from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from datetime import datetime

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self,user):
        return (
            six.text_type(user.id) + six.text_type(datetime) + six.text_type(user.is_active)
            # six.text_type(user.id) + six.text_type(timestamp) + six.text_type(user.is_active) the timestamp was removed cos it gives error

        )

        activation_token = TokenGenerator()