import pandas as pd
from SPARQLWrapper import SPARQLWrapper
from rdflib import Graph, URIRef, RDFS, Namespace, ConjunctiveGraph

# this section is to parse the data from the companies house URIs and create the local rdf datastore:
def makeCompanyGraph(parseRange, URIList, fileName = 'CompaniesData.ttl'):
    ''' 
    Parses parseRange (int) number of companies taking IDs in order from a pandas IDList and creates a local RDF store of name fileName(string)
    '''
    g = ConjunctiveGraph()
    for i in range(parseRange):
        uri = URIList['URI'][i+6000]
        g.parse(uri)
        print('parsing ['+str(i+1)+'/'+str(parseRange)+']: ' + uri)
    g = g.serialize(destination=fileName, format='ttl', encoding='utf-8')
    return g

#helper function from the lab to plot dot diagrams
def triplesToDot (triples, filename, nsdict):
  out = open(filename, 'w')
  out.write('graph "SimpleGraph" {\n')
  out.write('overlap = "scale";\n')

  for t in triples:
    s = '"%s" -- "%s " [label="%s"] ;\n' % (t[0].encode('utf-8'), t[2].encode('utf-8'), t[1].encode('utf-8'))

    for item in nsdict:
      s = s.replace(item, nsdict[item])

    out.write(s)

  out.write('}')

# # if the ttl list is not found, could use this step to generate it.
# l = pd.read_pickle('CompanyURI.pkl')
# g = makeCompanyGraph(parseRange=3, URIList=l, fileName='test.ttl')

#In this section, we will populate our ontology with the company details and location details as well:
file = 'test.ttl'
g = Graph()
g.parse(file,format='turtle')

# #testing some queries
# query = ''' 
# PREFIX cs0: <http://www.companieshouse.gov.uk/terms/>
# PREFIX wd: <http://www.wikidata.org/entity/>
# PREFIX wdt: <http://www.wikidata.org/prop/direct/>
# PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>        
# PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
# prefix owl: <http://www.w3.org/2002/07/owl#>
# PREFIX wikibase: <http://wikiba.se/ontology#>
# PREFIX bd: <http://www.bigdata.com/rdf#>

# SELECT ?company ?name ?CompanyNumber ?townURI ?townName ?population ?SICCode WHERE {
#     ?company cs0:CompanyName ?name;
#         cs0:CompanyNumber ?CompanyNumber;
#         cs0:Address ?Address.
#     ?Address cs0:PostTown ?town.
#     SERVICE <https://query.wikidata.org/sparql> {
#     ?townURI wdt:P31 wd:Q515;
#         wdt:P17 wd:Q145;
#         rdfs:label ?townName.
#     FILTER(LANG(?townName) = "en").
#     OPTIONAL {?townURI wdt:P1082 ?population.}
#     }
#     FILTER(UCASE(str(?townName)) = str(?town)).
# }
# '''


# results = g.query(query)
# print(type(results))
# for r in results:
#     print(r)


# building rdf graph with populated OWL
build = ''' 
PREFIX cs0: <http://www.companieshouse.gov.uk/terms/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>        
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
prefix owl: <http://www.w3.org/2002/07/owl#>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX bd: <http://www.bigdata.com/rdf#>
PREFIX uko: <http://www.semanticweb.org/SamiSaade/ontologies/UKCompanies#>

CONSTRUCT {
    ?company rdf:type uko:Company;
        uko:Name ?name;
        uko:registered_in ?townURI;
        uko:Company_ID ?companyNumber.
    ?townURI rdf:type uko:town;
        uko:Name ?townName;
        uko:has_population ?population;
        uko:part_of uko:UK.
    } WHERE {
    ?company cs0:CompanyName ?name;
        cs0:CompanyNumber ?CompanyNumber;
        cs0:Address ?Address.
    ?Address cs0:PostTown ?town.
    SERVICE <https://query.wikidata.org/sparql> {
    ?townURI wdt:P31 wd:Q515;
        wdt:P17 wd:Q145;
        rdfs:label ?townName.
    FILTER(LANG(?townName) = "en").
    OPTIONAL {?townURI wdt:P1082 ?population.}
    }
    FILTER(UCASE(str(?townName)) = str(?town)).
}
'''
print('querying...')
o = g.query(build)
o = o.serialize(destination="query_results.owl", format="xml")

print('Finished Query!')
print(o)

o.parse("CompanyUK.owl")
o.serialize("Companies_Full.owl", format="xml")

print('All done :)')





