from typing import Any, Literal, TypedDict

from asgiref.typing import WebSocketScope
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import BaseChannelLayer


class UrlRoute(TypedDict):
    args: tuple[str | int, ...]
    kwargs: dict[str, str | int]


class ChannelsWebSocketScope(WebSocketScope):
    url_route: UrlRoute


class ChatMessage(TypedDict):
    type: Literal["comments.comment"]
    comment: str


class Message(TypedDict):
    comment: str


class CommentsConsumer(AsyncJsonWebsocketConsumer):
    channel_layer: BaseChannelLayer

    async def connect(self) -> None:
        self.scope: ChannelsWebSocketScope = self.scope

        self.room_group_name = "comments"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code: int) -> None:
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive_json(self, content: Message, **kwargs: Any) -> None:
        message: ChatMessage = {
            "type": "comments.comment",
            "comment": content["comment"],
        }

        await self.channel_layer.group_send(self.room_group_name, message)

    async def chat_message(self, event: ChatMessage) -> None:
        message: Message = {
            "comment": event["comment"],
        }

        await self.send_json(content=message)
