import os
import re
import types

import mdf_toolbox
import pytest
from mdf_forge import Forge

# Sample results for download testing
example_result1 = {
    "mdf": {
        "resource_type": "record"
    },
    "files": [{
        "globus": "globus://82f1b5c6-6e9b-11e5-ba47-22000b92c6ec/test/test_fetch.txt",
        "url": "https://data.materialsdatafacility.org/test/test_fetch.txt"
    }]
}
example_result2 = [{
    "mdf": {
        "resource_type": "record"
    },
    "files": [{
        "globus": "globus://82f1b5c6-6e9b-11e5-ba47-22000b92c6ec/test/test_fetch.txt",
        "url": "https://data.materialsdatafacility.org/test/test_fetch.txt"
    }]
}, {
    "mdf": {
        "resource_type": "record"
    },
    "files": [{
        "globus": "globus://82f1b5c6-6e9b-11e5-ba47-22000b92c6ec/test/test_multifetch.txt",
        "url": "https://data.materialsdatafacility.org/test/test_multifetch.txt"
    }]
}, {
    "mdf": {
        "resource_type": "record"
    },
    "files": [{
        "globus": ("globus://e38ee745-6d04-11e5-ba46-22000b92c6ec"
                   "/MDF/mdf_connect/test_files/petrel_fetch.txt"),
        "url": ("https://e38ee745-6d04-11e5-ba46-22000b92c6ec.e.globus.org"
                "/MDF/mdf_connect/test_files/petrel_fetch.txt")
    }]
}, {
    "mdf": {
        "resource_type": "record"
    },
    "files": [{
        "globus": ("globus://e38ee745-6d04-11e5-ba46-22000b92c6ec"
                   "/MDF/mdf_connect/test_files/petrel_multifetch.txt"),
        "url": ("https://e38ee745-6d04-11e5-ba46-22000b92c6ec.e.globus.org"
                "/MDF/mdf_connect/test_files/petrel_multifetch.txt")
    }]
}]
example_result3 = {
    "mdf": {
        "resource_type": "record"
    },
    "files": [{
        "globus": "globus://82f1b5c6-6e9b-11e5-ba47-22000b92c6ec/test/test_fetch.txt",
        "url": "https://data.materialsdatafacility.org/test/test_fetch.txt"
    }, {
        "globus": "globus://82f1b5c6-6e9b-11e5-ba47-22000b92c6ec/test/test_multifetch.txt",
        "url": "https://data.materialsdatafacility.org/test/test_multifetch.txt"
    }, {
        "globus": ("globus://e38ee745-6d04-11e5-ba46-22000b92c6ec"
                   "/MDF/mdf_connect/test_files/petrel_fetch.txt"),
        "url": ("https://e38ee745-6d04-11e5-ba46-22000b92c6ec.e.globus.org"
                "/MDF/mdf_connect/test_files/petrel_fetch.txt")
    }, {
        "globus": ("globus://e38ee745-6d04-11e5-ba46-22000b92c6ec"
                   "/MDF/mdf_connect/test_files/petrel_multifetch.txt"),
        "url": ("https://e38ee745-6d04-11e5-ba46-22000b92c6ec.e.globus.org"
                "/MDF/mdf_connect/test_files/petrel_multifetch.txt")
    }]
}
# NOTE: This example file does not exist
example_result_missing = {
    "mdf": {
        "resource_type": "record"
    },
    "files": [{
        "globus": "globus://82f1b5c6-6e9b-11e5-ba47-22000b92c6ec/test/should_not_exist.txt",
        "url": "https://data.materialsdatafacility.org/test/should_not_exist.txt"
    }]
}
example_dataset = {
    "mdf": {
        "resource_type": "dataset",
        "source_id": "foobar_v1"
    },
    "data": {
        "endpoint_path": ("globus://e38ee745-6d04-11e5-ba46-22000b92c6ec"
                          "/MDF/mdf_connect/test_files/")
    }
}
example_bad_resource = {
    "mdf": {
        "resource_type": "foobar"
    }
}


