from codecs import open
from os import path
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="datakick",
    version="0.0.1",
    description="",
    long_description=long_description,
    url="https://github.com/carlos-a-rodriguez/datakick",
    author="Carlos A. Rodriguez",
    author_email="carlos.rodriguez@protonmail.ch",
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords="datakick barcode upc ean product",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires=["requests", "six"],
    extras_require={
        "dev": [],
        "test": ["mock", "requests", "six"]
    },
    package_data={},
    data_files=[],
    entry_points={},
)
