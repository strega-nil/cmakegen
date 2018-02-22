import argparse

from . import generate
from .options import *

def main():
  standard_version_help = (
      "The version of the standard you'd like to use "
      "(supported values: '14', '17')")
  kind_help = (
      "The kind of project you'd like to build "
      "(supported values: '{}', '{}', '{}')")
  kind_help = kind_help.format(KIND_EXE, KIND_LIB, KIND_HEAD)
  force_help = (
      "If the directory already exists, then cmakegen will not fail. "
      "Probably dangerous.")
  clangfmt_help = (
      "Generates a .clang-format file in the project directory. "
      "By default, this uses Nicole's preferred style. "
      "There is currently no support for other styles; it will be added later")
  dry_run_help = (
      "Don't actually do any building, just print out what we're doing. "
      "Useful for development purposes")

  ap = argparse.ArgumentParser(
      description="Create a directory structure for a CMake project")
  ap.add_argument(
      "project_name",
      help="The name of your CMake project",
      metavar="proj")
  ap.add_argument(
      "--std",
      nargs="?",
      choices=[14, 17],
      default=STANDARD_DEFAULT,
      help=standard_version_help,
      metavar="N",
      dest="standard")
  ap.add_argument(
      "--kind",
      nargs="?",
      choices=[KIND_EXE, KIND_LIB, KIND_HEAD],
      default=KIND_DEFAULT,
      help=kind_help,
      metavar="kind")
  ap.add_argument(
      "--style",
      "--clang-format",
      nargs="?",
      choices=[STYLE_NICOLETTE],
      default=None,
      const=STYLE_DEFAULT,
      help=clangfmt_help,
      dest="style")

  force_or_dry_run = ap.add_mutually_exclusive_group()
  force_or_dry_run.add_argument(
      "--force",
      action="store_true",
      help=force_help)
  force_or_dry_run.add_argument(
      "--dry-run",
      action="store_true",
      help=dry_run_help,
      dest="dry_run")

  args = ap.parse_args()

  generator = None
  if args.dry_run:
    generator = generate.DryRunGenerator()
  else:
    generator = generate.NormalGenerator(args.force)

  generate.build_project(
      generator,
      project_name=args.project_name,
      style=args.style,
      kind=args.kind,
      standard=args.standard)

