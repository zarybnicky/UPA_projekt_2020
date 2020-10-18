{ pkgs ? import <nixpkgs> {} }:
with pkgs.python36Packages; buildPythonApplication {
  name = "upa";
  propagatedBuildInputs = [
    flake8
    mypy
    numpy
    pylint
    python-dateutil
    requests
  ];
}
