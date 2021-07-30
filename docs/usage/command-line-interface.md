# Command Line Interface \(CLI\)

The Foundry command line interface \(CLI\) allows for users to build their data environment from the command line using a specification file. This is the data analag to how `pip` or `conda` allow users to build a software environment from software specification files.

## Installation

```text
pip install foundry-ml-cli
```

### CLI Options

**`--file`** : \(string\) the name of the specification file to build. _Default: "./foundry.json"_

**`--globus`** : \(bool\) If True, uses Globus to download the files, otherwise HTTPS. _Default: False_

**`--interval`** : \(int\) Time in seconds between polling operations to check transfer status. _Default: 3_

**`-verbose`** : \(bool\) If True, print out more logging information to the console. _Default: False_

## Example Usage

In a folder containing a file named foundry.json

```text
/foundry.json


$ foundry
```

This is the same as running

```text
/foundry.json


$ foundry --file=foundry.json --globus=False --interval=3 --verbose=False
```

