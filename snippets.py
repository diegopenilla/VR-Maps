"""Database and VR snippets together, to be separated"""

# We will need to work out some math to get the text at the right positions. 
# circle_positions: we will have circles of different radiuses satisfying the equation: levels = (x^2 + y^2)
# circle_angles: we split the 360 degrees in the number of nodes we have at that level.
# x and y positions given at x= r*cos(angle) and y = r*sin(angle)
import math
import time
from py2neo import Graph, Node, Relationship, NodeMatcher

#uri = "bolt://0.0.0.0:7687"
user = "neo4j"
password = "Chipichapes"
# for docker container
g = Graph(uri='bolt://db:7687', user=user, password=password)
# for my computer
#g = Graph(uri='bolt://0.0.0.0:7687', user=user, password=password)

def find_paths(name):
    time.sleep(1)
    cursor = g.run("MATCH (n)-[r]->() WHERE n.name = '{}' RETURN COUNT(r)".format(name))
    number_paths =  cursor.evaluate()
    cursor = g.run("MATCH (n)-[r]->(a) WHERE n.name = '{}' RETURN a".format(name))
    paths = []
    for record in cursor:
        paths.append(dict(record['a'])['name'])
    # find_paths('DiegoPenilla') 
    return number_paths, paths
# find_paths("DiegoPenilla") => root of the tree
opa = """
CREATE 
  (`2` :MindMap {name:"Physics",image:"https://simplemind.eu/wp-content/uploads/2017/01/vakantie-2016-reading-figuur-1-1024x569.png"}) ,
  (`3` :Cube1 {name:"Calculus",image:"https://simplemind.eu/wp-content/uploads/2017/01/vakantie-2016-reading-figuur-1-1024x569.png"}) ,
  (`2`)-[:`LINKS` ]->(`3`)
"""

def find_paths_type(name, type='name'):
    time.sleep(1)
    cursor = g.run("MATCH (n)-[r]->() WHERE n.{} = '{}' RETURN COUNT(r)".format(type, str(name)))
    number_paths =  cursor.evaluate()
    cursor = g.run("MATCH (n)-[r]->(a) WHERE n.{}= '{}' RETURN a".format(type, str(name)))
    paths = []
    for record in cursor:
        paths.append(dict(record['a'])['{}'.format(type)])
    # find_paths('DiegoPenilla') 
    return number_paths, paths


# to download images
def download_image(img_url='https://websunsay.pp.ua/img/workplace.jpg', output='image.jpg'):
    wget.download(img_url, f'temp/{output}')  



def circle_positions(name, radius):
    number_paths, paths = find_paths(name)
    whole_circle = 2*math.pi
    path_angle = whole_circle/number_paths
    angle = 0
    x, y  = [],[]
    for i in range(number_paths):
        x.append(radius*math.cos(angle))
        y.append(radius*math.sin(angle))
        angle += path_angle
    return x, y, paths

def create_img(img, position):
    pos = ''
    for i in position:
        pos +=' '+str(i)
    pos = pos[1:]
    tag = '<a-image src="/static/{}" position="{}"></a-image>'.format(img)
    tag = tag.replace("\n", "")
    return tag

def create_text(text, position, look_at = True):
    # transforms list into right format
    pos = ''
    for i in position:
        pos +=' '+str(i)
    pos = pos[1:]
    # text tags look towards the camera
    if look_at == True:
        tag = '''<a-entity position="{}" look-at="#look-cam" text="width: 5; lineHeight: 50; letterSpacing: 5; color: white; value: {}"></a-entity>'''.format(pos, text)
    else:
        tag = '''<a-entity position="{}" text="width: 2; lineHeight: 50; letterSpacing: 5; color: white; value: {}"></a-entity>'''.format(pos, text)
    return tag


def create_shape(object, position, color):
    '''Objects: a-box, a-sphere, a-cylinder, a-plane, a-sky, position is a listcat'''
    object = str(object)
    positions = []
    for i in positions:
        while abs(i[0] - position[0]) < 5 or abs(i[1] - position[1]) < 5 or abs(i[2] - position[2]) < 5:
            print('happening')
            position = [random.randint(-100,100), random.randint(-100,10), random.randint(-10,10)]
    positions.append(position)

    pos = ''
    for i in position:
        pos +=' '+str(i)
    pos = pos[1:]

    tag = '''<{} position="{}" rotation="0 0 0" color="{}"></{}>'''.format(object, pos, color, object)
    tag = tag.replace("\n", "")
    return str(tag)


      #<a-entity position="-5 2 -9" look-at="#look-cam" text="width: 2; lineHeight: 50; letterSpacing: 5; color: white; value: Funciono!!"></a-entity>
