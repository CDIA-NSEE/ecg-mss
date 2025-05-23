import json
from datetime import datetime

from pydantic import ValidationError
from typing import Optional, Dict, Any, Union

from core.entities import User


class HTTPRequest:
    body: Optional[Dict[str, str]]
    parms: Optional[Dict[str, str]]
    headers: Optional[Dict[str, str]]

    def __init__(self, event: dict, requested_user: Optional[User] = None):
        self.parms = event.get("queryStringParameters")
        self.body = json.loads(event.get("body")) if event.get("body") else None
        self.headers = event.get("headers")
        if self.headers and self.headers.get("Authorization"):
            self.headers["Authorization"] = self.headers.get("Authorization").replace("Bearer ", "")

    def __str__(self):
        return f"HttpRequest(parms={self.parms}, body={self.body}, headers={self.headers})"

    def __repr__(self):
        return str(self)


class HTTPResponse:
    def __init__(self, status_code: int, body: Optional[Dict[str, Any]] = None, message: Optional[str] = None):
        self.status_code = status_code
        self.body = body if body else {}
        self.message = message
        self.headers = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        }

    def to_dict(self):
        self.body["message"] = self.message
        return {
            "statusCode": self.status_code,
            "body": json.dumps(self.body) if self.body else None,
            "headers": self.headers
        }

    def __str__(self):
        return f"HTTPResponse(status_code={self.status_code}, body={self.body})"

    def __repr__(self):
        return str(self)


class HTTPError(HTTPResponse):
    def __init__(self, status_code: int, details: Optional[Union[ValueError, ValidationError, str]] = None):
        if not details:
            details = "An error occurred"
        elif isinstance(details, ValidationError):
            details = [{
                "field": err["loc"][0],
                "message": err["msg"]}
                for err in details.errors()]
        elif isinstance(details, ValueError):
            details = str(details)

        details = {"details": details}
        super().__init__(status_code, details)

        self.headers = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        }

    def __str__(self):
        return f"HTTPError(status_code={self.status_code}, message={self.body})"

    def __repr__(self):
        return str(self)
