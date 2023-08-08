from aws_lambda_powertools import Logger
from requests.sessions import RequestsCookieJar
from src.srp.aws_srp import AWSSRP
from typing import Dict, Tuple
import json
import re
import requests


COGNITO_CLIENT_ID = "4mbpjh0cd78jbbu5kc5i9717v"
USER_POOL_ID = "us-east-1_iu3YTdfT3"

ROOT_DOMAIN = "https://hub.reinvent.awsevents.com"
ATTENDEE_PORTAL_URL = f"{ROOT_DOMAIN}/attendee-portal/"
SESSIONS_URL = f"{ROOT_DOMAIN}/attendee-portal-api/sessions/list/"
GET_COOKIES_URL = (
    "https://hub.reinvent.awsevents.com/auth/login/cognito/?code={code}&state={state}"
)
STORAGE_URL = "https://28ym3tywek.execute-api.us-east-1.amazonaws.com/storage"
REDACT_LOGS = True


logger = Logger()


def call_attendee_portal_url(session: requests.Session) -> str:
    logger.debug(f"Calling Attendee Portal URL: {ATTENDEE_PORTAL_URL}")
    response = session.get(
        ATTENDEE_PORTAL_URL,
        allow_redirects=False,
        headers={
            "accept-encoding": "deflate, gzip",
            "authority": "hub.reinvent.awsevents.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-ch-ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        },
    )

    if response.status_code != 302:
        raise Exception(
            f"Response status code should be 302, but is {response.status_code}"
        )

    if "Location" not in response.headers:
        raise Exception("Response should have Location header")

    redirect_location = response.headers["Location"]

    # if the redirect location is a relative path, prepend the root domain
    if redirect_location.startswith("/"):
        redirect_location = ROOT_DOMAIN + redirect_location

    logger.debug(f" - Status code: {response.status_code}")
    logger.debug(f" - Redirect location: {redact(redirect_location)}")
    return redirect_location


def call_login_url(session: requests.Session, url) -> str:
    logger.debug(f"Calling login URL: {redact(url)}")
    response = session.get(
        url,
        allow_redirects=False,
    )

    if response.status_code != 302:
        raise Exception(
            f"Response status code should be 302, but is {response.status_code}"
        )

    if "Location" not in response.headers:
        raise Exception("Response should have Location header")

    redirect_location = response.headers["Location"]

    # if the redirect location is a relative path, prepend the root domain
    if redirect_location.startswith("/"):
        redirect_location = ROOT_DOMAIN + redirect_location

    logger.debug(f" - Status code: {response.status_code}")
    logger.debug(f" - Redirect location: {redact(redirect_location)}")
    return redirect_location


def call_authorize_url(session: requests.Session, url) -> Tuple[str, str]:
    logger.debug(f"Calling Authorize URL: {redact(url)}")
    response = session.get(
        url,
        allow_redirects=False,
    )

    if response.status_code != 302:
        raise Exception(
            f"Response status code should be 302, but is {response.status_code}"
        )

    if "Location" not in response.headers:
        raise Exception("Response should have Location header")

    redirect_location = response.headers["Location"]

    # if the redirect location is a relative path, prepend the root domain
    if redirect_location.startswith("/"):
        redirect_location = ROOT_DOMAIN + redirect_location

    logger.debug(f" - Status code: {response.status_code}")
    logger.debug(f" - Redirect location: {redact(redirect_location)}")

    redirect_uri_index = redirect_location.find("redirect_uri=") + len("redirect_uri=")
    redirect_uri = redirect_location[redirect_uri_index:]
    separators_pattern = r"[&\?]"

    # Split the string using the pattern
    tokens = re.split(separators_pattern, redirect_uri)
    for token in tokens:
        if token.startswith("authorization_code="):
            authorization_code = token[len("authorization_code=") :]
        if token.startswith("state="):
            state_code = token[len("state=") :]

    logger.debug(f" - authorization_code: {redact(authorization_code)}")
    logger.debug(f" - state_code: {redact(state_code)}")
    return authorization_code, state_code


def redact(string: str) -> str:
    if REDACT_LOGS:
        if string.startswith("https://") or string.startswith("http://"):
            query_index = string.find("?")
            # return just the url, not the query parameters
            if query_index != -1:
                return string[:query_index] + "?<<<query params redacted>>>"
            else:
                return string
        return "***"
    else:
        return string


def get_tokens(username: str, password: str) -> Tuple[str, str, str]:
    logger.debug(f"Getting cognito tokens")

    # Get tokens
    aws = AWSSRP(
        username=username,
        password=password,
        pool_id=USER_POOL_ID,
        client_id=COGNITO_CLIENT_ID,
        pool_region="us-east-1",
    )
    tokens = aws.authenticate_user()

    access_token = tokens["AuthenticationResult"]["AccessToken"]
    refresh_token = tokens["AuthenticationResult"]["RefreshToken"]
    id_token = tokens["AuthenticationResult"]["IdToken"]
    logger.debug(f" - access_token: {redact(access_token)}")
    logger.debug(f" - refresh_token: {redact(refresh_token)}")
    logger.debug(f" - id_token: {redact(id_token)}")

    return access_token, refresh_token, id_token


def perform_storage_call(
    session: requests.Session, authorization_code, access_token, refresh_token, id_token
) -> None:
    logger.debug(f"Calling Storage URL: {STORAGE_URL}")
    response = session.post(
        url=STORAGE_URL,
        headers={
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "pragma": "no-cache",
            "sec-ch-ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
        },
        data=json.dumps(
            {
                "authorization_code": authorization_code,
                "id_token": id_token,
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        ),
    )
    logger.debug(f" - Status code: {response.status_code}")


def get_cookies(
    session: requests.Session, authorization_code, state_code
) -> RequestsCookieJar:
    cookies_url = GET_COOKIES_URL.format(code=authorization_code, state=state_code)
    logger.debug(f"Cookies URL: {redact(cookies_url)}")
    response = session.get(
        cookies_url,
        allow_redirects=False,
        headers={
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-ch-ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-site",
            "upgrade-insecure-requests": "1",
        },
    )
    if response.status_code != 302:
        raise Exception(
            f"Response status code should be 302, but is {response.status_code}"
        )

    logger.debug(f" - Status code: {response.status_code}")

    return response.cookies


def fetch_sessions(username: str, password: str):
    session = requests.Session()
    attendee_portal_redirect_location = call_attendee_portal_url(session)
    login_redirect_location = call_login_url(session, attendee_portal_redirect_location)
    authorization_code, state_code = call_authorize_url(
        session, login_redirect_location
    )
    access_token, refresh_token, id_token = get_tokens(username, password)
    perform_storage_call(
        session, authorization_code, access_token, refresh_token, id_token
    )

    cookies = get_cookies(session, authorization_code, state_code)

    list_response = requests.get(SESSIONS_URL, cookies=cookies)
    sessions: Dict = list_response.json()["data"]
    return sessions
