"""ttLib/ttf.py -- quick command for ttf to woff.
"""

import sys
from fontTools import ttLib
import logging

log = logging.getLogger("fontTools.ttLib.woff")

def compress(input_file, output_file, transform_tables=None):
    """Compress OpenType font to WOFF2.

    Args:
        input_file: a file path, file or file-like object (open in binary mode)
            containing an OpenType font (either CFF- or TrueType-flavored).
        output_file: a file path, file or file-like object where to save the
            compressed WOFF font.
        transform_tables: Optional[Iterable[str]]: a set of table tags for which
            to enable preprocessing transformations. By default, only 'glyf'
            and 'loca' tables are transformed. An empty set means disable all
            transformations.
    """
    log.info("Processing %s => %s" % (input_file, output_file))

    font = ttLib.TTFont(input_file, recalcBBoxes=False, recalcTimestamp=False)
    font.flavor = "woff"


    font.save(output_file, reorderTables=False)

def main(args=None):
    import argparse
    from fontTools.ttx import makeOutputFileName

    parser = argparse.ArgumentParser(
        prog="fonttools ttLib.woff",
        description=main.__doc__,
        add_help = False
    )

    parser_group = parser.add_subparsers(title="sub-commands")
    parser_compress = parser_group.add_parser("compress",
        description = "Compress a TTF or OTF font to WOFF")

    parser_compress.add_argument(
        "input_file",
        metavar="INPUT",
        help="the input OpenType font (.ttf or .otf)",
    )

    parser_compress.add_argument(
        "-o",
        "--output-file",
        metavar="OUTPUT",
        help="the output WOFF font",
    )

    parser_compress.set_defaults(
        subcommand=compress,
        transform_tables={"glyf", "loca"},
    )

    options = vars(parser.parse_args(args))

    subcommand = options.pop("subcommand", None)

    if not subcommand:
        parser.print_help()
        return

    if not options["output_file"]:
        if subcommand is compress:
            extension = ".woff"
        else:
            raise AssertionError(subcommand)
        
        options["output_file"] = makeOutputFileName(
            options["input_file"], outputDir=None, extension=extension
        )

    try:
        subcommand(**options)
    except TTLibError as e:
        parser.error(e)


if __name__ == "__main__":
    sys.exit(main())