import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
packages = (setuptools.find_packages(),)
# TODO: change dependencies to be looser
setuptools.setup(
    name="foundry_ml",
    version="0.1.0",
    author="Aristana Scourtas, KJ Schmidt, Imogen Foster, Ribhav Bose, Zoa Katok, Ethan Truelove, Ian Foster, Ben Blaiszik",
    author_email="blaiszik@uchicago.edu",
    packages=setuptools.find_packages(),
    description="Package to support simplified application of machine learning models to datasets in materials science",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "mdf_forge>=0.7.6",
        "numpy>=1.15.4",
        "pandas>=0.23.4",
        "pydantic>=1.4",
        "mdf_connect_client>=0.3.8",
        "h5py>=2.10.0",
        "json2table"
    ],
    python_requires=">=3.6",
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
