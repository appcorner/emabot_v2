from asyncio import iscoroutinefunction
from typing import Optional, List
from functools import wraps

class LineAppBotHandler(object):
    def __init__(self):
        """__init__ method.
        """
        self._handlers = {}
        self._default = None

    def add(self, commands: Optional[List[str]]=None):
        """Add handler method.
        :return: decorator
        """
        if isinstance(commands, str):
            commands = [commands]

        def decorator(func):
            if iscoroutinefunction(func):
                @wraps(func)
                async def wrapper(*args, **kwargs):
                    return await func(*args, **kwargs)
                for command in commands:
                    self._handlers[command] = wrapper
                return wrapper
            else:
                @wraps(func)
                def wrapper(*args, **kwargs):
                    return func(*args, **kwargs)
                for command in commands:
                    self._handlers[command] = wrapper
                return wrapper

        return decorator

    async def handle(self, item):
        text = str(item['text'])
        if text.startswith('/'):
            tokens = [x.strip() for x in text.split()]
            tokens[0] = tokens[0][1:]
            command = '_'.join(tokens)
            func = None
            if command in self._handlers.keys():
                func = self._handlers.get(command, None)
            else:
                func = self._handlers.get('command_error', None)
            if func is None:
                print('No handler of ' + command + ' and no default handler')
            else:
                if iscoroutinefunction(func):
                    await func(item)
                else:
                    func(item)

appbot_handler = LineAppBotHandler()