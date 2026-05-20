"""Load paths from config.toml and expose them as named constants."""

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_CONFIG_FILE = _REPO_ROOT / "config.toml"

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib  # type: ignore[no-redef]

with _CONFIG_FILE.open("rb") as _fh:
    _config = tomllib.load(_fh)

_paths = _config.get("paths", {})

OKAPI_PATH: str = _paths.get("okapi", "C:/Software/Okapi")
ENG_ROOT: str = _paths.get("eng_root", "W:/Tools/ENGTools")
SEVENZIP_PATH: str = _paths.get("sevenzip", "C:/Program Files/7-Zip/7z.exe")