# Helper
# Return codes:
#  -1: No match, the value was never found
#   0: Exclusive match, no values other than argument found
#   1: Inclusive match, some values other than argument found
#   2: Partial match, value is found in some but not all results
def check_field(res, field, regex):
    dict_path = ""
    for key in field.split("."):
        if key == "[]":
            dict_path += "[0]"
        else:
            dict_path += ".get('{}', {})".format(key, "{}")
    # If no results, set matches to false
    all_match = (len(res) > 0)
    only_match = (len(res) > 0)
    some_match = False
    for r in res:
        vals = eval("r"+dict_path)
        if vals == {}:
            vals = []
        elif type(vals) is not list:
            vals = [vals]
        # If a result does not contain the value, no match
        if regex not in vals and not any([re.search(str(regex), str(value)) for value in vals]):
            all_match = False
            only_match = False
        # If a result contains other values, inclusive match
        elif len(vals) != 1:
            only_match = False
            some_match = True
        else:
            some_match = True

    if only_match:
        # Exclusive match
        return 0
    elif all_match:
        # Inclusive match
        return 1
    elif some_match:
        # Partial match
        return 2
    else:
        # No match
        return -1


def test_forge_match_source_names():
    os.system('echo hello')
    f = Forge(index="mdf", no_local_server=True, no_browser=True)
    os.system('echo there')
    assert True
    # One source
    f.match_source_names("khazana_vasp")
    res1 = f.search()
    assert res1 != []
    assert check_field(res1, "mdf.source_name", "khazana_vasp") == 0

    # Multi-source, strip version info
    f.match_source_names(["khazana_vasp", "ta_melting_v3.4"])
    res2 = f.search()

    # res1 is a subset of res2
    assert len(res2) > len(res1)
    assert all([r1 in res2 for r1 in res1])
    assert check_field(res2, "mdf.source_name", "ta_melting") == 2

    # No source
    assert f.match_source_names("") == f


def test_forge_test_match_records():
    f = Forge(index="mdf")
    # One record
    f.match_records("cip", 1006)
    res = f.search()
    assert len(res) == 1
    assert check_field(res, "mdf.source_name", "cip") == 0
    assert check_field(res, "mdf.scroll_id", 1006) == 0

    # Multi-record, strip version info
    f.match_records("cip_v3.4", [1006, 1002])
    res = f.search()
    assert len(res) == 2
    assert check_field(res, "mdf.source_name", "cip") == 0
    assert check_field(res, "mdf.scroll_id", 1006) == 2

    # No args
    assert f.match_records("", "") == f


def test_forge_match_elements():
    f = Forge(index="mdf")
    # One element
    f.match_elements("Al")
    res1 = f.search()
    assert res1 != []
    check_val1 = check_field(res1, "material.elements", "Al")
    assert check_val1 == 0 or check_val1 == 1

    # Multi-element
    f.match_elements(["Al", "Cu"])
    res2 = f.search()
    assert check_field(res2, "material.elements", "Al") == 1
    assert check_field(res2, "material.elements", "Cu") == 1

    # No elements
    assert f.match_elements("") == f


def test_forge_match_titles():
    # One title
    f = Forge(index="mdf")
    titles1 = '"High-throughput Ab-initio Dilute Solute Diffusion Database"'
    res1 = f.match_titles(titles1).search()
    assert res1 != []
    assert check_field(res1, "dc.titles.[].title",
                       "High-throughput Ab-initio Dilute Solute Diffusion Database") == 0

    # Multiple titles
    titles2 = [
        '"High-throughput Ab-initio Dilute Solute Diffusion Database"',
        '"Khazana (VASP)"'
    ]
    res2 = f.match_titles(titles2).search()
    assert res2 != []
    assert check_field(res2, "dc.titles.[].title", "Khazana (VASP)") == 2

    # No titles
    assert f.match_titles("") == f


def test_forge_match_years(capsys):
    # One year of data/results
    f = Forge(index="mdf")
    res1 = f.match_years("2015").search()
    assert res1 != []
    assert check_field(res1, "dc.publicationYear", 2015) == 0

    # Multiple years
    res2 = f.match_years(years=["2015", 2016]).search()
    assert check_field(res2, "dc.publicationYear", 2016) == 2

    # Wrong input
    with pytest.raises(AttributeError) as excinfo:
        f.match_years(["20x5"]).search()
    assert "Invalid year: '20x5'" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        f.match_years(start="20x5").search()
    assert "Invalid start year: '20x5'" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        f.match_years(stop="20x5").search()
    assert "Invalid stop year: '20x5'" in str(excinfo.value)

    # No filters with no input
    f.match_years()
    assert f.current_query() == ""

    # Test range
    res4 = f.match_years(start=2015, stop=2015, inclusive=True).search()
    assert check_field(res4, "dc.publicationYear", 2015) == 0

    res5 = f.match_years(start=2014, stop=2017, inclusive=False).search()
    assert check_field(res5, "dc.publicationYear", 2013) == -1
    assert check_field(res5, "dc.publicationYear", 2014) == -1
    assert check_field(res5, "dc.publicationYear", 2015) == 2
    assert check_field(res5, "dc.publicationYear", 2016) == 2
    assert check_field(res5, "dc.publicationYear", 2017) == -1

    assert f.match_years(start=2015, stop=2015, inclusive=False).search() == []


