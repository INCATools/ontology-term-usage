from typing import List

from ontology_term_usage import OntologyClient, TermUsage

from ontology_term_usage import __version__


def test_service_metadata():
    client = OntologyClient()
    s = client.get_services()
    print(s)
