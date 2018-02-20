executable = """\
cmake_minimum_required(VERSION 3.6)

project({projname} VERSION 0.1 LANGUAGES CXX)

add_executable({projname}
  source/main.cpp)

target_include_directories({projname} PUBLIC
    $<BUILD_INTERFACE:${{CMAKE_CURRENT_SOURCE_DIR}}/include>
    $<INSTALL_INTERFACE:include>
    PRIVATE source)

target_compile_features({projname} PUBLIC cxx_std_{cxx_version})

if(MSVC)
  # hack to deal with cmake automatically inserting /W3
  # stolen from llvm
  string(REGEX REPLACE " /W[0-4]" "" CMAKE_C_FLAGS "${{CMAKE_C_FLAGS}}")
  string(REGEX REPLACE " /W[0-4]" "" CMAKE_CXX_FLAGS "${{CMAKE_CXX_FLAGS}}")

  target_compile_options({projname}
    PUBLIC
      /D_SCL_SECURE_NO_WARNINGS
    PRIVATE
      /W4 /WX)
else()
  target_compile_options({projname}
    PRIVATE
      -Wall -Wextra -Werror)
endif()
"""

library = """\
cmake_minimum_required(VERSION 3.6)

project(lib{projname} VERSION 0.1 LANGUAGES CXX)

add_library(lib{projname}
  source/library.cpp)

target_include_directories(lib{projname} PUBLIC
    $<BUILD_INTERFACE:${{CMAKE_CURRENT_SOURCE_DIR}}/include>
    $<INSTALL_INTERFACE:include>
    PRIVATE source)

target_compile_features(lib{projname} PUBLIC cxx_std_{cxx_version})

if(MSVC)
  # hack to deal with cmake automatically inserting /W3
  # stolen from llvm
  string(REGEX REPLACE " /W[0-4]" "" CMAKE_C_FLAGS "${{CMAKE_C_FLAGS}}")
  string(REGEX REPLACE " /W[0-4]" "" CMAKE_CXX_FLAGS "${{CMAKE_CXX_FLAGS}}")

  target_compile_options(lib{projname}
    PUBLIC
      /D_SCL_SECURE_NO_WARNINGS
    PRIVATE
      /W4 /WX)
else()
  target_compile_options(lib{projname}
    PRIVATE
      -Wall -Wextra -Werror)
endif()
"""

header_library = """\
cmake_minimum_required(VERSION 3.6)

project(lib{projname} VERSION 0.1 LANGUAGES CXX)

add_library(lib{projname} INTERFACE)

target_include_directories(lib{projname}
  INTERFACE
    $<BUILD_INTERFACE:${{CMAKE_CURRENT_SOURCE_DIR}}/include>
    $<INSTALL_INTERFACE:include>)

target_compile_features(lib{projname} INTERFACE cxx_std_{cxx_version})
"""