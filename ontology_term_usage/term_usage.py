import logging
from typing import List

from SPARQLWrapper import SPARQLWrapper, JSON
from pydantic import BaseModel


TERM = str
URISTR = str

class TermUsage(BaseModel):
    """
    Info on how a term is used

    Most of the the time a curator needs to know the id/uri and label of the term,
    but it is also useful to give more context
    """
    uri: URISTR
    label: str = None
    predicate: URISTR = None
    graph: URISTR = None
    notes: str = None
    axiom_type: str = None

ontobee_usage_query_template = """
SELECT ?uri ?label ?predicate WHERE {{
  ?uri <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?restr .
  ?uri rdfs:label ?label .
  ?restr <http://www.w3.org/2002/07/owl#onProperty> ?predicate .
  ?restr <http://www.w3.org/2002/07/owl#someValuesFrom> <{term_uri}>
}}
"""

ubergraph_usage_query_template = """
SELECT ?uri ?label ?predicate ?graph WHERE {{
  GRAPH ?graph {{
    ?uri ?predicate <{term_uri}> 
  }}
  ?uri rdfs:label ?label 
}}
"""

class OntologyClient:
    """
    Wrapper for multiple ontology endpoints
    """

    def term_to_uri(self, term: TERM) -> URISTR:
        if ':/' in term:
            return term
        [prefix, local_id] = term.split(':')
        return f'http://purl.obolibrary.org/obo/{prefix}_{local_id}'

    def _term_usage_query(self, term: TERM, endpoint: str, template: str) -> List[TermUsage]:
        term_uri = self.term_to_uri(term)
        sparql = SPARQLWrapper(endpoint)
        q = template.format(term_uri=term_uri)
        print(q)
        sparql.setQuery(q)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        usages = []
        for result in results["results"]["bindings"]:
            d = {k: v['value'] for k, v in result.items()}
            u = TermUsage(**d)
            print(f'U={u}')
            logging.info(f'U={u}')
            usages.append(u)
        return usages

    def term_usage_ontobee(self, term: TERM) -> List[TermUsage]:
        """
        Queries ontobee for usage

        LIMITATIONS: assumes relaxation pattern, as it looks for X sub R some TERM

        :param term:
        :return:
        """
        return self._term_usage_query(term, "http://sparql.hegroup.org/sparql", ontobee_usage_query_template)

    def term_usage_ubergraph(self, term: TERM) -> List[TermUsage]:
        """
        Queries ubergraph for usage

        NOTE: currently includes false positives, need to filter out inference
        :param term:
        :return:
        """
        return self._term_usage_query(term, "https://stars-app.renci.org/ubergraph/sparql", ubergraph_usage_query_template)

