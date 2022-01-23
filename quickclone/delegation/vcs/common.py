import shlex
import shutil
import typing as t

from quickclone.delegation.errors import CommandNotFoundError


__all__ = ["BaseCommand", "Command"]


class BaseCommand(object):
    """
    Base class for representing commands.
    """
    
    def __init__(self, location: str = "", *args: t.Any, **kwargs: t.Any) -> None:
        self.location = location
        self.args = args
        self.kwargs = kwargs
    
    def format_command_list(self) -> t.List[str]:
        return []
    
    def format_command_str(self) -> str:
        return shlex.join(self.format_command_list())


class Command(BaseCommand):
    """
    Basic command. Uses `echo` as a dummy command.
    """
    
    COMMAND_NAME: str = "echo" # Dummy command
    
    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        location = shutil.which(self.COMMAND_NAME)
        if location is None:
            raise CommandNotFoundError(self.COMMAND_NAME)
        super().__init__(location, *args, **kwargs)
    
    def format_command_list(self) -> t.List[str]:
        return [self.location, *self.args]
