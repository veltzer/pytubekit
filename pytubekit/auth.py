import hashlib
import os
import pickle
from logging import Logger
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


def scopes_md5(scopes: List[str]) -> str:
    all_string = ",".join(scopes)
    m = hashlib.md5(all_string.encode())
    return m.hexdigest()


def get_credentials(
    app_name: str,
    scopes: List[str],
    logger: Logger,
) -> Credentials:
    credentials = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    md5_of_scopes = scopes_md5(scopes)
    token_filename = os.path.expanduser(f"~/.config/google_tokens/token-{md5_of_scopes}.pickle")
    if os.access(token_filename, os.R_OK):
        with open(token_filename, "rb") as token_stream:
            credentials = pickle.load(token_stream)
    # If there are no (valid) credentials available, let the user log in.
    if credentials is None or not credentials.valid:
        if credentials is not None:
            if credentials.expired and credentials.refresh_token:
                logger.debug("refreshing credentials")
                credentials.refresh(Request())
            else:
                pass
        else:
            client_secret = os.path.expanduser(f"~/.config/{app_name}/client_secret.json")
            if not os.path.isfile(client_secret):
                raise IOError(f"missing client secret file {client_secret} for application {app_name}")
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret, scopes,
            )
            credentials = flow.run_local_server(port=0)
        # Save the token for the next run
        logger.debug(f"creating a new token file {token_filename}")
        if os.access(token_filename, os.R_OK):
            os.unlink(token_filename)
        with open(token_filename, "wb") as token_stream:
            pickle.dump(credentials, token_stream)
        os.chmod(token_filename, 0o400)
    return credentials
