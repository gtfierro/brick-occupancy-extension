from rdflib import Literal
from ns import BRICK, OWL, RDFS, EXT, A, SKOS

# TODO: add definitions
properties = {
    "hasAccessTo": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        OWL.inverseOf: BRICK["isAccessibleBy"],
        SKOS.definition: Literal("i need to be defined"),
        RDFS.domain: EXT.Occupant,
        RDFS.range: BRICK.Location,
    },
    "isAccessibleBy": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        OWL.inverseOf: BRICK["hasAccessTo"],
        SKOS.definition: Literal("i need to be defined"),
        RDFS.domain: BRICK.Location,
        RDFS.range: EXT.Occupant,
    },
    "hasDegreeOfControl": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        SKOS.definition: Literal("i need to be defined"),
        RDFS.domain: BRICK.Equipment,
        RDFS.range: EXT.DegreeOfControl,
    },
    "hasOccupantAccessibilityLevel": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        SKOS.definition: Literal("i need to be defined"),
        RDFS.domain: BRICK.Equipment,
        RDFS.range: EXT.OccupantAccessibilityLevel,
    },
    "hasModeOfControl": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        SKOS.definition: Literal("i need to be defined"),
        RDFS.domain: BRICK.Equipment,
        RDFS.range: EXT.ModeOfControl,
    },
}
