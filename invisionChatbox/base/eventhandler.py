from typing import Union, List, Dict

from invisionChatbox.context import Context
from invisionChatbox.base.basic import Validator


class Event:
    def __init__(self, callback, command: bool = True, command_name: str = None, validators: List[Validator] = None):
        self.command = command
        self.command_name = command_name
        self.callback = callback
        self.validators = validators

    def check(self, context: Context, data: dict):
        return all([validator.validate(context.content) for validator in self.validators])


class EventHandler:
    def __init__(self):
        self.handlers: Dict[str, List[Event]] = {}

    def call_command(self, command_name, context: Context, data: dict):
        if command_name in self.handlers.keys():
            for event in self.handlers[command_name]:
                if event.check(context, data):
                    event.callback(context, data)

    def event(self, event_name: Union[str, List[str]] = None, validators=None, is_command=False):

        if not is_command:
            event_name = '__non_command__'

        if validators is None:
            validators = []

        def register_handler(handler):

            if isinstance(event_name, list) or isinstance(event_name, tuple):
                for _event_name in event_name:
                    register(handler=handler, _name=_event_name if event_name else handler.__name__,
                             _validators=validators, _is_command=is_command)
            else:
                register(handler=handler, _name=event_name if event_name else handler.__name__, _validators=validators,
                         _is_command=is_command)
            return handler

        def register(handler, _is_command, _validators, _name):
            if events := self.handlers.get(_name):
                events = events
            else:
                events = []

            events.append(Event(command=_is_command, command_name=_name, validators=_validators,
                                callback=handler))

            self.handlers.update({_name: events})

        return register_handler
