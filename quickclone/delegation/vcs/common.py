import shlex
import shutil
import typing as t

from quickclone.delegation.errors import CommandNotFoundError


__all__ = ["BaseVCSCommand", "VCSCommand"]


class BaseVCSCommand(object):
    """
    Base class for representing commands of different VCS programs.
    """
    
    def __init__(self, location: str = "", action: str = "", *args, **kwargs) -> None:
        self.location = location
        self.action = action
        self.kwargs = kwargs
    
    def format_command_list(self) -> t.List[str]:
        return []
    
    def format_command_str(self) -> str:
        return shlex.join(self.format_command_list())


class VCSCommand(BaseVCSCommand):
    """
    Basic VCSCommand. Uses `echo` as the dummy command.
    """
    
    NAME: str = "echo" # Dummy command
    
    def __init__(self, action: str = "", *args, **kwargs) -> None:
        location = shutil.which(self.NAME)
        if location is None:
            raise CommandNotFoundError(self.NAME)
        super().__init__(location, action, *args, **kwargs)
    
    def format_command_list(self) -> t.List[str]:
        return [self.location, *self.args]
