cmake_minimum_required(VERSION 3.6)

project(testexe VERSION 0.1 LANGUAGES CXX)

add_executable(testexe
  source/main.cpp)

target_include_directories(testexe
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
  PRIVATE
    source)

target_compile_features(testexe PUBLIC cxx_std_14)

if(MSVC)
  # hack to deal with cmake automatically inserting /W3
  # stolen from llvm
  string(REGEX REPLACE " /W[0-4]" "" CMAKE_C_FLAGS "${CMAKE_C_FLAGS}")
  string(REGEX REPLACE " /W[0-4]" "" CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")

  target_compile_options(testexe
    PUBLIC
      /D_SCL_SECURE_NO_WARNINGS
      /permissive-
    PRIVATE
      /W4
      /WX)
else()
  target_compile_options(testexe
    PRIVATE
      -Wall
      -Wextra
      -pedantic
      -Werror)
endif()
