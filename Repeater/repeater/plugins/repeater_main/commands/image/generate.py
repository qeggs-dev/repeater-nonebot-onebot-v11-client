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