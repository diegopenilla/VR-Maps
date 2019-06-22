def create_text(text, position):
    pos = ''
    for i in position:
        pos +=' '+str(i)
    pos = pos[1:]
    tag = '''<a-entity position="{}" text="width: 2; lineHeight: 50; letterSpacing: 5; color: white; value: {}"></a-entity>'''.format(position, text)
    tag = tag.replace("\n", "")
    return str(tag)


def create_shape(object, position, color):
    '''Objects: a-box, a-sphere, a-cylinder, a-plane, a-sky, position is a listcat'''
    object = str(object)
    global positions
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