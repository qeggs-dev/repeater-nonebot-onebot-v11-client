import re
from ...assist import PersonaInfo, SendMsg
from ...command_register import(
    CommandCaller,
)
from ...clients import FILE_TYPES
from .._bases import GenerateImageBase

@CommandCaller.register
class GenerateImageWithSize(GenerateImageBase):
    cmd = "generateImageWithSize"
    aliases = {
        "giz",
        "GIZ",
        "generate_image_with_size",
        "Generate_Image_With_Size",
        "GenerateImageWithSize",
        "GENERATE_IMAGE_WITH_SIZE",
    }
    description = f"""
    Generate an image from a given prompt.
    The size of the image can be specified by using the format "widthxheight".

    Usage:
        /{cmd} (x)x(y) prompt
    """

    pattern = re.compile(r"^(?P<size>\d+?x\d+)\s*?(?P<prompt>.*)$", re.DOTALL)
    
    async def get_prompt_with_size(self, persona_info: PersonaInfo, send_msg: SendMsg) -> tuple[list[FILE_TYPES] | None, str, str]:
        images, prompt = await self.get_prompt(persona_info, send_msg)
        
        matched = self.pattern.match(prompt)
        if matched is None:
            await send_msg.send_error("Error: Invalid prompt format")
            send_msg.break_handler()
        
        size = matched.group("size")
        prompt = matched.group("prompt")

        assert isinstance(size, str), "size must be a string"
        assert isinstance(prompt, str), "prompt must be a string"

        return images, prompt, size

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        image_client = await self.get_client(persona_info)
        images, prompt, size = await self.get_prompt_with_size(persona_info, send_msg)
        gen_images = await self.generate_image(
            images = images,
            prompt = prompt,
            size = size,
            image_client = image_client,
            send_msg = send_msg)
        await send_msg.send_images(*gen_images)