def test_forge_match_resource_types():
    f = Forge(index="mdf")
    # Test one type
    f.match_resource_types("record")
    res1 = f.search(limit=10)
    assert check_field(res1, "mdf.resource_type", "record") == 0

    # Test two types
    f.match_resource_types(["collection", "dataset"])
    res2 = f.search()
    assert check_field(res2, "mdf.resource_type", "record") == -1

    # Test zero types
    assert f.match_resource_types("") == f


def test_forge_match_organizations():
    f = Forge(index="mdf")
    # One repo
    f.match_organizations("NIST")
    res1 = f.search()
    assert res1 != []
    check_val1 = check_field(res1, "mdf.organizations", "NIST")
    assert check_val1 == 1

    # Multi-repo
    f.match_organizations(["NIST", "PRISMS"], match_all=False)
    res2 = f.search()
    assert check_field(res2, "mdf.organizations", "PRISMS") == 2
    assert check_field(res2, "mdf.organizations", "NIST") == 2

    # No repos
    assert f.match_organizations("") == f


def test_forge_match_dois():
    f = Forge(index="mdf")
    # One doi
    f.match_dois("https://dx.doi.org/10.13011/M3B36G")
    res1 = f.search()
    assert res1 != []
    assert check_field(res1, "dc.identifier.identifier", "https://dx.doi.org/10.13011/M3B36G") == 0

    # Multiple dois
    f.match_dois(["https://dx.doi.org/10.13011/M3B36G", "10.18126/M23P9G"])
    res2 = f.search()

    # # res1 is ça subset of res2
    assert len(res2) > len(res1)
    assert all([r1 in res2 for r1 in res1])
    assert check_field(res2, "dc.identifier.identifier", "10.18126/M23P9G") == 2

    # No doi
    assert f.match_dois("") == f


def test_forge_search_by_elements():
    f = Forge(index="mdf")
    elements = ["Cu", "Al"]
    sources = ["oqmd", "nist_xps_db"]
    res1, info1 = f.match_source_names(sources).match_elements(elements).search(limit=10000,
                                                                                info=True)
    res2, info2 = f.search_by_elements(elements, sources, limit=10000, info=True)
    assert all([r in res2 for r in res1]) and all([r in res1 for r in res2])
    assert check_field(res1, "material.elements", "Al") == 1
    assert check_field(res1, "mdf.source_name", "oqmd") == 2


def test_forge_search_by_titles():
    f = Forge(index="mdf")
    titles1 = ['"High-throughput Ab-initio Dilute Solute Diffusion Database"']
    res1 = f.search_by_titles(titles1)
    assert check_field(res1, "dc.titles.[].title",
                       "High-throughput Ab-initio Dilute Solute Diffusion Database") == 0

    titles2 = ["Database"]
    res2 = f.search_by_titles(titles2)
    assert check_field(res2, "dc.titles.[].title",
                       "NIST X-ray Photoelectron Spectroscopy Database") == 2


def test_forge_search_by_dois():
    f = Forge(index="mdf")
    res1 = f.search_by_dois("https://dx.doi.org/10.13011/M3B36G")
    assert check_field(res1, "dc.identifier.identifier", "https://dx.doi.org/10.13011/M3B36G") == 0


def test_forge_aggregate_sources():
    # Test limit
    f = Forge(index="mdf")
    res1 = f.aggregate_sources("nist_xps_db")
    assert isinstance(res1, list)
    assert len(res1) > 10000
    assert isinstance(res1[0], dict)


