import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
packages = (setuptools.find_packages(),)
setuptools.setup(
    name="foundry_ml",
    version="0.7.5",
    author="""Aristana Scourtas, KJ Schmidt, Isaac Darling, Aadit Ambadkar, Braeden Cullen,
            Imogen Foster, Ribhav Bose, Zoa Katok, Ethan Truelove, Ian Foster, Ben Blaiszik""",
    author_email="blaiszik@uchicago.edu",
    packages=setuptools.find_packages(),
    description="Package to support simplified application of machine learning models to datasets in materials science",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "mdf_forge>=0.8.0",
        "globus-sdk>=3,<4",
        "numpy>=1.15.4",
        "pandas>=0.23.4",
        "pydantic<2.0.0",
        "mdf_connect_client>=0.5.0",
        "h5py>=2.10.0",
        "json2table"
    ],
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
    keywords=[],
    license="MIT License",
    url="https://github.com/MLMI2-CSSI/foundry",
)
