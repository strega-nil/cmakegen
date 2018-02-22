from pathlib import Path
import pytest

from . import generate, files, options

class Generator(generate.Generator):
  def __init__(self):
    super().__init__()
    self.tree = {}

  def mkdir(self, path):
    assert path.parts

    dir = self.tree
    for p in path.parts[:-1]:
      assert p in dir
      dir = dir[p]
    dirname = path.parts[-1]
    assert dirname not in dir
    dir[dirname] = {}

  def write_file(self, path, to_write):
    assert path.parts

    dir = self.tree
    for p in path.parts[:-1]:
      assert p in dir
      dir = dir[p]
    filename = path.parts[-1]
    assert filename not in dir
    dir[filename] = to_write

class TestGenerator:
  def test_success(self):
    generator = Generator()
    generator.mkdir(Path("hello"))
    generator.mkdir(Path("hello/bar"))
    generator.write_file(Path("hello/foo"), "hello, world!")

    assert "hello" in generator.tree

    assert "bar" in generator.tree["hello"]
    assert not generator.tree["hello"]["bar"]

    assert "foo" in generator.tree["hello"]
    assert "hello, world!" == generator.tree["hello"]["foo"]

  def test_fail(self):
    generator = Generator()
    generator.mkdir(Path("hello"))
    generator.mkdir(Path("hello/bar"))
    generator.write_file(Path("hello/foo"), "hello, world!")

    with pytest.raises(AssertionError):
      generator.mkdir(Path(""))
    with pytest.raises(AssertionError):
      generator.write_file(Path(""), "hi")

    with pytest.raises(AssertionError):
      generator.mkdir(Path("hello"))

    with pytest.raises(AssertionError):
      generator.mkdir(Path("hello/bar"))
    with pytest.raises(AssertionError):
      generator.mkdir(Path("hello/foo"))

    with pytest.raises(AssertionError):
      generator.write_file(Path("hello"), "hello, world!")
    with pytest.raises(AssertionError):
      generator.write_file(Path("hello/foo"), "hello, world!")

def specific_flags(project_name, style, kind, standard):
  generator = Generator()
  generate.build_project(
      generator,
      project_name=project_name,
      style=style,
      kind=kind,
      standard=standard)

  tree = generator.tree

  assert project_name in tree
  proj = tree[project_name]

  assert "source" in proj
  assert "include" in proj
  assert project_name in proj["include"]

  assert "CMakeLists.txt" in proj
  assert (
      proj["CMakeLists.txt"]
      == generate.cmake_file(project_name, kind, standard))

  if style:
    assert ".clang-format" in proj
    if style == options.STYLE_NICOLETTE:
      assert proj[".clang-format"] == files.clang_format.nicolette
    else:
      assert False
  else:
    assert ".clang-format" not in proj

  if kind == options.KIND_EXE:
    assert "main.cpp" in proj["source"]
    assert (
        proj["source"]["main.cpp"]
        == files.cpp_files.executable.substitute(projname=project_name))

    header = project_name + ".h"
    assert header in proj["include"][project_name]
    assert (
        proj["include"][project_name][header]
        == files.cpp_headers.standalone.substitute(projname=project_name))

  elif kind == options.KIND_LIB:
    libfile = project_name + ".cpp"
    assert libfile in proj["source"]
    assert (
        proj["source"][libfile]
        == files.cpp_files.library.substitute(projname=project_name))

    header = project_name + ".h"
    assert header in proj["include"][project_name]
    assert (
        proj["include"][project_name][header]
        == files.cpp_headers.dependent.substitute(projname=project_name))

  elif kind == options.KIND_HEADER:
    header = project_name + ".h"
    assert header in proj["include"][project_name]
    assert (
        proj["include"][project_name][header]
        == files.cpp_headers.standalone.substitute(projname=project_name))
  else:
    assert False

def test_all_configurations():
  project_name = "foobar"
  styles = options.STYLE + (None,)
  for style in styles:
    for kind in options.KIND:
      for standard in options.STANDARD:
        specific_flags(project_name, style, kind, standard)
