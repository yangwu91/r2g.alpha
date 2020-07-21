from setuptools import setup
import re
import os

with open('README.md', 'r') as inf:
    long_description = inf.read()

with open('{}/src/scripts/r2g'.format(os.path.split(os.path.abspath(__file__))[0]), 'r') as inf:
    version = re.findall(r'version = "(.+)"', inf.read())[0]

setup(
    name='r2g',
    version=version,
    license="MIT",
    url='https://github.com/yangwu91/r2g.git',
    author='Yang Wu',
    author_email='wuyang@drwu.ga',
    maintainer="Yang Wu",
    maintainer_email="wuyang@drwu.ga",
    description='A light-weight pipeline for identifying, retrieving, and assembling homologous genes utilizing the '
                'NCBI SRA database.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    scripts=['src/scripts/r2g'],
    py_modules=["r2g.errors", "r2g.warnings"],
    packages=[
        "r2g.main",
        "r2g.Bio",
        "r2g.local",
        "r2g.online"
    ],
    package_dir={"": "src"},
    package_data={"": ["*LICENSE*", "*path.json*"]},
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        # Technically the license is not OSI approved,
        # but almost there, so might put:
        "License :: OSI Approved :: MIT License",
        # "License :: Freely Distributable",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ],
    test_suite="nose.collector",
    tests_require=['nose']
)
