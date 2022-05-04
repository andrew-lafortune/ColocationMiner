import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="general-colocation",
    version="1.0.5",
    description="Discover colocation patterns from spatial datasets",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/andrew-lafortune/ColocationMiner/tree/master/general-colocation",
    author="Andrew LaFortune",
    author_email="lafor038@umn.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pandas", "geopandas", "shapely", "numpy", "matplotlib", "imageio"],
    entry_points={
        "console_scripts": [
            "colocation=general_colocation:colocation.main",
        ]
    },
)