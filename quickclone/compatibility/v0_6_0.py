import toml
from quickclone.config.common import USER_HISTORY_CACHE_FILE

def quickclone_history_list() -> int:
    """
    Fix for v0.6.0 or below.
    
    Converts the history cache file such that it contains a list of previous
    cloned repositories from just containing the last cloned repository.
    """
    history = toml.load(USER_HISTORY_CACHE_FILE)
    old = history.get("last_clone")
    new = history.get("last_clones")
    if new is None:
        history["last_clones"] = [old] if old else []
    if old:
        del history["last_clone"]
    with USER_HISTORY_CACHE_FILE.open("w") as f:
        toml.dump(history, f)
    return 0