import os
import pickle
from logging import Logger
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


def get_credentials(
    app_name: str,
    scopes: List[str],
    logger: Logger,
) -> Credentials:
    token = os.path.expanduser(f"~/.config/{app_name}/token.pickle")
    client_secret = os.path.expanduser(f"~/.config/{app_name}/client_secret.json")
    credentials = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.access(token, os.R_OK):
        with open(token, "rb") as token:
            credentials = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret, scopes,
            )
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        logger.info("creating a new token file")
        if os.access(token, os.R_OK):
            os.unlink(token)
        with open(token, "wb") as token_stream:
            pickle.dump(credentials, token_stream)
        os.chmod(token, 0o400)
    return credentials
