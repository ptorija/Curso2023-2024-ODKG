# -*- coding: utf-8 -*-
"""Task08.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wYEOckbCVdWsz0is3CGk_oFWitS-xJje

**Task 08: Completing missing data**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g1.parse(github_storage+"/rdf/data01.rdf", format="xml")
g2.parse(github_storage+"/rdf/data02.rdf", format="xml")

"""Tarea: lista todos los elementos de la clase Person en el primer grafo (data01.rdf) y completa los campos (given name, family name y email) que puedan faltar con los datos del segundo grafo (data02.rdf). Puedes usar consultas SPARQL o iterar el grafo, o ambas cosas."""

for s,o,p in g1:
  print(s, o, p)

for s,o,p in g2:
  print(s, o, p)

from rdflib import Namespace, RDF

data = Namespace("http://data.org#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

# For each individual of type Person in g1, check and complete the fields
for person in g1.subjects(predicate=RDF.type, object=data.Person):
    # Check Given
    if not (person, vcard.Given, None) in g1:
        for name in g2.objects(subject=person, predicate=vcard.Given):
            g1.add((person, vcard.Given, name))

    # Check Family
    if not (person, vcard.Family, None) in g1:
        for family in g2.objects(subject=person, predicate=vcard.Family):
            g1.add((person, vcard.Family, family))

    # Check EMAIL
    if not (person, vcard.EMAIL, None) in g1:
        for email in g2.objects(subject=person, predicate=vcard.EMAIL):
            g1.add((person, vcard.EMAIL, email))

# Display the updated information
for s, p, o in g1.triples((None, RDF.type, data.Person)):
    print(f"Person: {s}")
    for name in g1.objects(subject=s, predicate=vcard.Given):
        print(f"Given Name: {name}")
    for family in g1.objects(subject=s, predicate=vcard.Family):
        print(f"Family Name: {family}")
    for email in g1.objects(subject=s, predicate=vcard.EMAIL):
        print(f"Email: {email}")
    print("-----------------------------------")