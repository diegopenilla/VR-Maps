'''ZDNA app initializes server, handles everything'''
import markdown
from flask import Flask, url_for, redirect, session
from flask import render_template, request
from flask import Markup
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import Required

from flask_bootstrap import Bootstrap
# My snippets
from snippets import *
import random
import math
import numpy as np
import time

# DATABASE
import pyrebase
config = {
    "apiKey": "AIzaSyBjB-sqssGhOGS3ENH8YRB_CC4fZNwdBNs",
    "authDomain": "treemaps-42314.firebaseapp.com",
    "databaseURL": "https://treemaps-42314.firebaseio.com",
    "projectId": "treemaps-42314",
    "storageBucket": "treemaps-42314.appspot.com",
    "messagingSenderId": "644928997389",
    "appId": "1:644928997389:web:c22c832abeadbad1"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Establish connection with the database

# _ _ _ _
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'epigen'

# ERROR HANDLERS _____________________________________
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
#___________________________________________________

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
# _______________________________________________

@app.route('/example1')
def example1():
    world = create_shape('a-box')
    print(world)
    return render_template('basevr.html') 

@app.route('/example2')
def example2():
    # a-box a-sphere a-plane
    positions = []
    world = ''
    for i in range(300):
        r = lambda: random.randint(0,255)
        c = '#%02X%02X%02X' % (r(),r(),r())
        #world = world + create_text(text='TreeMaps', position = [random.randint(-10,10), random.randint(-10,10), random.randint(-10,10)])
        world = world + create_shape('a-box', color=c, position= [random.randint(0, 100), random.randint(0,100), random.randint(0,100)])
        world = world + create_shape('a-box', color=c, position= [random.randint(30, 30), random.randint(-90, 90), random.randint(0,19)])
        world = world + create_shape('a-sphere', color = c, position = [random.randint(-100,0), random.randint(-100,0), random.randint(-100,0)])
    return render_template('MindMap.html', world=world) 

# not working right now...
@app.route('/mindmap')
def mindmap():
    from py2neo import Graph, Node, Relationship, NodeMatcher
    import snippets
    #[session[levels]] => to VISIT a specific MindMap
    #NOTE: THIS NEEDS HEAVILY REFACTORING
    world, x, y, paths, angles = first_circle('DiegoPenilla', 7)
    #print(len(world))
    #world += next_circle(world, x, y, paths, angles, 7, target='Cube1')
    #world += next_circle(world, x, y, paths, angles, 7, target='Cube2')
    print(len(world))
    return render_template('MindMap.html', world=world) 

# not working right now...
@app.route('/mindmap_secondcircle')
def mindmap_secondcircle():
    from py2neo import Graph, Node, Relationship, NodeMatcher
    import snippets
    #[session[levels]] => to VISIT a specific MindMap
    #NOTE: THIS NEEDS HEAVILY REFACTORING
    world, x, y, paths, angles = first_circle('DiegoPenilla', 7)
    print(len(world))
    world += next_circle(world, x, y, paths, angles, 7, target='Cube1')
    #world += next_circle(world, x, y, paths, angles, 7, target='Cube2')
    print(len(world))
    return render_template('MindMap.html', world=world) 


@app.route('/terminal')
def terminal():
    return render_template('textarea.html')

@app.route('/mindmap2')
def mindmap2():
    world = ''
    world = world + create_text(text='STARTHACKINGBRO', position = [-2, 2, -10])
    for i in range(500):
        #world = world + create_text(text='TreeMaps', position = [random.randint(-10,10), random.randint(-10,10), random.randint(-10,10)])
        world = world + create_text(text="*", position= [random.randint(-10, 10), random.randint(-10,10), random.randint(-10,10)])
    return render_template('MindMap.html', world=world) 


@app.route('/arrow')
def arrow():
    return render_template('index.html')


#@app.route('/example4')
##def example3():
  #  return render_template('AR.html')

@app.route("/markdown")
def markdown():
    return render_template('markdowntest.html')


@app.route("/look")
def lookat():
    return render_template('lookat-2.html')


@app.route('/info')
def info():
    information = open("static/info_program.txt", "r") 
    content = information.read() 
    information.close()
    content = Markup(markdown.markdown(content))
    return render_template('info.html', content=content)

@app.route('/')
def index():
    return render_template('home.html')


class CubeText(FlaskForm):
    '''Form '''
    CubeNameField = StringField('Enter name of your Cube3D', validators=[Required()])
    text = TextAreaField('Enter Text', validators=[Required()])
    submit = SubmitField('Enter Cube')


@app.route('/cube', methods=['GET', 'POST']) 
def cube():
    text = None
    form = CubeText(request.form)
    if 'memory' in session and session['memory'] is not None:
        form.CubeNameField.data = session['memory'][0]
        form.text.data = session['memory'][1]
        session['memory']= None

    if request.method == 'POST' and form.validate_on_submit():
        CubeName = str(form.CubeNameField.data)
        form.CubeNameField.data = ''
        text = str(form.text.data)
        form.text.data = ''
        # content to be uploaded
        db.child('users').child('user').child('worlds').child(CubeName).set(text)
        return render_template('WorldCubeText.html', text=text) 
        
    return render_template('CubeTextForm.html', form=form, text=text)


# _ _ __ _ _ _ _ MEMORY _ _ _ _ _ _ _ _
class MemoryCubes(FlaskForm):
    menu = SelectField("Select a Cube", validators=[Required()])
    remove = BooleanField('Check to delete Cube')
    submit = SubmitField('Submit')


@app.route('/trees', methods=['GET', 'POST'])
def trees():
    form = MemoryCubes(request.form)

    try:    
        cubes = [(str(i), i) for i in db.child('users').child('user').child('worlds').get().val().keys()]
        form.menu.choices = cubes
    except:
        cubes = [("", "")]
        form.menu.choices = cubes

    if form.remove.data == True and request.method == 'POST' and form.validate_on_submit():
        NameCube = form.menu.data
        remove = form.remove.data
        form.menu.data = ''
        form.remove.data = False
        
        # Sequence to be sent to HuntForm
        db.child("users").child('user').child('worlds').child(NameCube).remove()
        try:    
            cubes = [(str(i), i) for i in db.child('users').child('user').child('worlds').get().val().keys()]
            form.menu.choices = cubes
        except:
            cubes = [("", "")]
            form.menu.choices = cubes
        return render_template('trees.html', form=form)

    if request.method == 'POST' and form.validate_on_submit():
        NameCube = form.menu.data
        form.menu.data = ''
        # Sequence to be sent to HuntForm
        session['memory'] = (NameCube, str(db.child('users').child('user').child('worlds').get().val()[NameCube]).strip())
        return redirect(url_for('cube'))

    # memory of trees html
    return render_template('trees.html', form=form)

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port=5000)


