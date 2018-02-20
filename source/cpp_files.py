main_file = """\
#include <{projname}/{projname}.h>

int main() {{
  {projname}::say_hello();
}}
"""

library_file = """\
#include <{projname}/{projname}.h>

#include <iostream>

namespace {projname} {{

void say_hello() {{
  std::cout << "Hello, world!\\n";
}}

}}
"""

header_file_standalone = """\
#pragma once

#include <iostream>

namespace {projname} {{

inline void say_hello() {{
  std::cout << "Hello, world!\\n";
}}

}}
"""

header_file_dependent = """\
#pragma once

namespace {projname} {{

void say_hello();

}}
"""
