import csv
import logging
from collections import defaultdict
from rdflib import Graph, Literal, BNode, URIRef
from rdflib.collection import Collection
from ns import BRICK, RDF, OWL, RDFS, SKOS
from ns import bind_prefixes


logging.basicConfig(
    format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=logging.INFO,
)

G = Graph()
bind_prefixes(G)
A = RDF.type

tag_lookup = defaultdict(set)
intersection_classes = {}


def add_restriction(klass, definition):
    """
    Defines OWL.Restrictions linked to Brick classes
    through OWL.equivalentClass.

    This populates the property-object pairs (OWL.onProperty, 'property'),
    (OWL.hasValue, 'value'). The intersection of these properties is made to be
    equivalent to the given class.

    Args:
        klass: the URI of the Brick class to be modeled
        definition: a list of (property, value) pairs
    """
    if len(definition) == 0:
        return
    elements = []
    equivalent_class = BNode()
    list_name = BNode()
    for idnum, item in enumerate(definition):
        restriction = BNode()
        elements.append(restriction)
        G.add((restriction, A, OWL.Restriction))
        G.add((restriction, OWL.onProperty, item[0]))
        G.add((restriction, OWL.hasValue, item[1]))
    G.add((klass, OWL.equivalentClass, equivalent_class))
    G.add((equivalent_class, OWL.intersectionOf, list_name))
    Collection(G, list_name, elements)


def add_tags(klass, definition):
    """
    Adds the definition of tags to the given class. This method adds two
    group of triples. The first group models the class as a subclass
    of entities that have all of the given tags (the 'OWL.intersectionOf'
    the OWL.Restriction classes modeled as entities that have a given tag).

    The second group of triples uses the BRICK.hasAssociatedTag property
    to associate the tags with this class. While this is duplicate information,
    it is much easier to query for.

    Args:
        klass: the URI of the Brick class to be modeled
        definition: a list of BRICK.Tag instances (e.g. TAG.Air)
    """
    if len(definition) == 0:
        return
    all_restrictions = []
    equivalent_class = BNode()
    list_name = BNode()

    for tag in definition:
        G.add((klass, BRICK.hasAssociatedTag, tag))

    for idnum, item in enumerate(definition):
        restriction = BNode(f"has_{item.split('#')[-1]}")
        all_restrictions.append(restriction)
        G.add((restriction, A, OWL.Restriction))
        G.add((restriction, OWL.onProperty, BRICK.hasTag))
        G.add((restriction, OWL.hasValue, item))
        G.add((item, A, BRICK.Tag))  # make sure the tag is declared as such
        G.add(
            (item, RDFS.label, Literal(item.split("#")[-1]))
        )  # make sure the tag is declared as such

    # tag index
    tagset = tuple(sorted([item.split("#")[-1] for item in definition]))
    tag_lookup[tagset].add(klass)

    # if we've already mapped this class, don't map it again
    if klass in intersection_classes:
        return
    if len(all_restrictions) == 1:
        G.add((klass, RDFS.subClassOf, all_restrictions[0]))
    if len(all_restrictions) > 1:
        G.add((klass, RDFS.subClassOf, equivalent_class))
        G.add((equivalent_class, OWL.intersectionOf, list_name))
        Collection(G, list_name, all_restrictions)
    intersection_classes[klass] = tuple(sorted(definition))


def define_classes(definitions, parent, pun_classes=False, ns=BRICK):
    """
    Generates triples for the hierarchy given by 'definitions', rooted
    at the class given by 'parent'
    - class hierarchy ('subclasses')
    - tag mappings
    - substance + quantity modeling

    If pun_classes is True, then create punned instances of the classes
    """
    for classname, defn in definitions.items():
        classname = ns[classname]
        # class is a owl:Class
        G.add((classname, A, OWL.Class))
        # subclass of parent
        G.add((classname, RDFS.subClassOf, parent))
        # add label
        class_label = classname.split("#")[-1].replace("_", " ")
        G.add((classname, RDFS.label, Literal(class_label)))
        if pun_classes:
            G.add((classname, A, classname))

        # define mapping to tags if it exists
        # "tags" property is a list of URIs naming Tags
        taglist = defn.get("tags", [])
        assert isinstance(taglist, list)
        if len(taglist) == 0:
            logging.warning(f"Property 'tags' not defined for {classname}")
        add_tags(classname, taglist)

        # define mapping to substances + quantities if it exists
        # "substances" property is a list of (predicate, object) pairs
        substancedef = defn.get("substances", [])
        assert isinstance(substancedef, list)
        add_restriction(classname, substancedef)

        # define class structure
        # this is a nested dictionary
        subclassdef = defn.get("subclasses", {})
        assert isinstance(subclassdef, dict)
        define_classes(subclassdef, classname, pun_classes=pun_classes, ns=ns)

        # handle 'parents' subclasses (links outside of tree-based hierarchy)
        parents = defn.get("parents", [])
        assert isinstance(parents, list)
        for _parent in parents:
            G.add((classname, RDFS.subClassOf, _parent))

        # all other key-value pairs in the definition are
        # property-object pairs
        expected_properties = ["parents", "tags", "substances", "subclasses"]
        other_properties = [
            prop for prop in defn.keys() if prop not in expected_properties
        ]
        for propname in other_properties:
            propval = defn[propname]
            if isinstance(propval, list):
                for pv in propval:
                    G.add((classname, propname, pv))
            else:
                G.add((classname, propname, propval))


