from typing import Union, List, Dict

from invisionChatbox.base.base import Validator
from invisionChatbox.context import Context


class Event:
    def __init__(self, callback, command: bool = True, command_name: str = None, validators: List[Validator] = None,
                 case_sensitive: bool = False):
        self.command = command
        self.command_name = command_name
        self.callback = callback
        self.validators = validators
        self.case_sensitive = case_sensitive

    def check(self, command_name, context: Context, data: dict):
        is_case_match = True
        if self.case_sensitive:
            is_case_match = command_name == self.command_name
        return all([validator.validate(context) for validator in self.validators] + [is_case_match])


class EventHandler:
    def __init__(self):
        self.handlers: Dict[str, List[Event]] = {}

    def get_events(self, event_name: str) -> List[Event]:
        if events := self.handlers.get(event_name):
            return events
        return []

    def call_command(self, command_name: str, context: Context, data: dict):
        for event in self.get_events(command_name):
            if event.check(command_name, context, data):
                event.callback(context, data)

    def event(self, event_name: Union[str, List[str]] = None, validators=None, is_command=False,
              case_sensitive: bool = False):

        if not is_command:
            event_name = '__non_command__'

        if validators is None:
            validators = []

        def register_handler(handler):

            if isinstance(event_name, list) or isinstance(event_name, tuple):
                for _event_name in event_name:
                    register(handler=handler, _name=_event_name if event_name else handler.__name__,
                             _validators=validators, _is_command=is_command, _case_sensitive=case_sensitive)
            else:
                register(handler=handler, _name=event_name if event_name else handler.__name__, _validators=validators,
                         _is_command=is_command, _case_sensitive=case_sensitive)
            return handler

        def register(handler, _is_command, _validators, _name, _case_sensitive: bool = False):
            if events := self.handlers.get(_name):
                events = events
            else:
                events = []

            events.append(Event(command=_is_command, command_name=_name, validators=_validators,
                                callback=handler, case_sensitive=_case_sensitive))

            self.handlers.update({_name: events})

        return register_handler