def test_forge_fetch_datasets_from_results():
    # Get some results
    f = Forge(index="mdf")
    # Record from OQMD
    res01 = f.search("mdf.source_name:oqmd AND mdf.resource_type:record", advanced=True, limit=1)
    # Record from OQMD with info
    res02 = f.search("mdf.source_name:oqmd AND mdf.resource_type:record",
                     advanced=True, limit=1, info=True)
    # Records from JANAF
    res03 = f.search("mdf.source_name:khazana_vasp AND mdf.resource_type:record",
                     advanced=True, limit=2)
    # Dataset for NIST XPS DB
    res04 = f.search("mdf.source_name:nist_xps_db AND mdf.resource_type:dataset", advanced=True)

    # Get the correct dataset entries
    oqmd = f.search("mdf.source_name:oqmd AND mdf.resource_type:dataset", advanced=True)[0]
    khazana_vasp = f.search("mdf.source_name:khazana_vasp AND mdf.resource_type:dataset",
                            advanced=True)[0]

    # Fetch single dataset
    res1 = f.fetch_datasets_from_results(res01[0])
    assert mdf_toolbox.insensitive_comparison(res1[0], oqmd)

    # Fetch dataset with results + info
    res2 = f.fetch_datasets_from_results(res02)
    assert mdf_toolbox.insensitive_comparison(res2[0], oqmd)

    # Fetch multiple datasets
    rtemp = res01+res03
    res3 = f.fetch_datasets_from_results(rtemp)
    assert len(res3) == 2
    assert oqmd in res3
    assert khazana_vasp in res3

    # Fetch dataset from dataset
    res4 = f.fetch_datasets_from_results(res04)
    assert mdf_toolbox.insensitive_comparison(res4, res04)

    # Fetch entries from current query
    f.match_source_names("nist_xps_db")
    assert f.fetch_datasets_from_results() == res04

    # Fetch nothing
    unknown_entry = {"mdf": {"resource_type": "unknown"}}
    assert f.fetch_datasets_from_results(unknown_entry) == []

