from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from . import db
from .models import Post
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os
import secrets

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)


def save_imges(photo):
    if photo and isinstance(photo, FileStorage):
        hash_photo = secrets.token_urlsafe(16)
        file_extension = os.path.splitext(photo.filename)[
            1]  # Extract file extension
        photo_name = hash_photo + file_extension
        file_path = os.path.join(
            current_app.root_path, 'static/uploads', photo_name)
        photo.save(file_path)
        return photo_name
    else:
        return None


@views.route('/creat-post', methods=['POST'])
@login_required
def create_post():
    if request.method == "POST":
        caption = request.form.get("caption")
        photo = save_imges(request.files.get('photo'))
        if not photo:
            return 'No pic uploaded!', 400

        new_post = Post(caption=caption, post_image=photo,
                        author=current_user.id)

        db.session.add(new_post)
        db.session.commit()
        flash('Post Created!', category='success')
        return redirect(url_for('views.home'))


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    file_path = os.path.join(
        current_app.root_path, 'static/uploads', post.post_image)
    if os.path.exists(file_path):
        os.remove(file_path)
    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.user.id:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.home'))
