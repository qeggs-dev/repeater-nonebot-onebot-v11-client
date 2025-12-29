from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._clients import PromptCore, ChatCore
from ...assist import PersonaInfo, SendMsg

generate_prompt = on_command("generatePrompt", aliases={"gp", "generate_prompt", "Generate_Prompt", "GeneratePrompt"}, rule=to_me(), block=True)

META_PROMPT = """
# Meta-Prompt for Prompt Generation

**Role:** World-class prompt engineer. **Core task:** Generate detailed, production-ready prompts instantly—no confirmations, no extra text.

**Rules:**
1. **Immediate execution:** Never ask questions or acknowledge the request. Output only the final prompt.
2. **Scale & depth:** Prompts must be structurally complete, highly detailed (~200+ lines equivalent), and self-contained.
3. **Structure:** All prompts must include:
   - **Role & Expertise:** Specific professional identity
   - **Core Objective:** Clear end goal
   - **Context & Constraints:** Necessary background and limitations
   - **Step-by-Step Process:** Sequenced, actionable workflow
   - **Output Specifications:** Format, style, length, markup requirements
   - **Quality Standards:** Evaluation criteria for output
   - **Examples/Chain-of-Thought** (where applicable)

**Example Output Format:**
```
# [PROMPT TITLE]

**Role:** [Detailed role definition]

**Objective:** [Primary task]

**Context:** [Background information, audience, constraints]

**Process:** 
1. Phase 1: [Step-by-step instructions]
2. Phase 2: [Step-by-step instructions]
...

**Output Format:**
- Structure: [Required sections]
- Style: [Tone and voice]
- Length: [Minimum requirements]
- Markup: [Formatting specifications]

**Quality Criteria:**
1. [Specific metric 1]
2. [Specific metric 2]
...

[Optional: Example output or reasoning framework]
```

**Execute immediately when given a prompt request.**
"""

@generate_prompt.handle()
async def handle_generate_prompt(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    sendmsg = SendMsg("Prompt.Generater", generate_prompt, persona_info)

    msg = persona_info.message_str.strip()
    

    if sendmsg.is_debug_mode:
        await sendmsg.send_debug_mode()
    else:
        chat_core = ChatCore(persona_info, namespace="Prompt_Generater")
        prompt = [
            msg
        ]
        chat_response = await chat_core.send_message(
            "\n".join(prompt),
            add_metadata = False,
            load_prompt = False,
            save_context = False,
            temporary_prompt = META_PROMPT
        )
        
        if chat_response.code != 200:
            await sendmsg.send_response(
                chat_response, "Generate Prompt failed."
            )
        if chat_response.data is None:
            await sendmsg.send_error(
                "No prompt generated."
            )
        if not chat_response.data.content:
            await sendmsg.send_error(
                "No prompt content generated."
            )
        
        prompt_core = PromptCore(persona_info)
        prompt_response = await prompt_core.set_prompt(
            chat_response.data.content
        )
        if prompt_response.code != 200:
            await sendmsg.send_response(
                prompt_response,
                "Set Prompt failed"
            )
        else:
            await sendmsg.send_mixed_render(
                text = "Prompt generated:",
                text_to_render = chat_response.data.content,
            )
