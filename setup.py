from pathlib import Path

from setuptools import find_packages, setup

from cauth.version import get_version

readme_path = Path(__file__).parent.joinpath("README.md")

with open(readme_path, encoding="utf-8") as f:
    long_description = f.read()

setup(
    author="Cariad Eccleston",
    author_email="cariad@cariad.me",
    description="AWS CodeArtifact authorisation token generator for CLI tools",
    entry_points={
        "console_scripts": [
            "cauth=cauth.__main__:cli_entry",
        ]
    },
    include_package_data=True,
    install_requires=[
        "pyyaml",
        "boto3",
    ],
    license="MIT License",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="corf",
    packages=find_packages(),
    python_requires=">=3.8",
    version=get_version(),
)
