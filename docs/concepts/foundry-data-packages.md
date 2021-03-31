# Foundry Data Packages

Foundry Data Packages allow for a logical and portable way to specify, and collect data for analyses. From a data package, a user can easily build a local data environment matching the data package.

## Data Package Specification Fields

**`name`** : \(string\) A name for the data package

**`version`** : \(string\) A version of the form &lt;major&gt;.&lt;minor&gt;.&lt;sub&gt; e.g., "1.2.0"

**`description`**  : \(string\) A short description of the data package and its intended use

**`tags`**  : \(list\) A list of tag strings associated with the data package

**`dependencies`**  : \(list\) A list of dependency objects associated with the data package

**`private`**  : \(bool\) Whether the data package is to be registered in a public data package index

### Dependency Objects

**`identifier`** : \(string\) Unique identifier for the dataset

**`version`** : \(string\) The version of the dataset to use

**`provider`** : \(string\) The dataset provider. _Currently only "MDF" is supported_

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



