from ontology_term_usage.term_usage import OntologyClient

from ontology_term_usage import __version__


def test_version():
    assert __version__ == '0.1.0'

def test_ontobee():
    client = OntologyClient()
    #client.term_usage_ontobee('GO:0007588')

def test_ubergraph():
    client = OntologyClient()
    client.term_usage_ubergraph('GO:0007588')