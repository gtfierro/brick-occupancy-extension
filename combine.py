import brickschema

g = brickschema.Graph()
g.load_file("enumerations.ttl")
g.load_file("equipment.ttl")
g.load_file("occupants.ttl")
g.load_file("points.ttl")
g.load_file("rules.ttl")
g.load_file("core.ttl")

g.serialize("all.ttl", format="ttl")
