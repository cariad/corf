from pathlib import Path

from setuptools import find_packages, setup

from corf.version import get_version

readme_path = Path(__file__).parent.joinpath("README.md")

with open(readme_path, encoding="utf-8") as f:
    long_description = f.read()

classifiers = [
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Topic :: Internet",
    "Topic :: Security",
    "Topic :: Utilities",
]

version = get_version()

if "a" in version:
    classifiers.append("Development Status :: 3 - Alpha")
elif "b" in version:
    classifiers.append("Development Status :: 4 - Beta")
else:
    classifiers.append("Development Status :: 5 - Production/Stable")

classifiers.sort()

setup(
    author="Cariad Eccleston",
    author_email="cariad@cariad.me",
    classifiers=classifiers,
    description="AWS CodeArtifact authorisation token generator for CLI tools",
    entry_points={
        "console_scripts": [
            "corf=corf.__main__:cli_entry",
        ]
    },
    include_package_data=True,
    install_requires=[
        "pyyaml",
        "boto3",
    ],
    keywords=[
        "AWS",
        "Amazon Web Services",
        "CodeArtifact",
        "authorisation",
        "authorization",
        "token",
    ],
    license="MIT License",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="corf",
    packages=find_packages(),
    python_requires=">=3.8",
    url="https://github.com/cariad/corf",
    version=version,
)
