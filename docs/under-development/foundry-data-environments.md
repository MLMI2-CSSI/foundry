# Foundry Data Environments

Foundry Data Environments allow for a logical and portable way to specify and collect data for analyses. Data Environments help users get set up locally to access groups of specified datasets.&#x20;

This is comparable to a `package.json` file in an npm environment or a `requirements.txt` file in python environment.

## Data Environment Specification Fields

**`name`** : (string) A name for the data environment

**`version`** : (string) A version of the form \<major>.\<minor>.\<sub> e.g., "1.2.0"

**`description`**  : (string) A short description of the data environment and its intended use

**`tags`**  : (list) A list of tag strings associated with the data environment

**`dependencies`**  : (list) A list of dependency objects associated with the data environment

**`private`**  : (bool) Whether the data environment is to be registered in a public data environment index

### Dependency Objects

**`identifier`** : (string) Unique identifier for the dataset

**`version`** : (string) The version of the dataset to use

**`provider`** : (string) The dataset provider. _Currently only "MDF" is supported_

```javascript
{
    "identifier": "_test_foundry_mp_bandgap_v1.1",
    "version": "1.1",
    "provider": "MDF"
}
```

## Example Specification

```javascript
{
	"name": "Band Gap Analysis",
	"version": "1.0.0",
	"description": "Datasets for band gap uber model generation",
	"private": true,
	"dependencies": [{
			"name": "_test_foundry_experimental_bandgap_v1.1",
			"version": "1.1",
			"provider": "MDF"
		},
		{
			"name": "_test_foundry_mp_bandgap_v1.1",
			"version": "1.1",
			"provider": "MDF"
		},
		{
			"name": "_test_foundry_oqmd_bandgap_v1.1",
			"version": "1.1",
			"provider": "MDF"
		},
		{
			"name": "_test_foundry_assorted_computational_bandgap_v1.1",
			"version": "1.1",
			"provider": "MDF"
		}
	]
}
```

