import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wui",
    version="1.1.7",
    author="ShangXian Wang",
    author_email="997049907@qq.om",
    description="将wui的代码放到__init__中",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shangxianw/wsxpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)