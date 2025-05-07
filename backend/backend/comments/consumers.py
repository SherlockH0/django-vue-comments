import logging
from typing import Any, Literal, TypedDict

from asgiref.typing import WebSocketScope
from channels.consumer import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import BaseChannelLayer
from rest_framework import serializers

from .services import create_comment

logger = logging.getLogger(__name__)


class UrlRoute(TypedDict):
    args: tuple[str | int, ...]
    kwargs: dict[str, str | int]


class ChannelsWebSocketScope(WebSocketScope):
    url_route: UrlRoute


class Event(TypedDict):
    type: Literal["comments.comment"]
    comment: dict[str, Any]


class Message(TypedDict):
    comment: dict[str, Any]


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
        try:
            data = await database_sync_to_async(create_comment)(content["comment"])

            message: Event = {
                "type": "comments.comment",
                "comment": data,
            }

            await self.channel_layer.group_send(self.room_group_name, message)
        except serializers.ValidationError as error:
            await self.send_json(content={"type": "error", "body": error.detail})
        except Exception as error:
            logger.error(error)

    async def comments_comment(self, event: Event) -> None:
        await self.send_json(content={"type": "comment", "body": event["comment"]})
