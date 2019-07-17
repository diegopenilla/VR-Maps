"""Create a node in Neo4j the hard way"""

from py2neo import Graph, Node, Relationship, NodeMatcher
#uri = "bolt://0.0.0.0:7687" for local computer and docker (below):
g = Graph(uri='bolt://0.0.0.0:7687', user="neo4j", password="Chipichapes")
#g = Graph(uri='bolt://db:7687', user="neo4j", password="Chipichapes")
def write(cypher): return g.run(cypher).evaluate

session_id = {}
id_count = 0
def create_nodes(type, dicto):
    global id_count
    # if type does not exist initialize list
    if type not in session_id.keys():
        session_id[type] = []
    # constructs properties added from dicto
    no_keys = len(dicto.keys())
    current = 1
    properties = ''
    for key in dicto.keys():
        properties += '%s:"%s"'% (key, dicto[key])
        if current < no_keys:
            properties += ','
        current+=1
    #adds them into create node 
    q = "CREATE (`%s` :%s {%s})" % (id_count, type, properties)
    try:
        # running cypher
        g.run(q).evaluate()
        # updating list of nodes with same type, with ids
        current_list = session_id[type]
        current_list.append(id_count)
        session_id[type]=current_list
        # change id for the next node
        id_count +=1 
    except:
        print("Wrong query given")
    return "Created"
    

dicto = {
"name":"MindMap",
"image":"https://simplemind.eu/wp-content/uploads/2017/01/vakantie-2016-reading-figuur-1-1024x569.png",
"markdown": "# Title This is Working",
"code":"echo vamos",
}

create_nodes('MindMap' , dicto)

def anneal_nodes(parent_id, childs):
    links = ''
    for i in childs:
        links+= '(`%s`)-[:`LINKS` ]->(`%s`)' % (parent_id, i)
    q = "CREATE %s" % (links)
    g.run(q).evaluate()
