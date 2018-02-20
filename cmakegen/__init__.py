import argparse
from pathlib import Path

from . import cmake_lists
from . import cpp_files
from . import cpp_headers

# TODO(ubsan): add automatic tests to library and headers

KIND_EXE = "executable"
KIND_LIB = "library"
KIND_HEAD = "headers"

default_cxx_version = 14
default_kind = KIND_EXE

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
      default=default_cxx_version,
      help=standard_version_help,
      metavar="N",
      dest="cxx_version")
  ap.add_argument(
      "--kind",
      nargs="?",
      choices=[KIND_EXE, KIND_LIB, KIND_HEAD],
      default=default_kind,
      help=kind_help,
      metavar="kind")
  ap.add_argument(
      "--force",
      action="store_true",
      help=force_help)
  ap.add_argument(
      "--dry-run",
      action="store_true",
      help=dry_run_help,
      dest="dry_run")

  build_project(ap.parse_args())

def mkdir(args, path):
  if not args.dry_run:
    path.mkdir(exist_ok=args.force)
  else:
    print("make directory: ", path)

def write_file(args, path, to_write):
  if not args.dry_run:
    with path.open(mode="w") as file:
      file.write(to_write)
  else:
    print("writing to `", path, "`: ", sep="")
    print(to_write)
    print()

def build_project(args):
  proj_dir = Path(Path.cwd(), args.project_name)
  mkdir(args, proj_dir)
  
  source_dir = Path(proj_dir, "source")
  mkdir(args, source_dir)

  include_dir = Path(proj_dir, "include")
  mkdir(args, include_dir)

  proj_include_dir = Path(include_dir, args.project_name)
  mkdir(args, proj_include_dir)

  cmake_path = Path(proj_dir, "CMakeLists.txt")
  write_file(args, cmake_path, cmake_file(args))

  header_path = Path(proj_include_dir, args.project_name + ".h")

  if args.kind == KIND_EXE:
    write_file(
        args,
        header_path,
        cpp_headers.standalone.substitute(projname=args.project_name))
    write_file(
        args,
        Path(source_dir, "main.cpp"),
        cpp_files.executable.substitute(projname=args.project_name))

  elif args.kind == KIND_LIB:
    write_file(
        args,
        header_path,
        cpp_headers.dependent.substitute(projname=args.project_name))
    write_file(
        args,
        Path(source_dir, args.projname + ".cpp"),
        cpp_files.library.substitute(projname=args.project_name))

  else: # header only library
    write_file(
        args,
        header_path,
        cpp_headers.standalone.substitute(projname=args.project_name))

def cmake_file(args):
  cml = None
  kind = args.kind
  if kind == KIND_EXE:
    cml = cmake_lists.executable
  elif kind == KIND_LIB:
    cml = cmake_lists.library
  elif kind == KIND_HEAD:
    cml = cmake_lists.header
  else:
    assert false

  return cml.substitute(
      projname=args.project_name,
      cxx_version=args.cxx_version)

