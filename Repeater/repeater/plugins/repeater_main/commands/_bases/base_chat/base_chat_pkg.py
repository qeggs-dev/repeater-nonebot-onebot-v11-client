from typing import NoReturn, ClassVar
from itertools import chain

from ....logger import logger
from ....clients import ChatClient, ChatSendMsg, ChatResponse
from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....client_configs import storage_configs
from ....command_register import CommandPackage
from .message import SendMessage

class BaseChat(CommandPackage):
    cmd_type = CmdTypes.CHAT
    empty_exit: ClassVar[bool] = True
    no_input: ClassVar[bool] = False

    async def empty_message(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
    ):
        logger.warning("Message is empty")
        if self.empty_exit:
            send_msg.break_handler()
    
    async def parse_forward_msgs(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
    ) -> str:
        forward_msgs = await persona_info.get_forward_msgs()
        if forward_msgs:
            forward_msgs_text = persona_info.generates_text_from_messages_list(forward_msgs)
            message_text = f"Forwarded messages:\n{forward_msgs_text}\n\n---\n\n"
        else:
            message_text = ""
        
        return message_text
    
    @staticmethod
    async def open_file(
        persona_info: PersonaInfo
    ) -> tuple[list[str], list[str]]:
        not_open_files: list[str] = []
        reply_msgs_texts: list[str] = []

        for file_id in persona_info.get_file_ids():
            info = await persona_info.get_file_info(file_id)
            name = info.file_name
            size = int(info.file_size)

            if storage_configs.max_text_file_size is not None:
                if size > storage_configs.max_text_file_size:
                    logger.warning(
                        "File {name} is too large to open as text file",
                        name = name
                    )
                    not_open_files.append(name)
                    continue
            try:
                logger.info(
                    "Opening file {name}",
                    name = name
                )
                file_data = await persona_info.open_text_file(
                    info,
                    storage_configs.text_file_encoding
                )
                reply_msgs_text = f"[File {name}]\n[File Content Begin]{file_data}\n[File Content End]"
                reply_msgs_texts.append(reply_msgs_text)
            except UnicodeDecodeError:
                logger.warning(
                    "File {name} was not opened",
                    name = name
                )
                not_open_files.append(file_id)
        
        return reply_msgs_texts, not_open_files

    async def parse_input(self, persona_info: PersonaInfo, send_msg: SendMsg, input_text: str) -> tuple[str, list[str], list[str], list[str], list[str]]:
        messages_text = await self.parse_forward_msgs(persona_info, send_msg)
        text = messages_text + input_text
        images: list[str] = await persona_info.get_images_url()
        audios: list[str] = persona_info.get_audio_url()
        videos: list[str] = persona_info.get_video_url()
        reply_msgs_texts, not_open_files = await self.open_file(persona_info)

        return (
            "\n".join(reply_msgs_texts) + text,
            images,
            audios,
            videos,
            not_open_files
        )
    
    async def post_parse_input_text(self, text: str) -> str:
        return text

    async def parse_message(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
    ) -> SendMessage:
        if self.no_input:
            return SendMessage()
        else:
            if not persona_info:
                await self.empty_message(persona_info, send_msg)
            
            (
                message_text,
                images,
                audios,
                videos,
                files
            ) = await self.parse_input(
                persona_info,
                send_msg,
                await self.post_parse_input_text(
                    persona_info.message_stripped_str
                )
            )

            reply_msgs_texts: list[str] = []
            reply_images_list: list[str] = []
            reply_audios_list: list[str] = []
            reply_videos_list: list[str] = []
            reply_files_list: list[str] = []
            
            reply_msgs = await persona_info.from_reference_reversed_chain()
            
            for msg in reply_msgs:
                if msg.is_self:
                    break

                (
                    reference_text,
                    reference_images,
                    reference_audios,
                    reference_videos,
                    reference_files
                ) = await self.parse_input(
                    msg,
                    send_msg,
                    msg.message_stripped_str
                )

                reply_msgs_texts.append(reference_text)
                reply_images_list.extend(reference_images)
                reply_audios_list.extend(reference_audios)
                reply_videos_list.extend(reference_videos)
                reply_files_list.extend(reference_files)
                

            reply_msgs_text = "\n\n".join(reply_msgs_texts)
            reply_msgs_text = "\n> " + reply_msgs_text.replace("\n", "\n> ")

            if any(reply_images_list):
                if message_text:
                    message_text = f"Reply messages:\n{reply_msgs_text}\n\n---\n\n{message_text}"
                else:
                    message_text = reply_msgs_text
            
            return SendMessage(
                text = message_text,
                images = images,
                audios = audios,
                videos = videos,
                files = files
            )

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        logger.info(
            "Received a message {message} from {namespace}",
            message = persona_info.message_stripped_str,
            namespace = persona_info.namespace_str,
            module = send_msg.component
        )
        
        message = await self.parse_message(persona_info, send_msg)

        client = await self.get_client(persona_info)

        response = await self.send_message(
            client = client,
            send_messages = message,
            persona_info = persona_info,
            send_msg = send_msg
        )

        if not response and response.initialized:
            await send_msg.send_error_response(
                response = response,
            )

        chat_send_msg = ChatSendMsg(
            component = send_msg.component,
            persona_info = persona_info,
            matcher = send_msg.matcher,
            response = response,
            reasoning_content_handler = self.reason_filters,
            content_handler = self.filters
        )
        await self.send_chat_send_msg(chat_send_msg)
    
    def filters(self, text: str) -> str:
        return text
    
    def reason_filters(self, text: str) -> str:
        return text
    
    async def get_client(self, persona_info: PersonaInfo) -> ChatClient:
        user_configs = await persona_info.get_user_configs()
        client = ChatClient(persona_info, user_configs)
        return client
    
    async def send_message(
        self,
        client: ChatClient,
        send_messages: SendMessage,
        persona_info: PersonaInfo,
        send_msg: SendMsg
    ) -> Response[ChatResponse]:
        response: Response[ChatResponse] = await client.send_message(
            message = send_messages.text,
            image_url = send_messages.images,
            audio_url = send_messages.audios,
            video_url = send_messages.videos,
            file_url = send_messages.files,
        )
        return response
    
    async def send_chat_send_msg(self, chat_send_msg: ChatSendMsg) -> NoReturn:
        await chat_send_msg.send()