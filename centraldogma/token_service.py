from http import HTTPStatus
from typing import List

from pydantic import TypeAdapter

from centraldogma.base_client import BaseClient
from centraldogma.data import Token, CreatedToken


class TokenService:
    def __init__(self, client: BaseClient):
        self.client = client

    def create(self, app_id: str, is_admin: bool = False):
        handler = {HTTPStatus.CREATED: lambda resp: CreatedToken.from_dict(resp.json())}
        return self.client.request(
            "post",
            f"/tokens",
            data={"appId": app_id, "isAdmin": is_admin},
            handler=handler,
        )

    def deactivate(self, app_id: str):
        handler = {HTTPStatus.OK: lambda resp: None}
        return self.client.request(
            "patch",
            f"/tokens/{app_id}",
            json=[{"op": "replace", "path": "/status", "value": "inactive"}],
            handler=handler,
        )

    def delete(self, app_id: str):
        handler = {HTTPStatus.NO_CONTENT: lambda resp: None}
        return self.client.request("delete", f"/tokens/{app_id}", handler=handler)

    def list(self) -> List[Token]:
        handler = {
            HTTPStatus.OK: lambda resp: TypeAdapter(List[Token]).validate_json(
                resp.content
            )
        }
        return self.client.request("get", "/tokens", handler=handler)
