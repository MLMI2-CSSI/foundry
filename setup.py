import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
packages = (setuptools.find_packages(),)
setuptools.setup(
    name="foundry_ml",
    version="1.2.0",
    author="""Aristana Scourtas, KJ Schmidt, Isaac Darling, Aadit Ambadkar, Braeden Cullen,
            Imogen Foster, Ribhav Bose, Zoa Katok, Ethan Truelove, Ian Foster, Ben Blaiszik""",
    author_email="blaiszik@uchicago.edu",
    packages=setuptools.find_packages(),
    description="Package to support simplified application of machine learning models to datasets in materials science",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "mdf_toolbox>=0.6.0",
        "globus-sdk>=3,<4",
        "dlhub_sdk>=1.0.0",
        "numpy>=1.15.4",
        "pandas>=0.23.4",
        "pydantic>=2.7.2",
        "mdf_connect_client>=0.5.0",
        "h5py>=2.10.0",
        "json2table",
        "openpyxl>=3.1.0",
        # CLI and agent support (core)
        "typer[all]>=0.9.0",
        "rich>=13.0.0",
    ],
    extras_require={
        "huggingface": [
            "datasets>=2.14.0",
            "huggingface_hub>=0.17.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "foundry=foundry.__main__:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
    ],
    keywords=["materials science", "machine learning", "datasets", "MCP", "AI agents"],
    license="MIT License",
    url="https://github.com/MLMI2-CSSI/foundry",
)
