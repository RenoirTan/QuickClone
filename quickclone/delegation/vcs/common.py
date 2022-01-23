import shlex
import shutil
import subprocess
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
    
    def run(self) -> t.Union[subprocess.CompletedProcess, subprocess.SubprocessError]:
        cl = self.format_command_list()
        try:
            process = subprocess.run(cl)
        except subprocess.SubprocessError as se:
            return se
        else:
            return process


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
        kwarg_decomposed = []
        for flag, argument in self.kwargs:
            kwarg_decomposed.extend([flag, argument])
        return [self.location, *self.args, *kwarg_decomposed]
