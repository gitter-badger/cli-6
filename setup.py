"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
Author <jacoby@sparkl.com> Jacoby Thwaites.

Setup specification for distutils.

Please note this file has the version number replaced by
the make target, and is copied to setup.py.
"""
from distutils.core import setup
from subprocess import check_output

setup(
  name="sparkl_cli",
  description="SPARKL command line utility",
  url="sparkl.com",
  author="Jacoby Thwaites",
  author_email="dev@sparkl.com",
  version="v1.0.0-1-g047ac1c",
  scripts=["sparkl"],
  packages=["sparkl_cli"])
