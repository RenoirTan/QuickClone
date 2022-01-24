from pathlib import Path


DEFAULTS_FOLDER: Path = Path(__file__).parent / "defaults"
USER_CONFIG_FILE: Path = Path.home() / ".config" / "quickclone.toml"
