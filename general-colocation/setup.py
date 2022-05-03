import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="general-colocation",
    version="1.0.0",
    description="Discover colocation patterns from spatial datasets",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/andrew-lafortune/ColocationMiner",
    author="Andrew LaFortune",
    author_email="lafor038@umn.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["general-colocation"],
    include_package_data=True,
    install_requires=["pandas", "geopandas", "shapely", "numpy", "matplotlib", "imageio"],
    entry_points={
        "console_scripts": [
            "colocation=colocation.__main__:main",
        ]
    },
)