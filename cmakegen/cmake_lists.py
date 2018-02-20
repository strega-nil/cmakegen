from . import templates


def msvc_warning_hackify(template):
  from string import Template
  actual_hack = """\
# hack to deal with cmake automatically inserting /W3
  # stolen from llvm
  string(REGEX REPLACE " /W[0-4]" "" CMAKE_C_FLAGS "$${CMAKE_C_FLAGS}")
  string(REGEX REPLACE " /W[0-4]" "" CMAKE_CXX_FLAGS "$${CMAKE_CXX_FLAGS}")\
"""
  file = templates.get(template)
  file.template = file.template.replace("$MSVC_WARNING_HACK", actual_hack)
  return file

executable = msvc_warning_hackify("CMakeLists_exe.txt")
library = templates.get("CMakeLists_lib.txt")
header = templates.get("CMakeLists_head.txt")
