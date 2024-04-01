from typing import Literal, Optional, Union, List
from typing_extensions import TypedDict


class ChatCompletionRequestSystemMessage(TypedDict):
    role: Literal["system"]
    content: str


class ChatCompletionRequestUserMessage(TypedDict):
    role: Literal["user"]
    content: str


class ChatCompletionRequestAssistantMessage(TypedDict):
    role: Literal["assistant"]
    content: str


ChatCompletionRequestMessage = List[Union[
    ChatCompletionRequestSystemMessage,
    ChatCompletionRequestUserMessage,
    ChatCompletionRequestAssistantMessage]]
