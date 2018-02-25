from string import Template
from .data import get_template, get_file

class cpp_headers:
  standalone = get_template("standalone.h")
  dependent = get_template("dependent.h")

class cpp_files:
  executable = get_template("executable.cpp")
  library = get_template("library.cpp")

class clang_format:
  nicolette = get_file("nicolette.clang-format")

def _cmake_list_get(name):
  file = get_file("cmake/base_" + name + ".txt")
  file = file.replace("/header/", get_file("cmake/header.txt"))
  file = file.replace(
      "/include_directories/", get_file("cmake/include_directories.txt"))
  file = file.replace(
      "/include_directories_headers/",
      get_file("cmake/include_directories_headers.txt"))

  file = file.replace(
      "/flags_interface/", get_file("cmake/flags_interface.txt"))
  file = file.replace(
      "/warnings/", get_file("cmake/warnings.txt"))

  return Template(file)

class cmake_lists:
  executable = _cmake_list_get("exe")
  library = _cmake_list_get("lib")
  header = _cmake_list_get("header")
