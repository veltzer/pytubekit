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


def ensure_folder(filename: str) -> None:
    folder = os.path.dirname(filename)
    if not os.path.exists(folder):
        os.makedirs(os.path.dirname(filename))


def get_credentials(
    app_name: str,
    scopes: List[str],
    logger: Logger,
    host: str,
    port: int,
    authorization_prompt_message: str,
    force: bool = False,
) -> Credentials:
    """
    The file token.pickle stores the user's access and refresh tokens, and is
    created automatically when the authorization flow completes for the first
    time.
    """
    credentials = None
    md5_of_scopes = scopes_md5(scopes)
    token_filename = os.path.expanduser(f"~/.config/google_tokens/token-{md5_of_scopes}.pickle")
    logger.debug(f"reading credentials from [{token_filename}]")
    if force:
        if os.access(token_filename, os.R_OK):
            os.unlink(token_filename)
    if os.access(token_filename, os.R_OK):
        with open(token_filename, "rb") as token_stream:
            credentials = pickle.load(token_stream)
    if credentials is None or not credentials.valid:
        if credentials is not None:
            if credentials.expired and credentials.refresh_token:
                logger.debug("refreshing credentials")
                credentials.refresh(Request())
        else:
            client_secret = os.path.expanduser(f"~/.config/{app_name}/client_secret.json")
            if not os.path.isfile(client_secret):
                raise IOError(f"missing client secret file [{client_secret}] for application [{app_name}]")
            logger.debug(f"creating credentials from client secret at {client_secret}")
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret, scopes,
            )
            credentials = flow.run_local_server(
                host=host,
                port=port,
                authorization_prompt_message=authorization_prompt_message,
            )
        logger.debug(f"creating a new token file [{token_filename}]")
        # there is a need to remove the old file if it exists since we chmod them so we can't overwrite them
        if os.access(token_filename, os.R_OK):
            os.unlink(token_filename)
        ensure_folder(token_filename)
        with open(token_filename, "wb") as token_stream:
            os.fchmod(token_stream.fileno(), 0o400)
            pickle.dump(credentials, token_stream)
    else:
        logger.debug(f"have valid credentials in [{token_filename}]")
    return credentials
