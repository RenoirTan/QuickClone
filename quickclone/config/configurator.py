from __future__ import annotations
from pathlib import Path
import typing as t

import toml


from .common import DEFAULTS_FOLDER, USER_CONFIG_FILE


class Configurator(object):
    """
    A wrapper around a configuration file meant for QuickClone. This class
    has special methods for retrieving nested items.
    """
    
    def __init__(self, configuration: t.Mapping[str, t.Any]) -> None:
        self.configuration = configuration
    
    def __getitem__(self, key: t.Union[str, t.Iterable[str]]) -> t.Optional[t.Any]:
        if type(key) == str:
            return self.configuration.get(key)
        container = self.configuration
        for part in key:
            container = container.get(part)
            if container is None:
                return None
        return container
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(configuration={self.configuration})"
    
    @classmethod
    def from_file(cls, path: Path) -> Configurator:
        """
        Load the configuration from a file.
        
        Parameters
        ----------
        path: Path
            Path to the configuration file.
        
        Returns
        -------
        Configurator
            The configuration loaded from the file stored as a `Configurator`
            object.
        """
        configuration = toml.load(path)
        return cls(configuration)


DEFAULT_CONFIGURATION = Configurator.from_file(DEFAULTS_FOLDER / "quickclone.toml")


class SmartConfigurator(Configurator):
    def __getitem__(self, key: t.Union[str, t.Iterable[str]]) -> t.Any:
        result = super().__getitem__(key)
        if result is None:
            return DEFAULT_CONFIGURATION[key]
        else:
            return result


def load_user_config(path: t.Optional[Path] = None) -> SmartConfigurator:
    path = USER_CONFIG_FILE if path is None else path
    if path.exists() and path.is_file():
        return SmartConfigurator.from_file(path)
    else:
        return SmartConfigurator({})
