import pkg_resources
from string import Template

def get_file(data_file):
  filename = pkg_resources.resource_filename(__name__, "data/" + data_file)
  with open(filename, "rt") as file:
    return file.read()

def get_template(data_file):
  return Template(get_file(data_file))

