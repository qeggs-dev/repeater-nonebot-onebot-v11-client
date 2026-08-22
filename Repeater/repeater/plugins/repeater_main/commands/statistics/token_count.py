from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...clients import RequestLogClient

@CommandCaller.register
class TokenCount(CommandPackage):
    cmd = "tokenCount"
    aliases = {
        "tc",
        "TC",
        "token_count",
        "Token_Count",
        "TokenCount",
        "TOKEN_COUNT",
    }
    cmd_type = CmdTypes.STATISTIC
    description = f"""
    Count tokens using request_log.
    Warning: this is a very slow operation that can take a lot of time and resources.

    Usage:
        /{cmd}
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        user_configs = await persona_info.get_user_configs()
        client = RequestLogClient(persona_info, user_configs)

        request_logs = client.get_request_log()

        total_token_count: int = 0
        input_token_count: int = 0
        output_token_count: int = 0
        cache_hit_count: int = 0
        cache_miss_count: int = 0
        count: int = 0

        user_id = persona_info.namespace_str

        async for request_log in request_logs:
            if request_log.user_id == user_id:
                total_token_count += request_log.total_tokens
                input_token_count += request_log.prompt_tokens
                output_token_count += request_log.completion_tokens
                if request_log.cache_hit_count or request_log.cache_miss_count:
                    cache_hit_count += request_log.cache_hit_count
                    cache_miss_count += request_log.cache_miss_count
                else:
                    cache_miss_count += request_log.prompt_tokens
                count += 1
        
        await send_msg.send_prompt(
            f"Valid Record Count: {count}\n"
            f"Total Token Count: {total_token_count}\n"
            f"Input Token Count: {input_token_count}\n"
            f"Output Token Count: {output_token_count}\n"
            f"Cache Hit Count: {cache_hit_count}\n"
            f"Cache Miss Count: {cache_miss_count}\n"
            f"Cache Hit Rate: {cache_hit_count / (cache_hit_count + cache_miss_count):.2%}\n"
        )