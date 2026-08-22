from typing import Iterable, Generator
from nonebot.adapters.onebot.v11 import Message

from typing import List

def split_by_indent(
    message: Message,
    indent: int = 2,
    indent_char: str = " "
) -> list[list[Message]]:   # 返回顶级块列表，每个块是 [父行, 子块（可选）]
    lines = list(enumerate_indent(splitlines(message), indent, indent_char))
    results: list[list[Message]] = []

    current_root: Message | None = None   # 当前顶级行（缩进0）
    current_children: list[str] = []      # 当前子行剥离一级缩进后的文本

    for now_indent, line in lines:
        if now_indent == 0:
            # 完成上一个顶级块
            if current_root is not None:
                block = [current_root]
                if current_children:
                    merged_text = "\n".join(current_children)
                    # 创建新的 Message 来承载合并后的文本
                    # 使用构造函数，具体根据您的 Message API 调整
                    child_msg = Message(merged_text)
                    block.append(child_msg)
                results.append(block)

            # 开始新顶级块
            current_root = line
            current_children = []

        else:
            # 缩进 > 0：删除一级缩进（indent 个 indent_char）
            line_text = str(line)
            prefix = indent_char * indent
            if line_text.startswith(prefix):
                line_text = line_text[len(prefix):]   # 去掉一级缩进
            # 保留剩余缩进（如果有）
            current_children.append(line_text)

    # 处理最后一个顶级块
    if current_root is not None:
        block = [current_root]
        if current_children:
            merged_text = "\n".join(current_children)
            child_msg = Message(merged_text)
            block.append(child_msg)
        results.append(block)

    return results

def enumerate_indent(
    messages: Iterable[Message],
    indent: int = 2,
    indent_char: str = " ",
) -> Generator[tuple[int, Message], None, None]:
    if indent <= 0:
        raise ValueError("indent must be greater than 0")
    
    for message in messages:
        if not message:
            continue

        first_segment = message[0]
        if first_segment.type == "text":
            text = first_segment.data["text"]
            if not isinstance(text, str):
                raise TypeError("text segment must be str")
            
            indent_count: int = 0
            for char in text:
                if char == indent_char:
                    indent_count += 1
                else:
                    break
            
            yield indent_count // indent, message
        else:
            yield 0, message

def splitlines(
    message: Message
) -> list[Message]:
    cq_code_str = str(message)
    cq_codes = cq_code_str.splitlines()
    return [Message(cq_code) for cq_code in cq_codes if cq_code]
