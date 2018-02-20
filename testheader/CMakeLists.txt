cmake_minimum_required(VERSION 3.6)

project(libtestheader VERSION 0.1 LANGUAGES CXX)

add_library(libtestheader INTERFACE)

target_include_directories(libtestheader
  INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>)

target_compile_features(libtestheader INTERFACE cxx_std_14)

if(MSVC)
  target_compile_options(libtestheader
    INTERFACE
      /D_SCL_SECURE_NO_WARNINGS
      /permissive-)
endif()

