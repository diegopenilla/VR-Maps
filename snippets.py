# We will need to work out some math to get the text at the right positions. 
# circle_positions: we will have circles of different radiuses satisfying the equation: levels = (x^2 + y^2)
# circle_angles: we split the 360 degrees in the number of nodes we have at that level.
# x and y positions given at x= r*cos(angle) and y = r*sin(angle)

import math

def find_paths(name):
    import time
    from py2neo import Graph, Node, Relationship, NodeMatcher
    user = "neo4j"
    password = "Chipichapes"
    g = Graph(uri='bolt://0.0.0.0:7687/', user=user, password=password)
    time.sleep(1)
    cursor = g.run("MATCH (n)-[r]->() WHERE n.name = '{}' RETURN COUNT(r)".format(name))
    number_paths =  cursor.evaluate()
    cursor = g.run("MATCH (n)-[r]->(a) WHERE n.name = '{}' RETURN a".format(name))
    paths = []
    for record in cursor:
        paths.append(dict(record['a'])['name'])
    # find_paths('DiegoPenilla') 
    return number_paths, paths

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
