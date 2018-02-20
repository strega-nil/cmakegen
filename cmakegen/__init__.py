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
      metavar="N")
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

  args = ap.parse_args()
  #build_project(args)
  print(
      cmake_lists.executable.substitute(
        projname=args.project_name,
        cxx_version=args.std))

def build_project(args):
  proj_dir = Path(Path.cwd(), args.project_name)
  proj_dir.mkdir(exist_ok=args.force)
  
  source_dir = Path(proj_dir, "source")
  source_dir.mkdir(exist_ok=args.force)

  include_dir = Path(proj_dir, "include")
  include_dir.mkdir(exist_ok=args.force)

  proj_include_dir = Path(include_dir, args.project_name)
  proj_include_dir.mkdir(exist_ok=args.force)

  cmake_path = Path(proj_dir, "CMakeLists.txt")
  with cmake_path.open(mode="w") as cmakelists:
    cmakelists.write(cmake_file(args))

  header_filename = args.project_name + ".h"

  if args.kind == KIND_EXE:
    with Path(proj_include_dir, header_filename).open(mode="w") as header:
      header.write(
          cpp_headers.standalone.substitute(projname=args.project_name))
    with Path(source_dir, "main.cpp").open(mode="w") as main:
      main.write(cpp_files.executable.substitute(projname=args.project_name))

  elif args.kind == KIND_LIB:
    with Path(proj_include_dir, header_filename).open(mode="w") as header:
      header.write(
          cpp_headers.dependent.substitute(projname=args.project_name))
    lib_file = args.project_name + ".cpp"
    with Path(source_dir, lib_file).open(mode="w") as lib:
      lib.write(cpp_files.library.substitute(projname=args.project_name))

  else: # header only library
    with Path(proj_include_dir, header_filename).open(mode="w") as header:
      header.write(
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

  return cml.substitute(projname=args.project_name, cxx_version=args.std)

