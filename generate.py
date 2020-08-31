import logging
from rdflib import Literal, Namespace
from compile import define_classes, bind_prefixes, G
from ns import BRICK, RDF, OWL, RDFS, SKOS
from ns import BRICK_VERSION

EXT = Namespace(f"https://brickschema.org/schema/{BRICK_VERSION}/Brick/extension/occupancy#")
G.bind("occ", EXT)

logging.basicConfig(
    format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=logging.INFO,
)

logging.info("Beginning extension compilation")

extension_classes = {
    "Occupant": {
        SKOS.definition: Literal("A building occupant"),
        "subclasses": {
            "Temporary_Occupant": {
                SKOS.definition: Literal("A temporary building occupant; e.g. a visitor"),
            },
            "Regular_Occupant": {
                SKOS.definition: Literal("A regular building occupant; e.g. an employee"),
            },
        }
    }
}

equipment_extensions = {
    "Envelope_Equipment": {
        SKOS.definition: Literal("Equipment used in the building envelope"),
        "subclasses": {
            "Window": {
                SKOS.definition: Literal("An opening in the wall or roof of a building or vehicle that is fitted with glass or other transparent material in a frame to admit light or air and allow people to see out."),
            },
        }
    }
}

define_classes(extension_classes, BRICK.Class, ns=EXT)
define_classes(equipment_extensions, BRICK.Equipment, ns=EXT)


logging.info("Defining properties")
logging.info(f"Extension ontology compilation finished! Generated {len(G)} triples")


# serialize to output
with open("occupancy.ttl", "wb") as fp:
    fp.write(G.serialize(format="turtle").rstrip())
    fp.write(b"\n")
