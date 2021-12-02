#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages

sys.path.insert(0, 'src')

from ditto import __version__

with open('README.md', 'rb') as readme_file:
    readme = readme_file.read().decode('utf-8')

needs_pytest = {'pytest', 'test'}.intersection(sys.argv)
setup_requirements = ['pytest-runner'] if needs_pytest else []
requirements = ['paho-mqtt==1.5.1']
test_requirements = ['pytest']

setup(
    name='ditto-client',
    version=__version__,
    description='Eclipse Ditto Client SDK for Python',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Gabriela Yoncheva, Ognian Baruh',
    author_email='fixed-term.Gabriela.Yoncheva@bosch.io, fixed-term.Ognyan.Baruh@bosch.io',
    url='https://eclipse.org/ditto/',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    include_package_data=True,
    install_requires=requirements,
    license='Eclipse Public License v2.0',
    zip_safe=False,
    keywords='ditto',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Digital Twins',
        'Topic :: Edge Applications'
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
    extras_require={
        'test': test_requirements
    },
    project_urls={
        'Bug Reports': 'https://github.com/eclipse/ditto-clients-python/issues',
        'Source': 'https://github.com/eclipse/ditto-clients-python'
    },
)
