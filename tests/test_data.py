from datetime import datetime


datacite_data = {'identifier': {'identifier': '10.xx/xx', 'identifierType': 'DOI'},
                 'rightsList': [{'rights': 'CC-BY 4.0'}],
                 'creators': [{'creatorName': 'Brown, C',
                               'familyName': 'Brown',
                               'givenName': 'C'},
                              {'creatorName': 'Van Pelt, L',
                               'familyName': 'Van Pelt',
                               'givenName': 'L'}],
                 'subjects': [{'subject': 'blockheads'},
                              {'subject': 'foundry'},
                              {'subject': 'test_data'}],
                 'publicationYear': 2024,
                 'publisher': 'Materials Data Facility',
                 'dates': [{'date': '2024-08-03', 'dateType': 'Accepted'}],
                 'titles': [{'title': "You're a Good man, Charlie Brown"}],
                 'resourceType': {'resourceTypeGeneral': 'Dataset',
                                  'resourceType': 'Dataset'}}


valid_metadata = {"keys": [
                    {
                        "key": ["sepal length (cm)"],
                        "type": "input",
                        "units": "cm",
                        "description": "sepal length in Charlie Brown's zig-zag style"
                    },
                    {
                        "key": ["sepal width (cm)"],
                        "type": "input",
                        "units": "cm",
                        "description": "sepal width in Snoopy's flying ace mode"
                    },
                    {
                        "key": ["petal length (cm)"],
                        "type": "input",
                        "units": "cm",
                        "description": "petal length in Linus's security blanket units"
                    },
                    {
                        "key": ["petal width (cm)"],
                        "type": "input",
                        "units": "cm",
                        "description": "petal width in Lucy's psychiatric advice scale"
                    },
                    {
                        "key": ["y"],
                        "type": "output",
                        "units": "",
                        "description": "flower type",
                        "classes": [
                            {
                                "label": "0",
                                "name": "setosa"
                            },
                            {
                                "label": "1",
                                "name": "versicolor"
                            },
                            {
                                "label": "2",
                                "name": "virginica"
                            }
                        ]
                    }
                ],
                "splits": [
                    {"label": "train", "path": "train_snoopy.json", "type": "train"},
                    {"label": "test", "path": "test_woodstock.json", "type": "test"}
                ],
                "short_name": "peanuts_iris_{:.0f}".format(datetime.now().timestamp()),
                "data_type": "tabular",
                "task_type": ["unsupervised", "generative"],
                "domain": ["comics", "nostalgia"],
                "n_items": 1000
            }


invalid_metadata = {"oranges": [
                        {
                            "key": ["sepal length (cm)"],
                            "type": "input",
                            "units": "cm",
                            "description": 10
                        },
                        {
                            "key": ["sepal width (cm)"],
                            "type": "input",
                            "units": "cm",
                            "description": "sepal width in unit(cm)"
                        },
                        {
                            "key": ["petal length (cm)"],
                            "type": "input",
                            "units": "cm",
                            "description": "petal length in unit(cm)"
                        },
                        {
                            "key": ["petal width (cm)"],
                            "type": "input",
                            "units": "cm",
                            "description": "petal width in unit(cm)"
                        },
                        {
                            "key": ["y"],
                            "type": "output",
                            "units": "",
                            "description": "flower type",
                            "classes": [
                                {
                                    "label": "0",
                                    "name": "setosa"
                                },
                                {
                                    "label": "1",
                                    "name": "versicolor"
                                },
                                {
                                    "label": "2",
                                    "name": "virginica"
                                }
                            ]
                        }
                    ],
                    'splits': [
                        {'label': 'train', 'path': 'train.json', 'type': 'train'},
                        {'label': 'test', 'path': 'test.json', 'type': 'test'}
                    ],
                    "short_name": "example_AS_iris_test_{:.0f}".format(datetime.now().timestamp()),
                    "data_type": "tabular",
                    'task_type': ['unsupervised', 'generative'],
                    'domain': ['materials science', 'chemistry'],
                    'n_items': 1000
                }
