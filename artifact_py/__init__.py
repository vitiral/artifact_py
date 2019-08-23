# artifact_py: the design documentation tool made for everyone.
#
# Copyright (C) 2019 Rett Berg <github.com/vitiral>
#
# The source code is Licensed under either of
#
# * Apache License, Version 2.0, ([LICENSE-APACHE](LICENSE-APACHE) or
#   http://www.apache.org/licenses/LICENSE-2.0)
# * MIT license ([LICENSE-MIT](LICENSE-MIT) or
#   http://opensource.org/licenses/MIT)
#
# at your option.
#
# Unless you explicitly state otherwise, any contribution intentionally submitted
# for inclusion in the work by you, as defined in the Apache-2.0 license, shall
# be dual licensed as above, without any additional terms or conditions.
"""
A reimagining of artifact.

See README.md and #SPC-design
"""
from __future__ import print_function, unicode_literals, division
import sys
import argparse
import json
import yaml

from . import utils
from . import load
from . import dump
from . import lint


def parse_args(argv):
    """Parse arguments for the cmdline functions."""
    parser = argparse.ArgumentParser(
        description='The design documentation tool for everyone.')

    parser.add_argument('--doc',
                        help="Change the root design doc.",
                        default="./README.md")

    subparsers = parser.add_subparsers(
        help='There are multiple types of commands you can perform.',
        dest='mode')

    # export
    parser_export = subparsers.add_parser(
        'export', help='export the designs to stdout or an output.')
    parser_export.add_argument('-o', '--output', help='path to output file')
    parser_export.add_argument(
        '-i',
        '--inplace',
        action='store_true',
        help='whether to export inplace. Only valid with --format md')
    parser_export.add_argument(
        '--format',
        help='format to output to on of [json, yaml, md]',
        default='md')

    # completion
    parser_show = subparsers.add_parser('show',
                                        help='show various information')
    parser_show.add_argument(
        'type', help='the type of information to show. One of [spc, tst]')

    # lint
    parser_lint = subparsers.add_parser('lint',
                                        help='lint the project for errors.')
    parser_lint.add_argument('--strict',
                             action='store_true',
                             help='Return failure if warnings exist.')

    args = parser.parse_args(argv)
    return parser, args


def run_export(parser, args, project):
    """export cmd."""
    output = None
    try:
        if args.inplace:
            if args.format != 'md':
                return fail("if --inplace requires --format=md")
            output = open(args.doc, 'w')
        elif args.output:
            output = open(args.output, 'w')
        else:
            output = sys.stdout

        if args.format == 'json':
            json.dump(project.serialize(), output)
        elif args.format == 'yaml':
            yaml.safe_dump(project.serialize(), output)
        elif args.format == 'md':
            utils.write_lines(dump.dump_project(project), output)
        else:
            return fail("Unrecognized --format: " + args.format,
                        parser_help=parser)

        utils.flush_output(output)
    finally:
        if output and output is not sys.stdout:
            output.close()

    return 0


def run_show(parser, args, project):
    """show cmd."""
    artifacts = project.artifacts
    if args.type == 'spc':
        for art in sorted(artifacts, key=lambda art: art.name):
            print('{}\t{}'.format(art.name.key, art.completion.spc))
    elif args.type == 'tst':
        for art in sorted(artifacts, key=lambda art: art.name):
            print('{}\t{}'.format(art.name.key, art.completion.tst))
    else:
        return fail("Unrecognized type: " + args.type, parser_help=parser)

    return 0


def run_lint(_parser, args, project):
    """lint cmd."""
    lints = lint.lint_project(project)
    if lints.warnings:
        print('WARNINGS:')
        for warn in lints.warnings:
            print(warn)
        if lints.errors:
            # print extra line to separate errors
            print()

    if lints.errors:
        print('ERRORS:')
        for error in lints.errors:
            print(error)

    if lints.errors or (args.strict and lints.warnings):
        return 1
    return 0


def fail(msg, parser_help=None):
    """Print a message and, optionally, the parser to print it's help message."""
    print(msg)
    if parser_help:
        parser_help.print_help()
    return 1


def main(argv):  # pylint: disable=too-many-branches
    """Main function for cmdline."""

    parser, args = parse_args(argv)

    if args.mode is None:
        return fail("must specify a mode", parser_help=parser)

    project = load.from_root_file(args.doc)

    if args.mode == 'export':
        return run_export(parser, args, project)

    if args.mode == 'show':
        return run_show(parser, args, project)

    if args.mode == 'lint':
        return run_lint(parser, args, project)

    return fail("Unrecognized mode: " + args.mode, parser_help=parser)
