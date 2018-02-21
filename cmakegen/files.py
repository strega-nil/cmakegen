from .data import get_template, get_file

class cpp_headers:
  standalone = get_template("standalone.h")
  dependent = get_template("dependent.h")

class cpp_files:
  executable = get_template("executable.cpp")
  library = get_template("library.cpp")

class clang_format:
  nicolette = get_file("nicolette.clang-format")


def _msvc_warning_hackify(template):
  from string import Template
  actual_hack = """\
# hack to deal with cmake automatically inserting /W3; taken from llvm
  string(REGEX REPLACE " /W[0-4]" "" CMAKE_C_FLAGS "$${CMAKE_C_FLAGS}")
  string(REGEX REPLACE " /W[0-4]" "" CMAKE_CXX_FLAGS "$${CMAKE_CXX_FLAGS}")\
"""
  file = get_template(template)
  file.template = file.template.replace("$msvc_warning_hack", actual_hack)
  return file

class cmake_lists:
  executable = _msvc_warning_hackify("CMakeLists_exe.txt")
  library = _msvc_warning_hackify("CMakeLists_lib.txt")
  header = _msvc_warning_hackify("CMakeLists_head.txt")