def define_properties(definitions, superprop=None, ns=BRICK):
    """
    Define BRICK properties
    """
    if len(definitions) == 0:
        return

    for prop, propdefn in definitions.items():
        G.add((ns[prop], A, OWL.ObjectProperty))
        if superprop is not None:
            G.add((ns[prop], RDFS.subPropertyOf, superprop))

        # define property types
        prop_types = propdefn.get(A, [])
        assert isinstance(prop_types, list)
        for prop_type in prop_types:
            G.add((ns[prop], A, prop_type))

        # define any subproperties
        subproperties_def = propdefn.get("subproperties", {})
        assert isinstance(subproperties_def, dict)
        define_properties(subproperties_def, ns[prop], ns=ns)

        # define other properties of the Brick property
        for propname, propval in propdefn.items():
            # all other key-value pairs in the definition are
            # property-object pairs
            expected_properties = ["subproperties", A]
            other_properties = [
                prop for prop in propdefn.keys() if prop not in expected_properties
            ]

            for propname in other_properties:
                propval = propdefn[propname]
                G.add((ns[prop], propname, propval))


def define_values(definitions, ns=BRICK):
    for ent, entdefn in definitions.items():
        if A not in entdefn:
            raise Exception("Need to provide a class to instantiate!")
        for propname in entdefn.keys():
            vals = entdefn[propname]
            if not isinstance(vals, list):
                vals = [vals]
            for v in vals:
                G.add((ns[ent], propname, v))


def add_definitions():
    """
    Adds definitions for Brick subclasses through SKOS.definitions.

    This parses the definitions from ./bricksrc/definitions.csv and
    adds it to the graph. If available, adds the source information of
    through RDFS.seeAlso.
    """
    with open("./bricksrc/definitions.csv") as dictionary_file:
        dictionary = csv.reader(dictionary_file)

        # skip the header
        next(dictionary)

        # add definitions, citations to the graph
        for definition in dictionary:
            term = URIRef(definition[0])
            if len(definition[1]):
                G.add((term, SKOS.definition, Literal(definition[1], lang="en")))
            if len(definition[2]):
                G.add((term, RDFS.seeAlso, URIRef(definition[2])))

    qstr = """
    select ?param where {
      ?param rdfs:subClassOf* brick:Limit.
    }
    """
    limit_def_template = "A parameter that places {direction} bound on the range of permitted values of a {setpoint}."
    params = [row["param"] for row in G.query(qstr)]
    for param in params:
        words = param.split("#")[-1].split("_")
        prefix = words[0]

        # define "direction" component of Limit definition
        if prefix == "Min":
            direction = "a lower"
        elif prefix == "Max":
            direction = "an upper"
        else:
            prefix = None
            direction = "a lower or upper"

        # define the "setpoint" component of a Limit definition
        if param.split("#")[-1] in ["Max_Limit", "Min_Limit", "Limit"]:
            setpoint = "Setpoint"
        else:
            if prefix:
                setpoint = "_".join(words[1:-1])
            else:
                setpoint = "_".join(words[:-1])

        if setpoint.split("_")[-1] != "Setpoint":
            # While Limits are a boundary of a Setpoint, the associated
            # Setpoint names are not explicit in class's names. Thus needs
            # to be explicily added for the definition text.
            setpoint = setpoint + "_Setpoint"
            logging.info(f"Inferred setpoint: {setpoint}")
        limit_def = limit_def_template.format(direction=direction, setpoint=setpoint)
        G.add((param, SKOS.definition, Literal(limit_def, lang="en")))
        class_exists = G.query(
            f"""select ?class where {{
            BIND(brick:{setpoint} as ?class)
            ?class rdfs:subClassOf* brick:Class.
        }}
        """
        ).bindings
        if not class_exists:
            logging.warning(f"WARNING: {setpoint} does not exist in Brick for {param}.")