'''
def test_forge_http_download(capsys):
    f = Forge(index="mdf")
    # Simple case
    f.http_download(example_result1)
    assert os.path.exists("./test_fetch.txt")

    # Test conflicting filenames
    f.http_download(example_result1)
    assert os.path.exists("./test_fetch(1).txt")
    f.http_download(example_result1)
    assert os.path.exists("./test_fetch(2).txt")
    os.remove("./test_fetch.txt")
    os.remove("./test_fetch(1).txt")
    os.remove("./test_fetch(2).txt")

    # With dest and preserve_dir, and tuple of results
    dest_path = os.path.expanduser("~/mdf")
    f.http_download(([example_result1], {"info": None}), dest=dest_path, preserve_dir=True)
    assert os.path.exists(os.path.join(dest_path, "test", "test_fetch.txt"))
    os.remove(os.path.join(dest_path, "test", "test_fetch.txt"))
    os.rmdir(os.path.join(dest_path, "test"))

    # With multiple files
    f.http_download(example_result2, dest=dest_path)
    assert os.path.exists(os.path.join(dest_path, "test_fetch.txt"))
    assert os.path.exists(os.path.join(dest_path, "test_multifetch.txt"))
    assert os.path.exists(os.path.join(dest_path, "petrel_fetch.txt"))
    assert os.path.exists(os.path.join(dest_path, "petrel_multifetch.txt"))
    os.remove(os.path.join(dest_path, "test_fetch.txt"))
    os.remove(os.path.join(dest_path, "test_multifetch.txt"))
    os.remove(os.path.join(dest_path, "petrel_fetch.txt"))
    os.remove(os.path.join(dest_path, "petrel_multifetch.txt"))

    f.http_download(example_result3, dest=dest_path)
    assert os.path.exists(os.path.join(dest_path, "test_fetch.txt"))
    assert os.path.exists(os.path.join(dest_path, "test_multifetch.txt"))
    assert os.path.exists(os.path.join(dest_path, "petrel_fetch.txt"))
    assert os.path.exists(os.path.join(dest_path, "petrel_multifetch.txt"))
    os.remove(os.path.join(dest_path, "test_fetch.txt"))
    os.remove(os.path.join(dest_path, "test_multifetch.txt"))
    os.remove(os.path.join(dest_path, "petrel_fetch.txt"))
    os.remove(os.path.join(dest_path, "petrel_multifetch.txt"))

    # Too many files
    assert f.http_download(list(range(10001)))["success"] is False
    out, err = capsys.readouterr()
    assert "Too many results supplied. Use globus_download()" in out

    # "Missing" files
    f.http_download(example_result_missing)
    out, err = capsys.readouterr()
    assert not os.path.exists("./should_not_exist.txt")
    assert ("Error 404 when attempting to access "
            "'https://data.materialsdatafacility.org/test/should_not_exist.txt'") in out

    # No datasets
    f.http_download(example_dataset)
    out, err = capsys.readouterr()
    assert not os.path.exists(os.path.join(dest_path, "petrel_fetch.txt"))
    assert ("Skipping datset entry for 'foobar_v1': Cannot download dataset over HTTPS. "
            "Use globus_download() for datasets.") in out

    # Bad resource_type
    f.http_download(example_bad_resource)
    out, err = capsys.readouterr()
    assert "Error: Found unknown resource_type 'foobar'. Skipping entry." in out


@pytest.mark.xfail(reason="Test should have a local endpoint.")
def test_forge_globus_download():
    f = Forge(index="mdf")
    # Simple case
    f.globus_download(example_result1)
    assert os.path.exists("./test_fetch.txt")
    os.remove("./test_fetch.txt")

    # With dest and preserve_dir
    dest_path = os.path.expanduser("~/mdf")
    f.globus_download(example_result1, dest=dest_path, preserve_dir=True)
    assert os.path.exists(os.path.join(dest_path, "test", "test_fetch.txt"))
    os.remove(os.path.join(dest_path, "test", "test_fetch.txt"))
    os.rmdir(os.path.join(dest_path, "test"))

    # With multiple files
    f.globus_download(example_result2, dest=dest_path)
    assert os.path.exists(os.path.join(dest_path, "test_fetch.txt"))
    assert os.path.exists(os.path.join(dest_path, "test_multifetch.txt"))
    os.remove(os.path.join(dest_path, "test_fetch.txt"))
    os.remove(os.path.join(dest_path, "test_multifetch.txt"))

    f.globus_download(example_result3, dest=dest_path)
    assert os.path.exists(os.path.join(dest_path, "test_fetch.txt"))
    assert os.path.exists(os.path.join(dest_path, "test_multifetch.txt"))
    os.remove(os.path.join(dest_path, "test_fetch.txt"))
    os.remove(os.path.join(dest_path, "test_multifetch.txt"))


def test_forge_http_stream(capsys):
    f = Forge(index="mdf")
    # Simple case
    res1 = f.http_stream(example_result1)
    assert isinstance(res1, types.GeneratorType)
    assert next(res1) == "This is a test document for Forge testing. Please do not remove.\n"

    # With multiple files
    res2 = f.http_stream((example_result2, {"info": {}}))
    assert isinstance(res2, types.GeneratorType)
    assert next(res2) == "This is a test document for Forge testing. Please do not remove.\n"
    assert next(res2) == "This is a second test document for Forge testing. Please do not remove.\n"
    assert next(res2) == "This is a test document for Forge testing. Please do not remove.\n"
    assert next(res2) == "This is a second test document for Forge testing. Please do not remove.\n"

    res3 = f.http_stream((example_result3, {"info": {}}))
    assert isinstance(res3, types.GeneratorType)
    assert next(res3) == "This is a test document for Forge testing. Please do not remove.\n"
    assert next(res3) == "This is a second test document for Forge testing. Please do not remove.\n"
    assert next(res3) == "This is a test document for Forge testing. Please do not remove.\n"
    assert next(res3) == "This is a second test document for Forge testing. Please do not remove.\n"

    # Too many results
    res4 = f.http_stream(list(range(10001)))
    assert next(res4)["success"] is False
    out, err = capsys.readouterr()
    assert "Too many results supplied. Use globus_download()" in out
    with pytest.raises(StopIteration):
        next(res4)

    # "Missing" files
    assert next(f.http_stream(example_result_missing)) is None
    out, err = capsys.readouterr()
    assert not os.path.exists("./should_not_exist.txt")
    assert ("Error 404 when attempting to access "
            "'https://data.materialsdatafacility.org/test/should_not_exist.txt'") in out
'''

def test_forge_chaining():
    f = Forge(index="mdf")
    f.match_field("source_name", "cip")
    f.match_field("material.elements", "Al")
    res1 = f.search()
    res2 = f.match_field("source_name", "cip").match_field("material.elements", "Al").search()
    assert all([r in res2 for r in res1]) and all([r in res1 for r in res2])


