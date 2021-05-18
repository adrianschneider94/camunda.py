from contextvars import ContextVar
from typing import Optional, Union

from pydantic import AnyUrl, BaseModel
from requests import Session


class CamundaApiContext(BaseModel):
    session: Session
    url: AnyUrl

    class Config:
        arbitrary_types_allowed = True


camunda_api_context: ContextVar[CamundaApiContext] = ContextVar('camunda_api_context')


def join_urls(*args):
    return "/".join(map(lambda x: str(x).strip("/"), args))


class Api(object):
    def __init__(self):
        super().__init__()

    def get(self, path: str, params: dict = None, timeout: int = None, headers: dict = None) \
            -> Optional[Union[dict, list]]:
        context = camunda_api_context.get()
        session = context.session

        url = join_urls(context.url, path)

        result = session.get(url, params=params, timeout=timeout, headers=headers)
        result.raise_for_status()

        if result.status_code != 204:
            return result.json()

    def post(self, path: str, params: dict = None, data: dict = None, timeout: int = None, headers: dict = None) \
            -> Optional[Union[dict, list]]:
        context = camunda_api_context.get()
        session = context.session

        if not params:
            params = {}

        if not data:
            data = {}

        url = join_urls(context.url, path)
        result = session.post(url, params=params, timeout=timeout, json=data, headers=headers)
        result.raise_for_status()
        if result.status_code != 204:
            return result.json()

    def delete(self, path: str, params: dict = None, timeout: int = None, headers: dict = None):
        context = camunda_api_context.get()
        session = context.session

        url = join_urls(context.url, path)

        result = session.delete(url, params=params, timeout=timeout, headers=headers)
        result.raise_for_status()

    def update(self, path: str, params: dict = None, data: dict = None, timeout: int = None, headers: dict = None):
        context = camunda_api_context.get()
        session = context.session

        if not params:
            params = {}

        if not data:
            data = {}

        url = join_urls(context.url, path)

        result = session.put(url, params=params, timeout=timeout, json=data, headers=headers)
        result.raise_for_status()

        if result.status_code != 204:
            return result.json()


api = Api()


def _use_api() -> Api:
    return api
