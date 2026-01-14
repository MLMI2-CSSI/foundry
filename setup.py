import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
packages = (setuptools.find_packages(),)
setuptools.setup(
    name="foundry_ml",
    version="1.2.1",
    author="""Aristana Scourtas, KJ Schmidt, Isaac Darling, Aadit Ambadkar, Braeden Cullen,
            Imogen Foster, Ribhav Bose, Zoa Katok, Ethan Truelove, Ian Foster, Ben Blaiszik""",
    author_email="blaiszik@uchicago.edu",
    packages=setuptools.find_packages(),
    description="Package to support simplified application of machine learning models to datasets in materials science",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "mdf_toolbox>=0.7.1",
        "globus-sdk>=3,<4",
        "mdf_connect_client>=0.5.0",
        "requests>=2.31.0",
        "tqdm>=4.66.0",
        "numpy>=2.0.0",
        "pandas>=2.2.2",
        "h5py>=3.11.0",
        "pydantic>=2.7.2",
        "json2table>=1.1.5",
        # CLI and agent support (core)
        "typer>=0.12.0",
        "rich>=13.7.0",
    ],
    extras_require={
        "torch": [
            "torch>=2.1.0",
        ],
        "tensorflow": [
            "tensorflow>=2.12.0",
        ],
        "excel": [
            "openpyxl>=3.1.0",
        ],
        "huggingface": [
            "datasets>=2.14.0",
            "huggingface_hub>=0.17.0",
        ],
        "examples": [
            "scikit-learn>=1.4.0",
        ],
        "dev": [
            "pytest>=7.4",
            "pytest-cov>=4.1",
            "pytest-mock>=3.12",
            "flake8>=7.0",
            "jsonschema>=4.19",
            "mock>=5.1",
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
