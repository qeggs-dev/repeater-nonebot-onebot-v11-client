from ...command_register import(
    CommandCaller
)
from .._bases import GenerateImageBase

@CommandCaller.register
class GenerateImage(GenerateImageBase):
    cmd = "generateImage"
    aliases = {
        "gi",
        "GI",
        "generate_image",
        "Generate_Image",
        "GenerateImage",
        "GENERATE_IMAGE",
    }
    description = f"""
    Generate an image from a given prompt.
    When a picture is present in the message, it is extracted as a reference graph.
    When there is a reference, the picture in the reference message will be loaded first.

    Usage:
    ```
    /{cmd} prompt 
    ```
    """