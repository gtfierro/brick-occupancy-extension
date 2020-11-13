import logging
from rdflib import Literal, XSD
from compile import define_classes, define_values, G
from ns import BRICK, RDF, OWL, RDFS, SKOS, A, EXT

# EXT is the namespace of our extension
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
        "properties": {
            "Permenance": {
                "exclusive": True,
                "values": {
                    "Temporary": {
                        SKOS.definition: Literal("A temporary building occupant; e.g. a visitor"),
                    },
                    "Regular": {
                        SKOS.definition: Literal("A regular building occupant; e.g. an employee"),
                    }
                }
            },
            "Gender": {
                "exclusive": False,
                "values": [
                    "Male", "Female", "Non-binary", "Decline to state"
                ],
            },
            # TODO: make AgeRange more general (attach to a group of occupants too), and
            # be able to refer to it so we don't repeat the definition
            "AgeRange": {
                SKOS.definition: Literal("Age range of individuals or a certain group of occupants"),
                "exclusive": True,
                "values": {
                    "Children": {
                        SKOS.definition: Literal("Occupants are less than 11 years old (inclusive)"),
                    },
                    "Teens": {
                        SKOS.definition: Literal("Occupants are between 12 to 17 years old (inclusive)"),
                    },
                    "Adults": {
                        SKOS.definition: Literal("Occupants are between 18 to 64 years old (inclusive)"),
                    },
                    "Elderly": {
                        SKOS.definition: Literal("Occupants are more than 65 years old (inclusive)"),
                    }
                }
            },
            "Age": {
                SKOS.definition: Literal("Age of an individual"),
                "datatype": XSD.Integer,
            },
            # TODO: Race could be better modeled as Ancestry? Still need an enumeration definition (http://sitn.hms.harvard.edu/flash/2017/science-genetics-reshaping-race-debate-21st-century/)
            # TODO: thermal preference
            # TODO: energy use style

        },
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

# enumerations
enums = {
    "DeviceProperty": {
        SKOS.definition: Literal("Properties of devices that relate to occupants and their interactions with devices"),
        "subclasses": {
            "DegreeOfControl": {
                SKOS.definition: Literal("How a device may be controlled by an occupant"),
            },
            "OccupantAccessibilityLevel": {
                SKOS.definition: Literal("How accessible a device is to be controlled by occupants"),
            },
            "ModeOfControl": {
                SKOS.definition: Literal("The policy under which the device is controlled"),
            },
        },
    },
}
define_classes(enums, BRICK.Class, ns=EXT)


enum_values = {
    "OnOffControl": {
        A: EXT.DegreeOfControl,
        SKOS.definition: Literal("Device has on/off binary control"),
    },
    "ContinuousControl": {
        A: EXT.DegreeOfControl,
        SKOS.definition: Literal("Device supports a continuous range of control inputs (e.g. 0-100%)"),
    },
    "StagedControl": {
        A: EXT.DegreeOfControl,
        SKOS.definition: Literal("Device has a fixed number (> 2) of inputs"),
    },
    "NoControl": {
        A: EXT.DegreeOfControl,
        SKOS.definition: Literal("Device is fixed or has no control input capabilities"),
    },

    "NotAccessible": {
        A: EXT.OccupantAccessibilityLevel,
        SKOS.definition: Literal("Device is inaccessible to occupants"),
    },
    "Adjustable": {
        A: EXT.OccupantAccessibilityLevel,
        SKOS.definition: Literal("Device is accessible to occupants"),
    },
    "Shared": {
        A: EXT.OccupantAccessibilityLevel,
        SKOS.definition: Literal("Device is accessible by many occupants"),
    },

    "ManualMode": {
        A: EXT.ModeOfControl,
        SKOS.definition: Literal("Device is controlled manually"),
    },
    "AutomaticMode": {
        A: EXT.ModeOfControl,
        SKOS.definition: Literal("Device is controlled automatically, according to some schedule"),
    },
    "DynamicMode": {
        A: EXT.ModeOfControl,
        SKOS.definition: Literal("Device is controlled by a dynamic process, e.g. via a grid signal"),
    },
}
#TODO: instantiate
define_values(enum_values, ns=EXT)


logging.info("Defining properties")
logging.info(f"Extension ontology compilation finished! Generated {len(G)} triples")


# serialize to output
with open("occupancy.ttl", "wb") as fp:
    fp.write(G.serialize(format="turtle").rstrip())
    fp.write(b"\n")
