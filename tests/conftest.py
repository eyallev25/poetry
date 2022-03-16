import logging
import random
from time import sleep

import pytest

from .support import loggers

# # instantiate loggers
loggers.get_loggers()


# @pytest.fixture(scope="session")
# def fetch_api_key(authorization_data):
#     try:
#         response = LambdaInvoker.activate_lambda(
#             "WebhookSecretRetrieverLambda",
#             {"tenantId": "e2etenant"},
#             should_return_value=True,
#         )
#         api_key = response.get("key", "")
#         assert api_key
#         yield api_key
#     except:
#         pass
