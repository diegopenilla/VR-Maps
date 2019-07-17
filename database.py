# Establish connection with the database
from py2neo import Graph, Node, Relationship, NodeMatcher
import time
uri = "bolt://0.0.0.0:7687"
user = "neo4j"
password = "Chipichapes"

# Creating Graphc
g = Graph(uri=uri, user=user, password=password)
g.delete_all()
time.sleep(2)
# Constraints g.schema.create_uniqueness_constraint(root_type, root)
# Matcher
matcher = NodeMatcher(g)

print(len(g.nodes))

print(len(g.relationships))
# Need to insert this into the VR Application LOOKSAMAZING
# Create nodes (if they don't exist) and link them
def parent_child(root_type, branch_type,root, branch):
    a = Node(root_type, name=root)
    b = Node(branch_type, name=branch)
    LINKS = Relationship.type("LINKS")
    g.merge(LINKS(a, b), root_type, "name")

# create connections from root to branches.
def sprout(root_type, branch_type,root, branches):
    for branch in branches:
        parent_child(root_type, branch_type,root, branch)

# First Level _ _ _ _ _ _ _  _ 
branches = ['TreeMaps', 'Akelius', 'Z-Hunt', 'WATTx', 'Medium', 'CV', 'Learning']
sprout('MindMap', 'Cube', 'DiegoPenilla', branches)


# Second Level _ _ _ _ _ _ _ _ _
treemaps = ['Tech', 'Business', 'Design']
sprout("Cube", 'Cube1', 'TreeMaps', treemaps)

wattx = ['KostyaCode']
sprout('Cube', 'Cube1', 'WATTx', wattx)

medium = ['PlayGuitar', 'JupyterButtons', 'AzureCognitive']
sprout('Cube', 'Cube1', "Medium", medium)

akelius = ['Invoice', 'Projects']
sprout("Cube", "Cube1", "Akelius", akelius)

zhunt = ['Flask App', 'Current']
sprout("Cube", 'Cube1', 'Z-Hunt', zhunt)

learning = ['Raspberrypi', 'Docker', 'AI', 'DataBases', 'Guitar']
sprout("Cube", 'Cube1', 'Learning', learning)

# 3rd Level

guitar = ['Theory', 'Songs', 'Logic Pro']
sprout('Cube1', 'Cube2', 'Guitar', guitar)

database = ['Firebase', 'Neo4j']
sprout('Cube1', 'Cube2', 'DataBases', database)

ai = ['Tensorflow', 'ScikitLearn']
sprout('Cube1', 'Cube2', 'AI', ai)

docker = ['CookBook.pdf', 'UsingDocker.pdf', 'Images']
sprout('Cube1', 'Cube2', 'Docker', docker)

raspberry = ['Actuators', 'Actions']
sprout('Cube1', 'Cube2', 'Raspberrypi', raspberry)

projects = ['Transaction', 'Offer']
sprout('Cube1', 'Cube2', 'Projects', projects)


# Cube Level 3
projects = ['Camera', 'Speaker', 'Microphone']
sprout('Cube2', 'Cube3', 'Actuators', projects)

for i in ['Stairway To Heaven', 'Just Jamming', 'Destiny', 'Femme de Argent','Perdonar es Divino','Uno Entre 1000']:
    parent_child('Cube2', 'Cube3','Songs', i)

for i in ['Scales','Chords']:
    parent_child("Cube2", 'Cube3', 'Theory', i)

print(len(g.nodes))
print(len(g.relationships))

