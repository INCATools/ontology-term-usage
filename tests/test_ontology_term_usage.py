from typing import List

from ontology_term_usage import OntologyClient, TermUsage

from ontology_term_usage import __version__

TEST_TERM = 'GO:0006915' # apoptosis

def _check(results: List[TermUsage]):
    print(f'Num results = {len(results)}')
    assert len(results) > 0
    print(f'Example = {results[0]}')


def test_version():
    assert __version__ == '0.1.0'

def test_service_metadata():
    client = OntologyClient()
    s = client.get_services()
    print(s)

def test_ontobee():
    client = OntologyClient()
    _check(client.term_usage_ontobee(TEST_TERM))

def test_ubergraph():
    client = OntologyClient()
    _check(client.term_usage_ubergraph(TEST_TERM))

def test_uniprot():
    client = OntologyClient()
    _check(client.term_usage_uniprot(TEST_TERM))

def test_all():
    ontology_client = OntologyClient()
    rs = ontology_client.term_usage(TEST_TERM)
    print(f'RS={rs.term}')
    for s, usages in rs.usages.items():
        print(f'  {s}: {len(usages)}')

def test_limit():
    ontology_client = OntologyClient()
    rs = ontology_client.term_usage(TEST_TERM, limit=2)
    print(f'RS={rs.term}')
    for s, usages in rs.usages.items():
        print(f'  {s}: {len(usages)}')
        assert len(usages) == 2

def test_ro():
    ontology_client = OntologyClient()
    rs = ontology_client.term_usage('RO:0000057', limit=5)
    print(f'RO RS={rs.term}')
    for s, usages in rs.usages.items():
        print(f'  {s}: {len(usages)}')
        if usages != []:
            print(f'  {usages[0]}')
            assert len(usages) == 5
            assert any(usage for usage in usages if usage.query_type == 'RELATION')
