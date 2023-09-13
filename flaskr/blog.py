from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort


from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__, url_prefix='/blog')

# # main page with all posts showing
@bp.route('/')
def index():
    try:
        db = get_db()
        if g.user:
            # Retrieve published posts and the logged-in user's posts
            posts = db.execute(
                'SELECT p.id, title, body, created, author_id, username, published'
                ' FROM post p JOIN user u ON p.author_id = u.id'
                ' WHERE published = 1 OR p.author_id = ?'
                ' ORDER BY created DESC',
                (g.user['id'],)
            ).fetchall()

        else:
            # Retrieve only published posts
            posts = db.execute(
                'SELECT p.id, title, body, created, author_id, username'
                ' FROM post p JOIN user u ON p.author_id = u.id'
                ' WHERE published = 1'
                ' ORDER BY created DESC'
            ).fetchall()
        
        return render_template('blog/index.html', posts=posts)
    
    except Exception as e:
        flash('An error occurred while loading the posts. Please try again later.')
        # Log the exact error for debugging purposes
        current_app.logger.error(str(e))
        return render_template('error.html')
# get post page (helper function) no need for login_required
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

#View page
@bp.route('/<int:id>/view', methods=['GET'])
@login_required
def view_post(id):
    post = get_post(id, check_author=False)
    return render_template('blog/view.html', post=post)

# create post
@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        # Check if the checkbox for published is ticked off
        published = 'published' in request.form 
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id, published)' # Add the published column here
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['id'], published)  # set published based on checkbox state
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/<int:id>/publish', methods=['POST'])
@login_required
def publish(id):
    post = get_post(id, check_author=True)
    db = get_db()
    db.execute(
        'UPDATE post SET published = ? WHERE id = ?',
        (not post['published'], id)  # Toggle the published status
    )
    db.commit()
    return redirect(url_for('blog.index'))
    

# update post
@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    post = get_post(id, check_author=True)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        published = 'published' in request.form  # Check if the checkbox is ticked
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?, published = ?'
                ' WHERE id = ?',
                (title, body, published, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

# delete post
@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    get_post(id, check_author=True)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

