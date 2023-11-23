# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RsfoMjRAxYt2kEIRa3sJFg3ugbbg_qQJ

**Task 07: Querying RDF(s)**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

# TO DO
from rdflib.plugins.sparql import prepareQuery

# Using RDFLib
print("Using RDFLib:")
ns = Namespace("http://somewhere#")

# recursive function
def find_subclasses(graph, class_uri, namespace, subclasses=None):
    if subclasses is None:
        subclasses = set()

    # Find direct subclasses
    for subclass in graph.objects(None, RDFS.subClassOf):
        if subclass not in subclasses:
            subclasses.add(subclass)
            find_subclasses(graph, subclass, namespace, subclasses)

    return subclasses

all_subclasses = find_subclasses(g, ns.LivingThing, ns)

for subclass in all_subclasses:
    print(subclass)



# Using SPARQL
print("Using SPARQL:")
q1 = prepareQuery('''
    SELECT ?subclass
    WHERE {
    ?subclass rdfs:subClassOf* ns:LivingThing .
    }
    ''',
    initNs={"rdfs": RDFS, "ns": ns}
)
for r in g.query(q1):
    print(r.subClass)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# TO DO

# Using RDFLib
def find_individuals(graph, class_uri, namespace, individuals=None):
    if individuals is None:
        individuals = set()
    for individual in graph.subjects(RDF.type, class_uri):
        individuals.add(individual)
    for subclass in graph.subjects(RDFS.subClassOf, class_uri):
        find_individuals(graph, subclass, namespace, individuals)
    return individuals

print("Using RDFLib:")
ns = Namespace("http://somewhere#")
all_individuals = find_individuals(g, ns.Person, ns)
for individual in all_individuals:
    print(individual)


# Using SPARQL
print("Using SPARQL:")
q2 = prepareQuery('''
    SELECT ?individual
    WHERE {
    ?individual rdf:type ?type .
    ?type rdfs:subClassOf* ns:Person .
    }
    ''',
    initNs={"rdf": RDF, "rdfs": RDFS, "ns": ns}
)

for r in g.query(q2):
    print(r.individual)

"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""

# TO DO
# Using RDFLib
print("Using RDFLib:")
ns = Namespace("http://somewhere#")
for s, p, o in g.triples((None, RDF.type, ns.Person)):
  for s, p, o in g.triples((s, None, None)):
    print(s, p, o)
for s, p, o in g.triples((None, RDF.type, ns.Animal)):
  for s, p, o in g.triples((s, None, None)):
    print(s, p, o)

# Using SPARQL
print("Using SPARQL:")
q3 = prepareQuery('''
    SELECT ?individual ?property ?value
    WHERE {
        ?individual rdf:type ?class .
        ?individual ?property ?value .
        FILTER (?class IN (ns:Person, ns:Animal))
        MINUS { ?subclass rdfs:subClassOf ns:Person . ?individual rdf:type ?subclass . }
    }
    ''',
    initNs={"rdf": RDF, "ns": ns}
)

for r in g.query(q3):
    print(r.individual, r.property, r.value)

"""**TASK 7.4:  List the name of the persons who know Rocky**"""


# TO DO
# Using RDFLib
for s, p, o in g.triples((None, FOAF.knows, ns.RockySmith)):
    for x, z, name in g.triples((s, VCARD.FN, None)):
        print(name)
        
# Using SPARQL
from rdflib.namespace import FOAF
q4 = prepareQuery('''
    SELECT ?name
    WHERE {
        ?individual foaf:knows ns:RockySmith .
        ?individual vcard:FN ?name .
    }
    ''',
    initNs={"ns": ns, "foaf": FOAF, "vcard": Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")}
)


# Visualize the results
for r in g.query(q4):
    print(r.name)

"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

# TO DO
# Using RDFLib
known_entities = defaultdict(set)
for s, p, o in g.triples((None, FOAF.knows, None)):
    known_entities[s].add(o)
for individual, entities in known_entities.items():
    if len(entities) >= 2:
        print(individual)

# Using SPARQL
q5 = prepareQuery('''
    SELECT ?individual
    WHERE {
        ?individual foaf:knows ?entity .
    }
    GROUP BY ?individual
    HAVING (COUNT(DISTINCT ?entity) >= 2)

    ''',
    initNs={"foaf": FOAF}
)


# Visualize the results
for r in g.query(q5):
    print(r.individual)
