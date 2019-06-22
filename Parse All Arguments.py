# get the arguments of aframe automatically using a function
aframe_objects = \
    """<a-box position="-1 0.5 -3" rotation="0 45 0" color="#4CC3D9"></a-box>/n
       <a-sphere position="0 1.25 -5" radius="1.25" color="#EF2D5E"></a-sphere>/n
       <a-cylinder position="1 0.75 -3" radius="0.5" height="1.5" color="#FFC65D"></a-cylinder>/n
       <a-plane position="0 0 -4" rotation="-90 0 0" width="4" height="4" color="#7BC8A4"></a-plane>/n
       <a-sky color="#ECECEC"></a-sky>/n"""


args = [tag.strip() for tag in aframe_objects.split('/n')] 
def extract(s, no):
    return s[1:].split()[no]

arguments = []
unparsed_tag_args = []
for a in args:
    try:
        arguments.append(extract(a, 0))
        unparsed_tag_args.append([i.split(' ') for i in a.split("=")])
    except:
        pass

tag_arguments = []
for tag_arg in unparsed_tag_args:
    tag_args = []
    for element in tag_arg:
        if element[-1][-1] != '>':
            tag_args.append(element[-1])
    tag_arguments.append(tag_args)

for arg, args in zip(arguments, tag_arguments):
    if '-' in arg:
        arg = arg[arg.index('-')+1:]
    exec("""
def {}({}):
    for i in argv:
        print(i)
    return("<")


""".format(arg, "*argv"))
    print(arg, args)

def tag(*argv):
    for i in argv:
        print("""
global {}
{} = str({})""".format(i, i, i))

    #print("<{}> </{}>".format(tag, ))