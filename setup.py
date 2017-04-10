from setuptools import setup

setup(
    name = "emuparadise",
    packages = ["emuparadise"],
    entry_points = {
        "console_scripts": ['emuparadise = emuparadise.emuparadise:main']
        },
    version = "0.1.0",
    description = "A tool for getting files from emuparadise",
    author = "Steven Smith",
    author_email = "stevensmith.ome@gmail.com",
    license = "MIT",
    classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3",
        "Intended Audience :: End Users/Desktop",
        ]
    )
