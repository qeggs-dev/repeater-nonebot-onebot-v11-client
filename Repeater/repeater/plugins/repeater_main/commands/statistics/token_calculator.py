import time
import asyncio
from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from tokenizers import Tokenizer
from collections import Counter
from ...logger import logger
from cachetools import LRUCache
from ...client_configs import storage_configs

@CommandCaller.register
class TokenCalculator(CommandPackage):
    cmd = "tokenizer"
    aliases = {
        "tiz",
        "TIZ",
        "Tokenizer",
        "TOKENIZER"
    }
    cmd_type = CmdTypes.STATISTIC
    description = f"""
    Count tokens using tokenizer.

    Usage:
    (reply a tokenizer file)
    ```
    /{cmd} text
    ```
    """
    file_ids_cache: LRUCache[str, str] = LRUCache(maxsize=storage_configs.tokenizer_cache_size)
    cache: LRUCache[str, Tokenizer] = LRUCache(maxsize=storage_configs.tokenizer_cache_size)
    
    def init_tokenizer(self, json: str):
        if json in self.cache:
            tokenizer = self.cache[json]
        else:
            tokenizer = Tokenizer.from_str(json)
            self.cache[json] = tokenizer
        return tokenizer

    async def get_files(self, persona_info: PersonaInfo) -> list[str]:
        file_ids: list[str] = []
        file_ids.extend(persona_info.get_file_ids())
        for msg in await persona_info.from_reference_reversed_chain():
            file_ids.extend(msg.get_file_ids())
        return file_ids

    async def get_file_content(self, persona_info: PersonaInfo, send_msg: SendMsg) -> str:
        file_ids = await self.get_files(persona_info)
        if not file_ids:
            await send_msg.send_error("Need a tokenizer.json for reference.")
            send_msg.break_handler()
        elif len(file_ids) > 1:
            await send_msg.send_error("Only one tokenizer.json is allowed.")
            send_msg.break_handler()
        else:
            file_id = file_ids[0]
            if file_id in self.file_ids_cache:
                file_content = self.file_ids_cache[file_id]
            else:
                file_info = await persona_info.get_file_info(file_id)
                file_content = await persona_info.open_text_file(file_info)
                self.file_ids_cache[file_id] = file_content
            return file_content

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        file_content = await self.get_file_content(persona_info, send_msg)
            
        logger.info("Loading tokenizer...")
        init_start_time = time.perf_counter_ns()
        tokenizer = await asyncio.to_thread(
            self.init_tokenizer,
            json = file_content
        )
        init_end_time = time.perf_counter_ns()
        logger.info("Inited tokenizer in {init_time:.2f}ms.", init_time=(init_end_time - init_start_time) / 1e6)
        logger.info("Calculating tokens...")
        start_time = time.perf_counter_ns()
        tokens_encoding = tokenizer.encode(persona_info.message_stripped_str)
        counter = Counter(tokens_encoding.ids)
        end_time = time.perf_counter_ns()
        logger.info("Calculated tokens in {calc_time:.2f}ms.", calc_time=(end_time - start_time) / 1e6)
        tokens_count = len(tokens_encoding.ids)
        text_count = len(persona_info.message_stripped_str)
        most_frequent: list[str] = ["Most frequent:"]
        for id, count in counter.most_common(storage_configs.tokenizer_most_frequent_tokens):
            token = tokenizer.id_to_token(id) or "[UNK]"
            token_text = f"[{id}]: 0x{token.encode('utf-8').hex()}"
            most_frequent.append(token_text)

        await self.output(
            send_msg = send_msg,
            tokens_count = tokens_count,
            text_count = text_count,
            most_frequent = most_frequent
        )

    async def output(
            self,
            send_msg: SendMsg,
            tokens_count: int,
            text_count: int,
            most_frequent: list[str]
        ):
        await send_msg.send_mixed_render(
            prefix_text = "\n".join(
                [
                    f"Token count: {tokens_count}",
                    f"Text length: {text_count}",
                    f"Average something conversion rate: {tokens_count / text_count:.2%}(1:{tokens_count / text_count:.2f})"
                ]
            ),
            text_to_render = "\n  - ".join(most_frequent)
        )