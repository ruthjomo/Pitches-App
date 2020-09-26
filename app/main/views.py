from flask import render_template, redirect, url_for, abort, request
from . import main
from flask_login import login_required, current_user
from ..models import User, Comment, Pitch
from .forms import UpdateProfile, CommentForm, PitchForm
from .. import db, photos



vote=0
def Upvote(pitch):
    if pitch:
        vote=0
        vote=pitch+1

    return vote



def Downvote(pitch):
    if pitch:
        vote=0
        vote=pitch+1

    return vote

@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    return render_template('index.html')
    


@main.route('/product')
def product():
    '''
    View root page function that returns the index page and its data
    '''
    pitches = Pitch.get_pitches(id)
    return render_template('product.html', pitches=pitches)


@main.route('/pickup')
def pickup():
    '''
    View root page function that returns the index page and its data
    '''
    pitches = Pitch.get_pitches(id)
    return render_template('pickup.html')


@main.route('/product/pitch', methods=['GET', 'POST'])
@login_required
def productpitch():
    '''
    View root page function that returns the index page and its data
    '''
    form = PitchForm()

    if form.validate_on_submit():
        title = form.title.data
        pitch = form.pitch.data
        new_pitch = Pitch(title=title, pitch=pitch, user=current_user)
        new_pitch.save_pitch()
        return redirect(url_for('main.product'))

    return render_template('pitch.html', pitch_form=form)


@main.route('/pickup/pitch', methods=['GET', 'POST'])
@login_required
def pickuppitch():
    '''
    View root page function that returns the index page and its data
    '''
    form = PitchForm()

    if form.validate_on_submit():
        title = form.title.data
        pitch = form.pitch.data
        new_pitch = Pitch(title=title, pitch=pitch, user=current_user)
        new_pitch.save_pitch()
        return redirect(url_for('main.pickup'))

    return render_template('pitch.html', pitch_form=form)


@main.route('/product/comment', methods=['GET', 'POST'])
@login_required
def pnew_comment():

    form = CommentForm()

    comments = Comment.query.all()
    if form.validate_on_submit():
        comment = form.comment.data

        new_comment = Comment(comment=comment)
        # new_comment.save_comment()
        db.session.add(new_comment)
        db.session.commit()

    return render_template('comment.html', comment_form=form, comment=comments)


@main.route('/pickup/comment', methods=['GET', 'POST'])
@login_required
def new_comment():

    # user = User.query.filter_by(username = uname).first()
    # if user is None:
    #     abort(404)

    form = CommentForm()

    comments = Comment.query.all()
    if form.validate_on_submit():
        comment = form.comment.data

        new_comment = Comment(comment=comment)
        # new_comment.save_comment()
        db.session.add(new_comment)
        db.session.commit()

    return render_template('comment.html', comment_form=form)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form)


@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))

@main.route('/<int:pname>/comment',methods=['GET','POST'])
@login_required
def comment(pname):
    comments=CommentsForm()
    image=url_for('static',filename='profile/'+ current_user.profile_pic_path)
    pitch=Pitch.query.filter_by(id=pname).first()
    comment_query=Comment.query.filter_by(pitch_id=pitch.id).all()
    
    if request.args.get('likes'):
        pitch.upvotes=pitch.upvotes+int(1)
        db.session.add(pitch)
        db.session.commit()
        return redirect(url_for('main.comment',pname=pname))

    
    elif    request.args.get('dislike'):
        pitch.downvotes=pitch.downvotes+int(1)
        db.session.add(pitch)
        db.session.commit()
        return redirect(url_for('main.comment',pname=pname))

    if comments.validate_on_submit():
        comment=Comment(comment=comments.comment.data,pitch_id=pitch.id,user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('main.comment',pname=pname))
    
    return render_template('pitch.html' ,comment=comments,pitch=pitch,comments=comment_query,title='Pitch Comment',image=image)   