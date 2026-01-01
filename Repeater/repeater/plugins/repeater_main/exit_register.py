from __future__ import annotations
import sys
import atexit
import asyncio
import threading
from typing import Callable, Optional, Type, Coroutine

class ExitRegister:
    # 存储退出处理函数的字典，键为优先级，值为处理函数列表
    _exit_handlers: dict[int, list[Callable]] = {}
    # 存储优先级的列表
    _priorities = []
    # 存储ExitRegister实例的变量
    _instance: Optional[ExitRegister] = None
    # 是否使用锁的变量
    _with_lock: bool = False
    _with_async_lock: bool = False
    # 锁对象
    _lock: threading.Lock = threading.Lock()
    _async_lock: asyncio.Lock = asyncio.Lock()
    # 存储异常处理函数的字典，键为异常类型和处理函数，值为处理函数
    _exception_processors: dict[tuple[Type[Exception], Callable], Callable] = {}
    

    def __new__(cls):
        # 如果没有实例，则创建实例
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, with_lock: bool = False, with_async_lock: bool = False):
        # 初始化是否使用锁的变量
        if with_lock and with_async_lock:
            raise ValueError("Cannot use both lock and async lock")
        self._with_lock = with_lock
        self._with_async_lock = with_async_lock
        
        @atexit.register
        def _exit_handler():
            """
            程序退出时调用所有注册的函数
            
            使用闭包方法代替成员方法进行函数调用
            """
            # 按优先级从高到低遍历处理函数列表
            for priority in reversed(self._priorities):
                # 遍历每个优先级的处理函数列表
                for handler in self._exit_handlers[priority]:
                    try:
                        # 调用处理函数
                        handler()
                    except Exception as e:
                        # 如果处理函数抛出异常，则查找对应的异常处理器
                        index = (type(e), handler)
                        if index in self._exception_processors:
                            # 调用异常处理器
                            self._exception_processors[index](e)
                        else:
                            # 如果没有找到对应的异常处理器，则打印异常信息
                            print(f"[ExitRegister] Exception for unregistered processor: {e}", file=sys.stderr)


    def register(self, priority: int = 0):
        """装饰器工厂，用于注册函数并指定优先级"""
        def decorator(func: Callable):
            if isinstance(func, Coroutine):
                raise ValueError("Cannot register coroutine function")
            # 如果使用锁，则获取锁
            if self._with_lock:
                self._lock.acquire()
            if self._with_async_lock:
                self._async_lock.acquire()
            
            # 如果优先级不在字典中，则添加优先级和对应的处理函数列表
            if priority not in self._exit_handlers:
                self._exit_handlers[priority] = []
                self._priorities.append(priority)
                self._priorities.sort()
            # 将处理函数添加到对应的优先级列表中
            self._exit_handlers[priority].append(func)

            # 如果使用锁，则释放锁
            if self._with_lock:
                self._lock.release()
            if self._with_async_lock:
                self._async_lock.release()
            return func
        return decorator
    
    def exit_handler_exception_processor(self, exception: Exception, handler: Callable):
        """装饰器工厂，用于注册异常处理器"""
        def decorator(func: Callable):
            if isinstance(func, Coroutine):
                raise ValueError("Cannot register coroutine function")
            # 如果使用锁，则获取锁
            if self._with_lock:
                self._lock.acquire()
            if self._with_async_lock:
                self._async_lock.acquire()
            
            # 将异常类型和处理函数作为键，将处理函数添加到字典中
            index = (exception, handler)
            self._exception_processors[index] = func

            # 如果使用锁，则释放锁
            if self._with_lock:
                self._lock.release()
            if self._with_async_lock:
                self._async_lock.release()
        return decorator
        