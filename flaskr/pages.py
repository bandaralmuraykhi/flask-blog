from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('pages', __name__, url_prefix='/pages')


# main page with all posts showing
@bp.route('/')
def index():
    db = get_db()
    pages = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM page p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('pages/index.html', pages=pages)



# create post
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO page (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('pages.index'))

    return render_template('pages/create.html')



def get_page(id, check_author=True):
    page = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM page p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if page is None:
        abort(404, f"Page id {id} doesn't exist.")

    if check_author and page['author_id'] != g.user['id']:
        abort(403)

    return page


#update
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    page = get_page(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE page SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('pages.index'))

    return render_template('pages/update.html', page=page)

#delete
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_page(id)
    db = get_db()
    db.execute('DELETE FROM page WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('pages.index'))


