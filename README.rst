papernetwork
=============


.. image:: https://img.shields.io/pypi/v/papernetwork.svg
    :target: https://pypi.python.org/pypi/papernetwork
    :alt: Latest PyPI version

.. image:: https://travis-ci.com/EvdH0/papernetwork.svg?token=Fxxpxvyc3NhNSDqPmztx&branch=master
   :target: https://travis-ci.com/EvdH0/papernetwork
   :alt: Latest Travis CI build status

Collect and analyze scientific literature from Semantic Scholar

Examples
--------

Basic example of loading data from `Semantic Scholar <https://www.semanticscholar.org/>`_ via the `API <https://api.semanticscholar.org/>`_, be sure to read the `dataset license agreement <https://api.semanticscholar.org/corpus/legal/>`_::

    from papernetwork.core import PaperNetwork, Paper, PaperList

    # Define a list of DOI's you would like to download
    list_of_dois = ['10.1093/nar/gkw1328', '10.1128/CMR.00016-17', '10.1038/s41564-019-0626-z']

    # Pull the papers from semanticscholar.org via the API and parse them
    my_network = PaperNetwork(doi_list=list_of_dois)

    # Show the titles in the PaperNetwork object
    print(my_network)  # Rapid resistome mapping using nanopore sequencing, Whole-Genome Sequencing of Bacterial Pathogens: the Future of Nosocomial Outbreak Analysis., Rapid MinION profiling of preterm microbiota and antimicrobial-resistant pathogens

    # The papers are internally stored in a OrderedSet-like object, accessible via the collection 
    my_collection = my_network.collection

    # The papers themselves are individually stored in a Dict-like object
    my_paper = my_collection[0]  # Take the first paper in the list


    print(my_paper['title'])

    # They keys of the object are defined by the Semantic Scholar API, see https://api.semanticscholar.org/
    # To get an overview of the available keys
    for key, value in my_collection[0].items():
        print(key)

    # Currently the following keys are supplied by semanticscholar.org
    # arxivId
    # authors
    # citationVelocity
    # citations
    # corpusId
    # doi
    # fieldsOfStudy
    # influentialCitationCount
    # is_open_access
    # is_publisher_licensed
    # paperId
    # references
    # title
    # topics
    # url
    # venue
    # year 


A more elaborate example can be found in the `examples directory <examples/simple_example.py>`_ to get started.

More detailed usage can be found in the `test directory <tests/test_papernetwork.py>`_ as well.

Run using::
    python -m examples.simple_example

Installation
------------
Use pip to `install papernetwork from
PyPI <https://pypi.python.org/pypi/papernetwork>`_ (recommend doing this
inside a `virtual
environment <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_)::

    pip install papernetwork

Or from source::

    git clone --recursive https://github.com/evdh0/papernetwork.git
    cd papernetwork
    python setup.py install



Licence
-------
The MIT License (MIT)


Authors
-------

`papernetwork` was written by `Eric van der Helm <i@iric.nl>`_.
