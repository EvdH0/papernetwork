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

    from papernetwork.papernetwork import PaperNetwork, Paper, PaperList
    list_of_dois = ['10.1093/nar/gkw1328']
    my_network = PaperNetwork(doi_list=list_of_dois)


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