def test_forge_anonymous(capsys):
    f = Forge(anonymous=True)
    # Test search
    assert len(f.search("mdf.source_name:ab_initio_solute_database",
                        advanced=True, limit=300)) == 300

    # Test aggregation
    assert len(f.aggregate("mdf.source_name:nist_xps_db")) > 10000

    # Error on auth-only functions
    # http_download
    assert f.http_download({})["success"] is False
    out, err = capsys.readouterr()
    assert "Error: Anonymous HTTP download not yet supported." in out
    # globus_download
    assert f.globus_download({})["success"] is False
    out, err = capsys.readouterr()
    assert "Error: Anonymous Globus Transfer not supported." in out
    # http_stream
    res = f.http_stream({})
    assert next(res)["success"] is False
    out, err = capsys.readouterr()
    assert "Error: Anonymous HTTP download not yet supported." in out
    with pytest.raises(StopIteration):
        next(res)


def test_get_dataset_version():
    # Get the version number of the OQMD
    f = Forge()
    hits = f.search('mdf.source_name:oqmd AND mdf.resource_type:dataset',
                    advanced=True, limit=1)
    assert hits[0]['mdf']['version'] == f.get_dataset_version('oqmd')

    # Test invalid source_name
    with pytest.raises(ValueError):
        f.get_dataset_version('notreal')


def test_describe_field(capsys):
    f = Forge()
    # Basic usage (raw=True for ease of testing)
    res = f.describe_field("dataset", raw=True)
    assert res["success"]
    assert "dc" in res["schema"]["properties"].keys()
    assert res["schema"]["properties"]["mdf"]["properties"]["source_id"]
    # Specific field
    res = f.describe_field("dataset", field="dc", raw=True)
    assert "mdf" not in res["schema"]["properties"].keys()
    assert "titles" in res["schema"]["properties"].keys()
    # Special case
    res = f.describe_field("list", raw=True)
    assert isinstance(res["schema"], list)
    assert "mdf" in res["schema"]
    # Printing to stdout
    f.describe_field("record")
    out, err = capsys.readouterr()
    assert "- custom" in out
    # Specific field
    f.describe_field("record", field="mdf")
    out, err = capsys.readouterr()
    assert "- custom" not in out
    assert "- source_id" in out

    # Errors
    # Invalid resource_type
    res = f.describe_field("notexists", raw=True)
    assert res["success"] is False
    assert res["schema"] is None
    assert res["error"].startswith("Error 404")
    # stdout
    f.describe_field("notexists")
    out, err = capsys.readouterr()
    assert "Error 404" in out
    # Invalid field
    res = f.describe_field("dataset", field="foo.bar", raw=True)
    assert res["success"] is False
    assert res["schema"] is None
    assert res["error"].startswith("Error: Field 'foo' (from 'foo.bar')")
    # stdout
    f.describe_field("dataset", field="foo.bar")
    out, err = capsys.readouterr()
    assert "Error: Field 'foo' (from 'foo.bar')" in out


def test_describe_organization(capsys):
    f = Forge()
    # Basic usage (with raw=True)
    res = f.describe_organization("Argonne National Laboratory", raw=True)
    assert res["success"]
    assert isinstance(res["organization"], dict)
    assert res["organization"]["canonical_name"] == "Argonne National Laboratory"
    assert "ANL" in res["organization"]["aliases"]
    # List
    res = f.describe_organization("list", raw=True)
    assert isinstance(res["organization"], list)
    assert "Center for Hierarchical Materials Design" in res["organization"]
    # All
    res = f.describe_organization("all", raw=True)
    assert isinstance(res["organization"], list)
    assert isinstance(res["organization"][0], dict)
    # Print to stdout
    f.describe_organization("CHiMaD")
    out, err = capsys.readouterr()
    assert "canonical_name: Center for Hierarchical Materials Design" in out
    assert "CHiMaD" in out
    assert "public" in out
    # List
    f.describe_organization("list")
    out, err = capsys.readouterr()
    assert "Center for Hierarchical Materials Design" in out
    assert "CHiMaD" not in out
    assert "Argonne National Laboratory" in out
    assert "ANL" not in out
    # Summary flag
    f.describe_organization("chimad", summary=True)
    out, err = capsys.readouterr()
    assert "canonical_name: Center for Hierarchical Materials Design" not in out
    assert "Center for Hierarchical Materials Design" in out
    assert "CHiMaD" in out
    assert "public" not in out

    # Errors
    # Invalid org
    res = f.describe_organization("foobar", raw=True)
    assert res["success"] is False
    assert "Error 404" in res["error"]
    assert res["status_code"] == 404
    # stdout
    res = f.describe_organization("foobar")
    out, err = capsys.readouterr()
    assert "Error 404" in out
