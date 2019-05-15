#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup


setup_kwargs = dict(
    test_suite='tests',
    long_description_content_type="text/markdown",
)

try:
    setup(
        use_scm_version=True,
        **setup_kwargs
    )
except LookupError:
    # This means the source code was not from git / PyPI
    setup(
        version='0.0.2b0',
        **setup_kwargs
    )

