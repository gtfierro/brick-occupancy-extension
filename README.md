# Occupancy Modeling Extension

Look at `extension.ttl` for the ontology extension definition. Look at `example1.ttl` for usage. Look at `sample_queries.py` for what it says on the tin.

## Occupants

The extension introduces some classes for describing properties of the building occupants. An `Occupant` is any individual or group of individuals. An `Individual` is a subclass of Occupant corresponding to a single individual. A `Group` is also a subclass of `Occupant`.

Occupant Properties:
- `occ:isMemberOf <Group>`: an occupant can be a member of a group. This allows nested groups
- `occ:uses <Equipment>`: an occupant can use equipment.
- `occ:ageRange <range>`: an occupant can have an associated age range
- `occ:label <string>`: a human-readable label associated with the occupant

Individual Properties:
- An individual can have any or all of the properties associated with an Occupant, including...
- `occ:age <value>`: the exact age of an individual. Can be in years, months, days, etc
- `occ:gender <value>`: the surveyed gender of an occupant
- `occ:ethnicity <value>`: the surveyed ethnicity of an occupant

Group Properties:
- A group can have any or all of the properties associated with an occupant, including...
- `occ:hasMember <Occupant>`: the inverse relationship of `occ:isMemberOf`
- `occ:groupSize <integer>`: the number of individuals in a group

### Surveyed Values

For items like age range, gender and ethnicity it is important to capture not just the value that was surveyed, but also the range of values that was contained in the survey. A possible way of modeling this has been done for `AgeRange`, but not for `ethnicity` or `gender` (yet).

How does it work? An `occ:AgeRange` class is declared with several pre-declared instances: `occ:18_25`, `occ:26_34`, `occ:35_50` and `occ:51_plus`. There are annotations on these instances which explicitly denote the upper/lower bounds of each age range, but I'll omit that here for simplicity. In the `example1.ttl` file, the value of the `occ:ageRange` property for an Occupant entity is one of these range instances. For surveys with *different* ranges, the data graph should define its own classes with the `occ:upperBound` and `occ:lowerBound` properties to denote what the actual age ranges are.

## Equipment

The extension introduces several new classes of equipment:

- Ceiling Fan
- Personal Devices:
    - Portable Fan
    - Portable Heater
    - Desktop Light
- Envelope Equipment:
    - Door
    - Window

The extension supports several kinds of annotations on equipment entities:
- `occ:degreeOfControl`: manual, dynamic or automatic
- `occ:occupantAccessibility`: shared, adjustable or not accessible
- `occ:usedBy <Occupant>`: denotes which occupants, individuals or groups make use of an equipment. If at least 1 occupant uses an equipment, the ontology will infer the `Adjustable` property for the equipment. If at least 2 occupants use an equipment then the ontology will also infer the `Shared` property.
