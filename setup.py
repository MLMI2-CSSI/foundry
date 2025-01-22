from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

# Core dependencies required for basic functionality
CORE_REQUIREMENTS = [
    "numpy>=1.15.4",
    "pandas>=0.23.4",
    "h5py>=2.10.0",
    "pillow>=9.0.0",  # For image loading
    "scipy>=1.7.0",
    "mdf_forge>=0.8.0",
    "globus-sdk>=3,<4",
    "pydantic>=2.7.2",
    "mdf_connect_client>=0.5.0",
    "json2table>=1.1.5",
    "openpyxl>=3.1.0",  # For Excel support
    "tqdm>=4.19.4",     # For progress bars
]

# Optional dependencies for specific features
EXTRAS_REQUIRE = {
    'molecular': ["rdkit>=2022.9.1"],
    'torch': ["torch>=1.8.0"],
    'tensorflow': ["tensorflow>=2.0.0"],
    'spectral': ["jcamp>=1.0.0"],
    'all': ["rdkit>=2022.9.1", 
            "torch>=1.8.0", 
            "tensorflow>=2.0.0",
            "jcamp>=1.0.0"]
}

setup(
    name="foundry_ml",
    version="1.0.4",
    author="""Aristana Scourtas, KJ Schmidt, Isaac Darling, Aadit Ambadkar, Braeden Cullen,
            Imogen Foster, Ribhav Bose, Zoa Katok, Ethan Truelove, Ian Foster, Ben Blaiszik""",
    author_email="blaiszik@uchicago.edu",
    packages=find_packages(),
    description="Package to support simplified application of machine learning models to datasets in materials science",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=CORE_REQUIREMENTS,
    extras_require=EXTRAS_REQUIRE,
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ],
    keywords=["materials science", "machine learning", "data science"],
    license="MIT License",
    url="https://github.com/MLMI2-CSSI/foundry",
)
