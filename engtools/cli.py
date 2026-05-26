"""ENGTools CLI — main entry point.

Mirrors the top-level menu structure of ENGTools.bat.
Each subcommand is a stub that prints a "not yet implemented" message;
the goal of this step is to establish the command hierarchy.
"""

import sys
import click
from engtools import __version__
from engtools.logger import setup_logging


# ---------------------------------------------------------------------------
# Root group
# ---------------------------------------------------------------------------

@click.group()
@click.version_option(version=__version__, prog_name="engtools")
def main() -> None:
    """ENGTools — LanguageWire Engineering toolbox."""
    setup_logging()


# ---------------------------------------------------------------------------
# sfp
# ---------------------------------------------------------------------------

@main.group()
def sfp() -> None:
    """Source File Preparation workflows."""


_SFP_COMMANDS = [
    ("standard",         "Okapi standard SFP."),
    ("custom",           "Okapi custom SFP."),
    ("xliff",            "Okapi XLIFF SFP."),
    ("proofreading",     "Okapi SFP for proofreading."),
    ("pretranslate",     "Okapi pretranslation SFP."),
    ("daimler",          "Daimler multilingual proofreading."),
    ("epiroc",           "Epiroc TXT SFP."),
    ("axis",             "AXIS Type 4 SFP."),
    ("beurer",           "Beurer multilingual SFP."),
    ("edwards",          "Edwards / Leybold / Atlas brand processor."),
    ("confirm-sdlxliff", "Confirm segments in SDLXLIFF files."),
]

for _name, _help in _SFP_COMMANDS:
    def _make_sfp(cmd_name: str, cmd_help: str) -> click.Command:
        @sfp.command(name=cmd_name, help=cmd_help)
        @click.option("--sl", default="", metavar="LANG", help="Source language code (e.g. en).")
        @click.option("--tl", default="", metavar="LANG", help="Target language code (e.g. de).")
        def _cmd(sl: str, tl: str) -> None:  # noqa: ANN001
            click.echo(f"[sfp {cmd_name}] not yet implemented.")
            sys.exit(0)
        return _cmd
    _make_sfp(_name, _help)


# ---------------------------------------------------------------------------
# tm
# ---------------------------------------------------------------------------

@main.group()
def tm() -> None:
    """TM Management workflows."""


_TM_COMMANDS = [
    ("xlf-to-tmx",         "Convert XLF/flavours to TMX."),
    ("xlf-to-table",       "Convert XLF/flavours to bilingual table."),
    ("cleanup",            "Clean up TMX."),
    ("excel-to-tmx",       "Convert Excel (bilingual/multilingual) to TMX."),
    ("resegment",          "Resegment paragraph-based TMX."),
    ("split-multilingual", "Split multilingual TMX."),
]

for _name, _help in _TM_COMMANDS:
    def _make_tm(cmd_name: str, cmd_help: str) -> click.Command:
        @tm.command(name=cmd_name, help=cmd_help)
        @click.option("--sl", default="", metavar="LANG", help="Source language code (e.g. en).")
        @click.option("--tl", default="", metavar="LANG", help="Target language code (e.g. de).")
        def _cmd(sl: str, tl: str) -> None:  # noqa: ANN001
            click.echo(f"[tm {cmd_name}] not yet implemented.")
            sys.exit(0)
        return _cmd
    _make_tm(_name, _help)


# ---------------------------------------------------------------------------
# translation
# ---------------------------------------------------------------------------

@main.group()
def translation() -> None:
    """Translation workflows."""


_TRANSLATION_COMMANDS = [
    ("standard",      "Standard translation workflow."),
    ("translation-2", "Translation 2.0 workflow."),
]

for _name, _help in _TRANSLATION_COMMANDS:
    def _make_translation(cmd_name: str, cmd_help: str) -> click.Command:
        @translation.command(name=cmd_name, help=cmd_help)
        @click.option("--sl", default="", metavar="LANG", help="Source language code (e.g. en).")
        @click.option("--tl", default="", metavar="LANG", help="Target language code (e.g. de).")
        def _cmd(sl: str, tl: str) -> None:  # noqa: ANN001
            click.echo(f"[translation {cmd_name}] not yet implemented.")
            sys.exit(0)
        return _cmd
    _make_translation(_name, _help)


# ---------------------------------------------------------------------------
# alignment
# ---------------------------------------------------------------------------

@main.group()
def alignment() -> None:
    """Alignment workflows."""


@alignment.command(name="id-based")
@click.option("--sl", default="", metavar="LANG", help="Source language code (e.g. en).")
@click.option("--tl", default="", metavar="LANG", help="Target language code (e.g. de).")
def alignment_id_based(sl: str, tl: str) -> None:
    """ID-based alignment."""
    click.echo("[alignment id-based] not yet implemented.")
    sys.exit(0)


# ---------------------------------------------------------------------------
# office
# ---------------------------------------------------------------------------

@main.group()
def office() -> None:
    """Microsoft Office Tools."""


_OFFICE_COMMANDS = [
    ("update-toc",    "Batch update TOCs in Word files."),
    ("unhide-docx",   "Batch unhide and rename .doc/.docx files."),
    ("hide-color",    "Batch hide based on colour text in Word files."),
    ("anonymize",     "Anonymize track changes."),
    ("unhide-xlsx",   "Batch unhide and rename .xls/.xlsx files."),
    ("split-xlsx",    "Split/merge multilingual .xlsx files."),
]

for _name, _help in _OFFICE_COMMANDS:
    def _make_office(cmd_name: str, cmd_help: str) -> click.Command:
        @office.command(name=cmd_name, help=cmd_help)
        def _cmd() -> None:  # noqa: ANN001
            click.echo(f"[office {cmd_name}] not yet implemented.")
            sys.exit(0)
        return _cmd
    _make_office(_name, _help)


# ---------------------------------------------------------------------------
# tools
# ---------------------------------------------------------------------------

@main.group()
def tools() -> None:
    """Miscellaneous utility tools."""


_TOOLS_COMMANDS = [
    ("flatten",           "Flatten folder structure."),
    ("unflatten",         "Unflatten folder structure."),
    ("distribute",        "Distribute files by target language code."),
    ("json-paths",        "Extract JSON paths."),
    ("xpath",             "XPath generator."),
    ("remove-locales",    "Remove platform locales."),
    ("regin",             "Regin .en files to/from multilingual Excel."),
    ("maxlen",            "Static Maxlen Setter."),
    ("delete-column-csv", "Batch delete column from CSV."),
    ("webcrawl",          "Web-crawling utility."),
    ("pdf-comments",      "Extract PDF comments to Excel/CSV."),
    ("append-folder",     "Append folder name to files."),
    ("srt-vtt",           "Convert SRT to/from VTT."),
]

for _name, _help in _TOOLS_COMMANDS:
    def _make_tool(cmd_name: str, cmd_help: str) -> click.Command:
        @tools.command(name=cmd_name, help=cmd_help)
        def _cmd() -> None:  # noqa: ANN001
            click.echo(f"[tools {cmd_name}] not yet implemented.")
            sys.exit(0)
        return _cmd
    _make_tool(_name, _help)
