import pkg_resources
from string import Template

def get(data_file):
  filename = pkg_resources.resource_filename(__name__, "data/" + data_file)
  with open(filename, "rt") as file:
    return Template(file.read())

