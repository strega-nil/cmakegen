cmake_minimum_required(VERSION 3.6)

project(testheader VERSION 0.1 LANGUAGES CXX)

add_library(testheader INTERFACE)

target_include_directories(testheader
  INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>)

target_compile_features(testheader INTERFACE cxx_std_14)

if(MSVC)
  # hack to deal with cmake automatically inserting /W3
  # stolen from llvm
  string(REGEX REPLACE " /W[0-4]" "" CMAKE_C_FLAGS "${CMAKE_C_FLAGS}")
  string(REGEX REPLACE " /W[0-4]" "" CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")

  target_compile_options(testheader
    INTERFACE
      /D_SCL_SECURE_NO_WARNINGS
      /permissive-)
endif()
