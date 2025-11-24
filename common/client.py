import enum
import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


class HttpMethods(enum.Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "del"

    @property
    def is_get(self):
        return self == HttpMethods.GET

    @property
    def is_post(self):
        return self == HttpMethods.POST

    @property
    def is_put(self):
        return self == HttpMethods.PUT

    @property
    def is_patch(self):
        return self == HttpMethods.PATCH

    @property
    def is_delete(self):
        return self == HttpMethods.DELETE


class BaseRequestClient:

    base_url = None
    user_token = None

    headers = {
        "Accept": "application/json",
        # "Content-Type": "multipart/form-data"
    }

    def __init__(self, retries=3, backoff_factor=0.3, status_force_list=(500, 502, 504, 429)):
        self.retries = retries
        self.backoff_factor = backoff_factor
        self.status_force_list = status_force_list

        self.session = self.get_session()

        self.logger = logging.getLogger("routing.client")

    def _get_url(self, endpoint:str, **kwargs):
        """Get url for endpoint."""
        return f"{self.base_url}{endpoint.format(**kwargs)}"

    def get_session(self):
        session = requests.Session()
        retry = Retry(
            total=self.retries,
            read=self.retries,
            connect=self.retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.status_force_list
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def get_default_headers(self):
        return self.headers.copy()

    def send(self, url: str, method: HttpMethods, data=None, params=None, headers=None):
        """Generic method for sending request.

        :param url The url to send request to.
        :param method The http method to use for request.
        :param data The data to use for POST request
        :param params The parameters to use for GET query parameters.
        :param headers: Extra headers to add to request.
        """
        try:
            # add logs
            self.logger.info(f"Sending {method.value.upper()} request to {url} with data {data} and parameters {params}")

            all_headers = self.get_default_headers()

            if headers:
                all_headers.update(headers)

            if method.is_get:
                response = self.session.get(
                    url,
                    headers=all_headers,
                    params=params,
                )
            elif method.is_post:
                response = self.session.post(
                    url,
                    headers=all_headers,
                    data=data,
                    params=params,
                )
            elif method.is_put:
                response = self.session.put(
                    url,
                    headers=all_headers,
                    data=data,
                    params=params,
                )
            elif method.is_patch:
                response = self.session.patch(
                    url,
                    headers=all_headers,
                    data=data,
                    params=params,
                )
            elif method.is_delete:
                response = self.session.delete(
                    url,
                    headers=all_headers,
                    params=params,
                )
            else:
                raise ValueError(f"Invalid method: {method}")

            response.raise_for_status()
            json_response = response.json()
            self.logger.info("Received response from %s. Response: %s", url, json_response)
            return json_response
        except requests.exceptions.RequestException as e:
            self.logger.error("Error sending request. Error: %s", e)
            if hasattr(e.response, 'text'):
                self.logger.error("Response: %s", e.response.text)
            raise e
        except Exception as e:
            self.logger.error("Error sending request. Error: %s", e)
            if hasattr(e, 'response') and e.response:
                self.logger.error("Response: %s", e.response.text)
            raise e

    def get(self, endpoint, params, headers=None,**kwargs):
        """Send GET request."""
        url = self._get_url(endpoint, **kwargs)
        return self.send(url, HttpMethods.GET, params=params)

    def post(self, endpoint, data, headers=None, **kwargs):
        """Send POST request."""
        url = self._get_url(endpoint, **kwargs)
        return self.send(url, HttpMethods.POST, data=data)
