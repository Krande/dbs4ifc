from rdflib import Graph, Namespace


def main():
    # Define the IFC namespace
    IFC_NS = Namespace("https://standards.buildingsmart.org/IFC/DEV/IFC4_1/OWL/")

    # Define the namespaces for RDF and RDFS
    RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")

    # Create an in-memory RDF graph
    g = Graph()
    g.parse("https://standards.buildingsmart.org/IFC/DEV/IFC4_1/OWL/")
    print(len(g))
    v = g.serialize(format="xml")
    print(v)


if __name__ == '__main__':
    main()
