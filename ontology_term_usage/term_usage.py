import logging
from typing import List, Dict

from SPARQLWrapper import SPARQLWrapper, JSON
from pydantic import BaseModel


TERM = str
URISTR = str
SERVICE = str
CATEGORY = str

class ServiceMetadata(BaseModel):
    endpoint: str
    query_template: str
    category: CATEGORY = None
    description: str = None

class ServiceMetadataCollection(BaseModel):
    services: Dict[SERVICE, ServiceMetadata]

class TermUsage(BaseModel):
    """
    Info on how a term is used

    Most of the the time a curator needs to know the id/uri and label of the term,
    but it is also useful to give more context

    Note the thing using the term need not be an ontology term - e.g. it could be a uniprot protein
    """
    uri: URISTR
    label: str = None
    category: CATEGORY = None
    predicate: URISTR = None
    graph: URISTR = None
    notes: str = None
    axiom_type: str = None
    endpoint: str = None

class ResultSet(BaseModel):
    term: URISTR = None
    limit: int = None
    usages: Dict[SERVICE, List[TermUsage]] = {}

ontobee_usage_query_template = """
SELECT ?uri ?label ?predicate WHERE {{
  GRAPH ?graph {{
    ?uri <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?restr .
    ?restr <http://www.w3.org/2002/07/owl#onProperty> ?predicate .
    ?restr <http://www.w3.org/2002/07/owl#someValuesFrom> <{term_uri}> 
  }}
  ?uri rdfs:label ?label 
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

uniprot_usage_query_template = """
SELECT ?uri ?label WHERE {{
  ?uri <http://purl.uniprot.org/core/classifiedWith> <{term_uri}> ;
     rdfs:label ?label
}}
"""

gocam_usage_query_template = """
SELECT ?uri ?graph WHERE {{
  GRAPH ?graph {{
    ?uri rdf:type <{term_uri}> 
  }}
}}
"""

config = {
    'ontobee':
        {
            'endpoint': 'http://sparql.hegroup.org/sparql',
            'query_template': ontobee_usage_query_template,
            'category': 'OntologyTerm',
            'description': 'Ontobee includes all of OBO. We query for existential restrictions'
        },
    'ubergraph':
        {
            'endpoint': 'https://stars-app.renci.org/ubergraph/sparql',
            'query_template': ubergraph_usage_query_template,
            'category': 'OntologyTerm',
            'description': 'Ubergraph includes a subset of OBO, but may include axioms not in Ontobee'
        },
    'uniprot':
        {
            'endpoint': 'https://sparql.uniprot.org/sparql',
            'query_template': uniprot_usage_query_template,
            'category': 'Protein',
            'description': 'Uniprot includes annotations for GO terms'
        },
    'gocam':
        {
            'endpoint': 'http://rdf.geneontology.org/sparql',
            'query_template': gocam_usage_query_template,
            'category': 'Model',
            'description': 'GO-CAM includes models with instantiated GO terms'
        },
}


class OntologyClient(BaseModel):
    """
    Wrapper for multiple ontology endpoints
    """

    limit: int = 30

    def get_services(self) -> ServiceMetadataCollection:
        return ServiceMetadataCollection(services=config)

    def term_to_uri(self, term: TERM) -> URISTR:
        if ':/' in term:
            return term
        [prefix, local_id] = term.split(':')
        return f'http://purl.obolibrary.org/obo/{prefix}_{local_id}'

    def _term_usage_query(self, term: TERM, service: str) -> List[TermUsage]:
        info = ServiceMetadata(**config[service])
        limit = self.limit
        term_uri = self.term_to_uri(term)
        sparql = SPARQLWrapper(info.endpoint)
        q = info.query_template.format(term_uri=term_uri)
        q = f'{q}\nLIMIT {limit}'
        logging.info(q)
        sparql.setQuery(q)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        usages = []
        for result in results["results"]["bindings"]:
            d = {k: v['value'] for k, v in result.items()}
            u = TermUsage(**d)
            u.endpoint = info.endpoint
            u.category = info.category
            logging.debug(f'U={u}')
            usages.append(u)
        return usages

    def term_usage(self, term: TERM, services: List[SERVICE] = None) -> ResultSet:
        """
        iterate through all services querying for term usage

        :param term:
        :param services: if None, queries all
        :return:
        """
        rs = ResultSet(term=term, limit=self.limit)
        if services == None:
            services = config.keys()
        for service in services:
            rs.usages[service] = self._term_usage_query(term, service)
        return rs

    def term_usage_ontobee(self, term: TERM) -> List[TermUsage]:
        """
        Queries ontobee for usage

        LIMITATIONS: assumes relaxation pattern, as it looks for X sub R some TERM

        :param term:
        :return:
        """
        return self._term_usage_query(term, 'ontobee')

    def term_usage_ubergraph(self, term: TERM) -> List[TermUsage]:
        """
        Queries ubergraph for usage

        NOTE: currently includes false positives, need to filter out inference
        :param term:
        :return:
        """
        return self._term_usage_query(term, 'ubergraph')

    def term_usage_uniprot(self, term: TERM) -> List[TermUsage]:
        """
        Queries uniprot for usage

        :param term:
        :return:
        """
        return self._term_usage_query(term, 'uniprot')

