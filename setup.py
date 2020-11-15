from setuptools import find_packages, setup

from cauth.version import get_version

setup(
    name="corf",
    version=get_version(),
    description="""
`corf` is an AWS CodeArtifact authorization helper for `pipenv` and other command line
tools that read CodeArtifact authorization tokens.""",
    author="Cariad Eccleston",
    author_email="cariad@cariad.me",
    license="MIT License",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "cauth=cauth.__main__:cli_entry",
        ]
    },
    install_requires=[
        "pyyaml",
        "boto3",
    ],
    python_requires=">=3.8",
    include_package_data=True,
)
