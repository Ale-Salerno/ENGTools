"""SFP workflows."""

import logging
import os
from pathlib import Path

from engtools.config import ENG_ROOT, OKAPI_PATH, SEVENZIP_PATH
from engtools.runner import copy_script_and_run, make_zip, mkdir, robocopy, run_okapi

_QUIET_ROBOCOPY_FLAGS = ["/NDL", "/NFL", "/NJH", "/NJS", "/NP"]


def run_standard(sl: str, tl: str, cwd: Path) -> None:
    """Replicate the OKAPISTANDARDSPF workflow from ENGTools.bat."""
    prep_dir = cwd / "Prep"
    source_dir = prep_dir / "01_source"
    transl_dir = prep_dir / "02_transl"
    pseudo_dir = prep_dir / "03_pseudo"
    config_dir = prep_dir / "04_configs"
    translated_dir = prep_dir / "05_translated"

    logging.info("[INFO] Creating folder structure...")
    mkdir(str(source_dir))
    mkdir(str(transl_dir))
    mkdir(str(pseudo_dir))
    mkdir(str(config_dir))
    mkdir(str(translated_dir))

    logging.info("[INFO] Copying source and config files...")
    robocopy(
        str(cwd),
        str(source_dir),
        "*.*",
        extra_flags=["/XF", "*.bat", *_QUIET_ROBOCOPY_FLAGS],
    )

    eng_root = Path(ENG_ROOT)
    robocopy(
        str(eng_root / "Segmentation" / "okapi"),
        str(config_dir),
        "defaultSegmentation.srx",
        extra_flags=_QUIET_ROBOCOPY_FLAGS,
    )
    robocopy(
        str(eng_root / "Pipelines"),
        str(config_dir),
        "pseudo.pln",
        extra_flags=_QUIET_ROBOCOPY_FLAGS,
    )
    robocopy(
        str(eng_root / "Dependencies" / "bats"),
        str(prep_dir),
        "TFC.bat",
        extra_flags=_QUIET_ROBOCOPY_FLAGS,
    )

    logging.info("[INFO] Running Okapi extraction...")
    run_okapi(
        str(Path(OKAPI_PATH) / "tikal.bat"),
        [
            "-x",
            str(cwd / "Prep" / "01_source" / "*.*"),
            "-seg",
            str(cwd / "Prep" / "04_configs" / "*.srx"),
            "-sl",
            sl,
            "-tl",
            tl,
            "-nocopy",
            "-od",
            str(cwd / "Prep" / "02_transl"),
            "-ie",
            "utf-8",
        ],
    )

    logging.info("[INFO] Running escape_more_than on extracted files...")
    copy_script_and_run(
        script_source=str(eng_root / "Dependencies" / "python" / "escape_more_than.py"),
        destination_dir=str(transl_dir),
        script_name="escape_more_than.py",
    )

    logging.info("[INFO] Pseudotranslating files...")
    robocopy(str(transl_dir), str(pseudo_dir), "*.xlf", extra_flags=_QUIET_ROBOCOPY_FLAGS)
    original_cwd = Path.cwd()
    try:
        os.chdir(pseudo_dir)
    except OSError as exc:
        raise RuntimeError(
            f"Failed to switch working directory to: {pseudo_dir} ({exc})"
        ) from exc
    try:
        copy_script_and_run(
            script_source=str(eng_root / "Dependencies" / "python" / "pseudo.py"),
            destination_dir=str(pseudo_dir),
            script_name="pseudo.py",
        )
    finally:
        os.chdir(original_cwd)

    logging.info("[INFO] Running escape_more_than on pseudotranslated files...")
    copy_script_and_run(
        script_source=str(eng_root / "Dependencies" / "python" / "escape_more_than.py"),
        destination_dir=str(pseudo_dir),
        script_name="escape_more_than.py",
    )

    logging.info("[INFO] Running Okapi merge...")
    run_okapi(
        str(Path(OKAPI_PATH) / "tikal.bat"),
        [
            "-m",
            str(cwd / "Prep" / "03_pseudo" / "*.xlf"),
            "-sd",
            str(cwd / "Prep" / "01_source"),
            "-od",
            str(cwd / "Prep" / "03_pseudo"),
            "-ie",
            "utf-8",
        ],
    )

    logging.info("[INFO] Creating zip package...")
    make_zip(
        str(SEVENZIP_PATH),
        str(cwd / "Prep.zip"),
        str(cwd / "Prep" / "*"),
    )
