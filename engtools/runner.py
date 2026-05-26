"""Shared subprocess helpers used by ENGTools workflows."""

import logging
import shutil
import subprocess
import sys
from pathlib import Path


def _run_command(command: list[str], success_codes: set[int] | None = None) -> None:
    expected_codes = success_codes or {0}
    command_text = " ".join(command)
    logging.info("Running command: %s", command_text)

    try:
        result = subprocess.run(command, check=False)
    except OSError as exc:
        logging.error("Failed to launch command: %s", command_text)
        raise RuntimeError(f"Failed to launch command: {command_text}") from exc

    if result.returncode not in expected_codes:
        logging.error("Command failed with exit code %s: %s", result.returncode, command_text)
        raise RuntimeError(
            f"Command failed with exit code {result.returncode}: {command_text}"
        )


def run_okapi(tikal_path: str, args: list[str]) -> None:
    """Call tikal.bat with the given arguments. Raise on non-zero exit code."""
    _run_command([tikal_path, *args])


def run_python_script(script_path: str, args: list[str] | None = None) -> None:
    """Run a Python script by path with optional arguments. Raise on non-zero exit code."""
    script_args = args or []
    _run_command([sys.executable, script_path, *script_args])


def robocopy(
    src: str,
    dst: str,
    files: str = "*.*",
    extra_flags: list[str] | None = None,
) -> None:
    """Wrap robocopy. Treat exit codes 0-3 as success (robocopy convention)."""
    flags = extra_flags or []
    _run_command(["robocopy", src, dst, files, *flags], success_codes={0, 1, 2, 3})


def make_zip(sevenzip_path: str, output_zip: str, source_glob: str) -> None:
    """Create a zip archive using 7-Zip."""
    _run_command([sevenzip_path, "a", "-tzip", output_zip, source_glob])


def mkdir(path: str) -> None:
    """Create a directory if it doesn't exist. Equivalent to mkdir ... 2>nul."""
    target = Path(path)
    logging.info("Ensuring directory exists: %s", target)
    try:
        target.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        logging.error("Failed to create directory: %s", target)
        raise RuntimeError(f"Failed to create directory: {target}") from exc


def copy_script_and_run(
    script_source: str,
    destination_dir: str,
    script_name: str,
    args: list[str] | None = None,
) -> None:
    """Copy a Python script to destination_dir, run it, then delete it."""
    mkdir(destination_dir)
    source_path = Path(script_source)
    destination_path = Path(destination_dir) / script_name

    logging.info("Copying script from %s to %s", source_path, destination_path)
    try:
        shutil.copy2(source_path, destination_path)
    except OSError as exc:
        logging.error("Failed to copy script to destination: %s", destination_path)
        raise RuntimeError(
            f"Failed to copy script '{source_path}' to '{destination_path}'"
        ) from exc

    try:
        run_python_script(str(destination_path), args=args)
    finally:
        if destination_path.exists():
            logging.info("Deleting temporary script: %s", destination_path)
            try:
                destination_path.unlink()
            except OSError as exc:
                logging.error("Failed to delete temporary script: %s", destination_path)
                raise RuntimeError(
                    f"Failed to delete temporary script: {destination_path}"
                ) from exc
