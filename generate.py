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
        SKOS.definition: Literal("Building occupant, which can be an indiviudal occupant or a group of occupants sharing some common attributes"),
        "properties": {
            "Permenance": {
                "exclusive": True,
                "values": {
                    "Individual": {
                        SKOS.definition: Literal("A description of one individual occupant"),
                    },
                    "Group": {
                        SKOS.definition: Literal("A description of a certain group of occupant"),
                    }
                }
            },
            "Gender": {
                "exclusive": False,
                "values": {
                    "Male": {
                        SKOS.definition: Literal("Occupants are male"),
                    },
                    "Female": {
                        SKOS.definition: Literal("Occupants are female"),
                    },
                    "Nonbinary": {
                        SKOS.definition: Literal("Occupants are non-binary"),
                    },
                    "Decline_to_state": {
                        SKOS.definition: Literal("Occupants declined to state"),
                    },
                }
            },
            "Race": {
                "exclusive": False,
                "values": {
                    "African_American": {
                        SKOS.definition: Literal("Occupants are African American"),
                    },
                    "Asian": {
                        SKOS.definition: Literal("Occupants are Asian"),
                    },
                    "American_Indian": {
                        SKOS.definition: Literal("Occupants are American Indian"),
                    },
                    "Native_Hawaiian": {
                        SKOS.definition: Literal("Occupants are Native Hawaiian"),
                    },
                    "White": {
                        SKOS.definition: Literal("Occupants are white people"),
                    },
                    "Mix": {
                        SKOS.definition: Literal("The group of occupants has a mix of races"),
                    }
                }
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
            # TODO: energy use style
            "Thermal_Preference": {
                "exclusive": False,
                "values": {
                    "Warmer": {
                        SKOS.definition: Literal("Occupants prefer warmer indoor environment"),
                    },
                    "Cooler": {
                        SKOS.definition: Literal("Occupants prefer cooler indoor environment"),
                    },
                    "Neutral": {
                        SKOS.definition: Literal("Occupants prefer neutral indoor environment"),
                    },
                    "No_Preference": {
                        SKOS.definition: Literal("Occupants do not have special thermal preference"),
                    }
                }
            },
            "Energy_Use_Style": {
                "exclusive": False,
                "values": {
                    "Austerity": {
                        SKOS.definition: Literal("Occupants have an austerity energy use behavior"),
                    },
                    "Wasteful": {
                        SKOS.definition: Literal("Occupants have a wasteful energy use behavior"),
                    },
                    "Norm": {
                        SKOS.definition: Literal("Occupants have an average energy use behavior"),
                    }
                }
            },

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
                SKOS.definition: Literal("An opening in the wall of a building to admit light or air and allows occupants to see out"),
            },
            "Door": {
                SKOS.definition: Literal("A hinged, sliding, or revolving barrier at the entrance of a building or a zone that allows occupants to go in and out"),
            }
        }
    },
    "Personal_Device": {
        SKOS.definition: Literal("Dedicated devices used to maintain thermal comfort for occupants"),
        "subclasses": {
            "Portable_Fan": {
                SKOS.definition: Literal("A cord-connected appliance that is easily moved by hand from place to place to provide flowing air"),
            },
            "Portable_Heater": {
                SKOS.definition: Literal("A cord-connected appliance that is easily moved by hand from place to place to provide heating"),
            },
            "Ceiling_Fan": {
                SKOS.definition: Literal("A mechanical fan mounted on the ceiling of a room or space, usually electrically powered, that uses hub-mounted rotating blades to circulate air"),
            },
            "Desktop_Light": {
                SKOS.definition: Literal("A lighting equipment on the desktop to provide illuminance"),
            }
        }
    }
}
point_extensions = {
    "Status": {
        SKOS.definition: Literal("Status of the equipment"),
        "subclasses": {
            "Window_Status": {
                SKOS.definition: Literal("Status of the windows (open, closed)"),
            },
            "Door_Status": {
                SKOS.definition: Literal("Status of the doors (open, closed)"),
            },
            "Lighting_Status": {
                SKOS.definition: Literal("Status of the lightings (on, off)"),
            }
        }
    },
    "Sensor": {
        SKOS.definition: Literal("A Sensor is an input point that represents the value of a device or instrument designed to detect and measure a variable (ASHRAE Dictionary)"),
        "subclasses": {
            "Window_Sensor": {
                SKOS.definition: Literal("A sensor used to monitor the status of the window (open, closed, open angle)"),
            },
            "Wifi_AP": {
                # TODO: address?
                SKOS.definition: Literal("Number of wifi access point"),
            },
            "Shading_Sensor": {
                SKOS.definition: Literal("A sensor used to monitor the status of the shading (on, off)"),
            }
        }
    }
}

define_classes(extension_classes, BRICK.Class, ns=EXT)
define_classes(equipment_extensions, BRICK.Equipment, ns=EXT)
define_classes(point_extensions, BRICK.Status, ns=EXT)

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
        SKOS.definition: Literal("Device is accessible to occupants for adjustment"),
    },
    "Shared": {
        A: EXT.OccupantAccessibilityLevel,
        SKOS.definition: Literal("Device is accessible by multiple occupants"),
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
