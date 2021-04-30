import urllib.parse
import http.client
from .utils import utf8_bytes

class Request:
    def __init__(self, environ):
        self.environ = environ
        self.path = environ["PATH_INFO"]
        self.method = environ["REQUEST_METHOD"]

    @property
    def args(self):
        """
        :returns: Decoded dictionary version of the HTTP query's parameters
        (e.g localhost:/home... ?user=Admin) -> { "user": "Admin" }
        """

        parsed = urllib.parse.parse_qs(self.environ["QUERY_STRING"])

        # Multiple values can match the same key, we choose to get the first occurrence
        return {k:v[0] for k, v in parsed.items()}

class Response:
    def __init__(self, body=b'', status=200):
        self.body = body
        self._content_type = "text/html"
        self.headers = { "Content-Type": "text/html; charset=utf8" }
        self.status_code = status

    @property
    def content_type(self):
        return self._content_type

    @content_type.setter
    def content_type(self, value):
        """
        Setter for the request's content_type
        (This change will update the request's headers as well)
        """

        self._content_type = value
        self.headers["Content-Type"] = f"{value}; charset=utf-8"

    @property
    def status(self):
        """
        :returns: A string of the response's status consisting 
        of the status_code and a related string message
        (e.g "200 OK")
        """

        status_string = http.client.responses.get(self.status_code, "UNKNOWN STATUS")
        return f"{self.status_code} {status_string}"

    def __call__(self, environ, start_response):
        """
        Callable following the PEP333 WSGI standards

        :param environ: A dictionary containing request and server information
        :param start_response: A callable which accepts the status and the headers of the request 
        """

        start_response(self.status, self.headers.items())
        yield utf8_bytes(self.body)
