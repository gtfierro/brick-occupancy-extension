import brickschema

g = brickschema.Graph()
g.load_file("extension.ttl")
g.load_file("example1.ttl")
# "compile" model
g.expand("owlrl+shacl")

# get all shared equipment
res = g.query("SELECT ?shared_equip WHERE { ?shared_equip occ:occupantAccessibility/brick:value occ:Shared }")
print(list(res))

# get all adjustable equipment
res = g.query("SELECT ?shared_equip WHERE { ?shared_equip occ:occupantAccessibility/brick:value occ:Adjustable }")
print(list(res))

# get all equipment used by employees in the 26-34 age range
res = g.query("SELECT ?equip ?occ WHERE { ?equip occ:isAccessibleBy ?occ . ?occ occ:ageRange  occ:26_34 }")
for row in res:
    print(row)
