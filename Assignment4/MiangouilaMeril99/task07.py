# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EuFHoryrW1xNUfg8tGh1kk_8R_4TAJOD

**Task 07: Querying RDF(s)**
"""

github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS
from pprint import pprint
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

# Import necessary libraries
ns = Namespace("http://somewhere#")
q1 = '''
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ns: <http://somewhere#>
    SELECT ?subclass
    WHERE {
        ?subclass rdfs:subClassOf+ ns:LivingThing .
    }
'''

# Execute the query and print results
for r in g.query(q1):
  print(r.subclass)

living_thing = ns.LivingThing

def find_subclasses(subclass, graph, subclasses):
    for s, p, o in graph.triples((None, RDFS.subClassOf, subclass)):
        if s not in subclasses:
            subclasses.add(s)
            find_subclasses(s, graph, subclasses)

subclasses_of_living_thing = set()

find_subclasses(living_thing, g, subclasses_of_living_thing)

# Print the subclasses
for subclass in subclasses_of_living_thing:
    print(subclass)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

q2 = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ns: <http://somewhere#>
    SELECT ?individual
    WHERE {
        ?individual rdf:type ?type .
        ?type rdfs:subClassOf* ns:Person .
    }
"""
for r in g.query(q2):
    print(r)


# Function to recursively find all subclasses of "Person"
def task07_2_find_person_subclasses(class_uri, graph, subclasses):
    for s, p, o in graph.triples((None, RDFS.subClassOf, class_uri)):
        if s not in subclasses:
            subclasses.add(s)
            task07_2_find_person_subclasses(s, graph, subclasses)

person_subclasses = set([ns.Person])
task07_2_find_person_subclasses(ns.Person, g, person_subclasses)

individuals_of_person = set()

for person_class in person_subclasses:
    for s, p, o in g.triples((None, RDF.type, person_class)):
        individuals_of_person.add(s)

for individual in individuals_of_person:
    print(individual)


"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""

q3 = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX ns: <http://somewhere#>
    SELECT DISTINCT ?individual ?property ?value
    WHERE {
        { ?individual rdf:type ns:Person . }
        UNION
        { ?individual rdf:type ns:Animal . }
        ?individual ?property ?value .
    }
"""
for r in g.query(q3):
    pprint(r)


def task07_3(graph, ns):
    for s, p, o in graph:
        if p == RDF.type and (o == ns.Person or o == ns.Animal):
            pprint(f"Individual: {s}")
            for prop, value in graph.predicate_objects(s):
                pprint(f"  Property: {prop}, Value: {value}")
            print()


task07_3(g, ns)



"""**TASK 7.4:  List the name of the persons who know Rocky**"""


ns = Namespace("http://somewhere#")
q4 = """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX vcard: <http://www.w3.org/2001/vcard-rdf/3.0#>
    PREFIX ns: <http://somewhere#>
    SELECT ?name
    WHERE {
        ?person foaf:knows ns:Rocky ;
                vcard:FN ?name .
    }
"""
for r in g.query(q4):
 pprint(r)

from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, FOAF

def task07_4(graph, ns):
    rocky_uri = ns.RockySmith
    vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
    for s, p, o in graph:
        if p == FOAF.knows and o == rocky_uri:
            for _, prop, name in graph.triples((s, vcard.FN, None)):
                print(f"Person's Name: {name}")

task07_4(g, Namespace("http://somewhere#"))


"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

ns = Namespace("http://somewhere#")
q5 = """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    SELECT ?entity
    WHERE {
        ?entity foaf:knows ?known1 .
        ?entity foaf:knows ?known2 .
        FILTER (?known1 != ?known2)
    }
    GROUP BY ?entity
    HAVING (COUNT(DISTINCT ?known1) >= 2)
"""

for r in g.query(q5):
    print(r)

from rdflib.namespace import FOAF
from collections import defaultdict

def task07_5(graph):
    known_entities = defaultdict(set)

    for s, p, o in graph.triples((None, FOAF.knows, None)):
        known_entities[s].add(o)
    for entity, known in known_entities.items():
        if len(known) >= 2:
            print(entity)

task07_5(g)

