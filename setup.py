from setuptools import setup, find_packages

setup(
  name="cmakegen",
  version="0.1",
  packages=find_packages(),
  package_data={"cmakegen": ["data/*"]},
  entry_points={"console_scripts": ["cmakegen=cmakegen:main"]},
  
  author="Nicole Mazzuca",
  author_email="npmazzuca@gmail.com",
  description="Generate a CMake project, in the spirit of cargo-new",
  license="MIT",
  keywords="cmake cxx cpp build")
