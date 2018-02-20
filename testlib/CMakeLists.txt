cmake_minimum_required(VERSION 3.6)

project(libtestlib VERSION 0.1 LANGUAGES CXX)

add_library(libtestlib
  source/library.cpp)

target_include_directories(libtestlib PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
    PRIVATE source)

target_compile_features(libtestlib PUBLIC cxx_std_14)

if(MSVC)
  # hack to deal with cmake automatically inserting /W3
  # stolen from llvm
  string(REGEX REPLACE " /W[0-4]" "" CMAKE_C_FLAGS "${CMAKE_C_FLAGS}")
  string(REGEX REPLACE " /W[0-4]" "" CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")

  target_compile_options(libtestlib
    PUBLIC
      /D_SCL_SECURE_NO_WARNINGS
    PRIVATE
      /W4 /WX)
else()
  target_compile_options(libtestlib
    PRIVATE
      -Wall -Wextra -Werror)
endif()
