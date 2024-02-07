from flask_app import app
from flask import render_template, redirect, flash, session, request

from flask_app.models.user import User
from flask_app.models.show import Show


@app.route('/shows/new')
def newShow():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    return render_template('newShow.html',loggedUser = User.get_user_by_id(data) )


@app.route('/shows/create', methods = ['POST'])
def createShow():
    if 'user_id' not in session:
        return redirect('/')
    if not Show.validate_show(request.form):
        return redirect(request.referrer)
    data = {
        'title': request.form['title'],
        'network': request.form['network'],
        'releaseDate': request.form['releaseDate'],
        'description': request.form['description'],
        'user_id': session['user_id']
    }
    Show.create(data)
    return redirect('/')

@app.route('/shows/delete/<int:id>')
def deleteShow(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id':session['user_id'],
        'id': id
    }
    user = User.get_user_by_user_id(data)
    show = Show.get_show_by_id(data)
    if user['id'] == show['user_id']:
        Show.deleteAllPostComments(data)
        Show.delete(data)
    return redirect(request.referrer)
    

@app.route('/delete/comment/<int:id>')
def deleteComment(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id':session['user_id'],
        'id': id
    }
    user = User.get_user_by_user_id(data)
    komenti = Show.get_comment_by_id(data)
    if user['id'] == komenti['user_id']:
        Show.deleteComment(data)
    return redirect(request.referrer)

@app.route('/shows/<int:id>')
def showOne(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id':session['user_id'],
        'id': id
    }
    user = User.get_user_by_user_id(data)
    show = Show.get_show_by_id(data)
    return render_template('show.html', show = show, loggedUser = user)



@app.route('/comments/add/<int:id>', methods = ['POST'])
def createComment(id):
    if 'user_id' not in session:
        return redirect('/')
    if 'komenti' not in request.form:
        flash('Komenti eshte mandator', 'komenti')
    data = {
        'user_id':session['user_id'],
        'show_id': id,
        'komenti': request.form['komenti']
    }
    Show.addComment(data)
    return redirect(request.referrer)
