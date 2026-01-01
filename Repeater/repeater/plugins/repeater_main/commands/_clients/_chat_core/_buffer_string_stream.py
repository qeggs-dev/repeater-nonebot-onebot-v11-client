from typing import AsyncIterator

class BufferStringStream:
    def __init__(self, async_iterator: AsyncIterator[str], separator: str = "\n\n"):
        self._async_iterator = async_iterator
        self._separator = separator
        self._buffer = ""
        self._is_done = False

    async def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self._is_done:
            raise StopAsyncIteration
        try:
            while True:
                next_item = await anext(self._async_iterator)
                self._buffer += next_item
                if self._separator in self._buffer:
                    output, self._buffer = self._buffer.rsplit(self._separator, 1)
                    return output
        except StopAsyncIteration:
            self._is_done = True
            return self._buffer
                