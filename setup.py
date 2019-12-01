import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aoc_utils",
    version="0.0.4",
    author="Logan McDonald",
    author_email="loganmcdona11@gmail.com",
    description="A aoc_utils package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/loganmeetsworld/aoc-utils",
    packages=['aoc_utils'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
