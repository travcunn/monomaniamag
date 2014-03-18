import datetime
import hashlib
import os
import time

from flask import abort, flash, g, redirect, render_template, request, \
        url_for
from flask.ext.login import current_user, login_required, login_user, \
        logout_user
from werkzeug import secure_filename

from sqlalchemy.orm import defer

from app import app, db, login_manager
from config import ALBUM_REVIEWS_PER_PAGE
from forms import AlbumReviewForm, AlbumReviewFormDelete, \
        AlbumReviewFormEdit, LoginValidator, NewsForm
from models import AlbumReview, Article, User


login_manager.login_view = 'login'

@app.route('/')
def home():
    news_articles = Article.query.options(defer('content'))
    ordered_articles = news_articles.order_by(Article.pub_date.desc())
    panel_news = ordered_articles.paginate(0, 4, False)

    # Album reviews query
    album_reviews = AlbumReview.query.options(defer('content'))
    ordered_reviews = album_reviews.order_by(AlbumReview.pub_date.desc())
    panel_album_reviews = ordered_reviews.paginate(0, 4, False)

    return render_template('home.html',
                           panel_album_reviews=panel_album_reviews,
                           news=panel_news)

@app.route('/news')
def news():
    album_reviews = Article.query.options(defer('content'))

    ordered_reviews = album_reviews.order_by(Article.pub_date.desc())
    panel_album_reviews = ordered_reviews.paginate(0, 4, False)

    return render_template('news.html', news=panel_album_reviews)

@app.route('/news/new', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        upload = secure_filename(form.upload.data.filename)
        name, extension = os.path.splitext(upload)
        filename_hash = hashlib.sha1(str(time.time()))
        filename = str(filename_hash.hexdigest()) + str(extension)
        form.upload.data.save(os.path.join(app.config['BASEDIR'], 'static', 'news',
                                           filename))

        article_url = form.title.data.replace(" ", "-").lower()

        review = Article(page_title=form.title.data, preview=form.preview.data,
                         featured=form.featured.data, photo=filename,
                         content=form.content.data,
                         pub_date=datetime.datetime.utcnow(),
                         url=article_url, author=g.user)
        db.session.add(review)
        db.session.commit()
        flash('The news article was created and published.')
        return redirect(url_for('news'))

    return render_template('new-news-article.html', title='Add News Article',
                           form=form)

@app.route('/news/<article_url>')
def single_news_article(article_url):
    review = AlbumReview.query.filter_by(url=article_url).first()
    if review is None:
        abort(404)

    side_reviews = AlbumReview.query.options(defer('content'))
    sorted_side_reviews = side_reviews.order_by(AlbumReview.pub_date.desc())
    shown_side_reviews = sorted_side_reviews.paginate(0, 6, False)

    delete_form = AlbumReviewFormDelete()

    return render_template('album-review.html', title=review.page_title,
                           review=review, side_reviews=shown_side_reviews,
                           delete_form=delete_form)

@app.route('/reviews/album')
@app.route('/reviews/album/page/<int:page>', methods = ['GET', 'POST'])
def album_reviews(page=1):
    reviews = AlbumReview.query.options(defer('content'))
    sorted_reviews = reviews.order_by(AlbumReview.pub_date.desc())
    shown_reviews = sorted_reviews.paginate(page, ALBUM_REVIEWS_PER_PAGE,
                                            False)
    if len(shown_reviews.items) is 0:
        if page is 1:
            flash("There are no reviews yet.", 'info')
        else:
            abort(404)

    return render_template('album-reviews.html', title='Album Reviews',
                           reviews=shown_reviews)

@app.route('/reviews/track')
@app.route('/reviews/track/page/<int:page>', methods = ['GET', 'POST'])
def track_reviews(page=1):
    reviews = TrackReview.query.options(defer('content'))
    sorted_reviews = reviews.order_by(TrackReview.pub_date.desc())
    shown_reviews = sorted_reviews.paginate(page, TRACK_REVIEWS_PER_PAGE,
                                            False)
    if len(shown_reviews.items) is 0:
        if page is 1:
            flash("There are no reviews yet.", 'info')
        else:
            abort(404)

    return render_template('track-reviews.html', title='Track Reviews',
                           reviews=shown_reviews)

@app.route('/reviews/artist')
@app.route('/reviews/artist/page/<int:page>', methods = ['GET', 'POST'])
def track_reviews(page=1):
    reviews = ArtistReview.query.options(defer('content'))
    sorted_reviews = reviews.order_by(ArtistReview.pub_date.desc())
    shown_reviews = sorted_reviews.paginate(page, ARTIST_REVIEWS_PER_PAGE,
                                            False)
    if len(shown_reviews.items) is 0:
        if page is 1:
            flash("There are no reviews yet.", 'info')
        else:
            abort(404)

    return render_template('artist-reviews.html', title='Artist Reviews',
                           reviews=shown_reviews)

@app.route('/reviews/album/<review_url>')
def single_album_review(review_url):
    review = AlbumReview.query.filter_by(url=review_url).first()
    if review is None:
        abort(404)

    side_reviews = AlbumReview.query.options(defer('content'))
    sorted_side_reviews = side_reviews.order_by(AlbumReview.pub_date.desc())
    shown_side_reviews = sorted_side_reviews.paginate(0, 6, False)

    delete_form = AlbumReviewFormDelete()

    return render_template('album-review.html', title=review.page_title,
                           review=review, side_reviews=shown_side_reviews,
                           delete_form=delete_form)

@app.route('/reviews/track/<review_url>')
def single_track_review(review_url):
    review = TrackReview.query.filter_by(url=review_url).first()
    if review is None:
        abort(404)

    side_reviews = TrackReview.query.options(defer('content'))
    sorted_side_reviews = side_reviews.order_by(TrackReview.pub_date.desc())
    shown_side_reviews = sorted_side_reviews.paginate(0, 6, False)

    delete_form = TrackReviewFormDelete()

    return render_template('track-review.html', title=review.page_title,
                           review=review, side_reviews=shown_side_reviews,
                           delete_form=delete_form)

@app.route('/reviews/artist/<review_url>')
def artist_track_review(review_url):
    review = ArtistReview.query.filter_by(url=review_url).first()
    if review is None:
        abort(404)

    side_reviews = ArtistReview.query.options(defer('content'))
    sorted_side_reviews = side_reviews.order_by(ArtistReview.pub_date.desc())
    shown_side_reviews = sorted_side_reviews.paginate(0, 6, False)

    delete_form = ArtistReviewFormDelete()

    return render_template('arist-review.html', title=review.page_title,
                           review=review, side_reviews=shown_side_reviews,
                           delete_form=delete_form)

@app.route('/reviews/album/<review_url>/<action>', methods=['GET', 'POST'])
def album_review_action(review_url, action):
    review = AlbumReview.query.filter_by(url=review_url).first()
    if review is None:
        abort(404)

    if action == "edit":
        form = AlbumReviewFormEdit()
        if request.method == 'POST':
            if form.validate_on_submit():
                review.artist = form.artist.data
                review.album = form.album.data
                review.content = form.content.data

                review_title = "%s - %s" % (form.artist.data, form.album.data)
                url_base = "%s %s" % (form.artist.data, form.album.data)
                review_url = url_base.replace(" ", "-").lower()
                review.page_title = review_title
                review.url = review_url

                db.session.commit()

                flash('Saved successfully.', 'success')
                return redirect(url_for('single_album_review',
                                        review_url=review.url))

        return render_template('edit-album-review.html', title="Edit Review",
                               review=review, form=form)

    elif action == "delete":
        form = AlbumReviewFormDelete()
        if request.method == 'POST':
            if form.validate_on_submit():
                # delete the review image
                img_path = os.path.join(app.config['BASEDIR'],
                                        'static/reviews/',
                                        review.photo)
                os.remove(img_path)

                db.session.delete(review)
                db.session.commit()

                flash('Deleted successfully.', 'success')
                return redirect(url_for('album_reviews'))
            else:
                return redirect(url_for('single_album_review',
                                        review_url=review.url))
        else:
            abort(404)

@app.route('/reviews/track/<review_url>/<action>', methods=['GET', 'POST'])
def track_review_action(review_url, action):
    review = TrackReview.query.filter_by(url=review_url).first()
    if review is None:
        abort(404)

    if action == "edit":
        form = TrackReviewFormEdit()
        if request.method == 'POST':
            if form.validate_on_submit():
                review.artist = form.artist.data
                review.album = form.album.data
                review.content = form.content.data
		review.name = form.name.data

                review_title = "%s - %s" % (form.artist.data, form.track.data)
                url_base = "%s %s" % (form.artist.data, form.track.data)
                review_url = url_base.replace(" ", "-").lower()
                review.page_title = review_title
                review.url = review_url

                db.session.commit()

                flash('Saved successfully.', 'success')
                return redirect(url_for('single_track_review',
                                        review_url=review.url))

        return render_template('edit-track-review.html', title="Edit Review",
                               review=review, form=form)

    elif action == "delete":
        form = TrackReviewFormDelete()
        if request.method == 'POST':
            if form.validate_on_submit():
                # delete the review image
                img_path = os.path.join(app.config['BASEDIR'],
                                        'static/reviews/',
                                        review.photo)
                os.remove(img_path)

                db.session.delete(review)
                db.session.commit()

                flash('Deleted successfully.', 'success')
                return redirect(url_for('track_reviews'))
            else:
                return redirect(url_for('single_track_review',
                                        review_url=review.url))
        else:
            abort(404)

@app.route('/reviews/artist/<review_url>/<action>', methods=['GET', 'POST'])
def artist_review_action(review_url, action):
    review = ArtistReview.query.filter_by(url=review_url).first()
    if review is None:
        abort(404)

    if action == "edit":
        form = ArtistReviewFormEdit()
        if request.method == 'POST':
            if form.validate_on_submit():
                review.artist = form.artist.data
                review.album = form.album.data
                review.content = form.content.data
		review.name = form.name.data

                review_title = "%s" % (form.artist.data)
                url_base = "%s" % (form.artist.data)
                review_url = url_base.replace(" ", "-").lower()
                review.page_title = review_title
                review.url = review_url

                db.session.commit()

                flash('Saved successfully.', 'success')
                return redirect(url_for('single_artist_review',
                                        review_url=review.url))

        return render_template('edit-artist-review.html', title="Edit Review",
                               review=review, form=form)

    elif action == "delete":
        form = ArtistReviewFormDelete()
        if request.method == 'POST':
            if form.validate_on_submit():
                # delete the review image
                img_path = os.path.join(app.config['BASEDIR'],
                                        'static/reviews/',
                                        review.photo)
                os.remove(img_path)

                db.session.delete(review)
                db.session.commit()

                flash('Deleted successfully.', 'success')
                return redirect(url_for('track_reviews'))
            else:
                return redirect(url_for('single_artist_review',
                                        review_url=review.url))
        else:
            abort(404)

@app.route('/reviews/album/new', methods=['GET', 'POST'])
@login_required
def add_new_album_review():
    form = AlbumReviewForm()
    if form.validate_on_submit():
        upload = secure_filename(form.upload.data.filename)
        name, extension = os.path.splitext(upload)
        filename_hash = hashlib.sha1(str(time.time()))
        filename = str(filename_hash.hexdigest()) + str(extension)
        form.upload.data.save(os.path.join(app.config['BASEDIR'], 'static', 'reviews',
                                           filename))

        review_title = "%s - %s - Album Review" % (form.artist.data,
                                                   form.album.data)
        url_base = "%s %s Album Review" % (form.artist.data, form.album.data)
        review_url = url_base.replace(" ", "-").lower()

        review = AlbumReview(artist=form.artist.data, album=form.album.data,
                             photo=filename, content=form.content.data,
                             pub_date=datetime.datetime.utcnow(),
                             author=g.user, page_title=review_title,
                             url=review_url)
        db.session.add(review)
        db.session.commit()
        flash('The album review was created and published.')
        return redirect(url_for('reviews'))

    return render_template('new-album-review.html', title='Add New Review',
                           form=form)


@app.route('/reviews/track/new', methods=['GET', 'POST'])
@login_required
def add_new_track_review():
    form = TrackReviewForm() #!#
    if form.validate_on_submit():
        upload = secure_filename(form.upload.data.filename)
        name, extension = os.path.splitext(upload)
        filename_hash = hashlib.sha1(str(time.time()))
        filename = str(filename_hash.hexdigest()) + str(extension)
        form.upload.data.save(os.path.join(app.config['BASEDIR'], 'static', 'reviews',
                                           filename))

        review_title = "%s - %s - Track Review" % (form.artist.data,
                                                   form.name.data)
        url_base = "%s %s Track Review" % (form.artist.data, form.name.data)
                             pub_date=datetime.datetime.utcnow(),
        review_url = url_base.replace(" ", "-").lower()

        review = TrackReview(artist=form.artist.data, album=form.album.data,
                             photo=filename, content=form.content.data,
                             author=g.user, page_title=review_title,
                             url=review_url, name=form.name.data)
        db.session.add(review)
        db.session.commit()
        flash('The track review was created and published.')
        return redirect(url_for('reviews'))

    return render_template('new-track-review.html', title='Add New Review',
                           form=form)

@app.route('/reviews/artist/new', methods=['GET', 'POST'])
@login_required
def add_new_artist_review():
    form = ArtistReviewForm()
    if form.validate_on_submit():
        upload = secure_filename(form.upload.data.filename)
        name, extension = os.path.splitext(upload)
        filename_hash = hashlib.sha1(str(time.time()))
        filename = str(filename_hash.hexdigest()) + str(extension)
        form.upload.data.save(os.path.join(app.config['BASEDIR'], 'static', 'reviews',
                                           filename))

        review_title = "%s - Artist Review" % (form.artist.data,)
        url_base = "%s Artist Review" % (form.artist.data)
                             pub_date=datetime.datetime.utcnow(),
        review_url = url_base.replace(" ", "-").lower()

        review = ArtistReview(artist=form.artist.data, album=form.album.data,
                             photo=filename, content=form.content.data,
                             author=g.user, page_title=review_title,
                             url=review_url, name=form.name.data)
        db.session.add(review)
        db.session.commit()
        flash('The artist review was created and published.')
        return redirect(url_for('reviews'))

    return render_template('new-artist-review.html', title='Add New Review',
                           form=form)


@app.route('/artists')
def artists():
    return redirect(url_for('album-reviews'))

@app.route('/photos')
def photos():
    return redirect(url_for('album-reviews'))

@app.route('/videos')
def videos():
    return redirect(url_for('album-reviews'))

@app.route('/admin')
@login_required
def admin():
    return redirect(url_for('home'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('admin'))

    if request.method == 'POST':
        login = LoginValidator(username=request.form.get('email'),
                               password=request.form.get('password'))
        remember_user = False
        if request.form.get('remember'):
            remember_user = True

        if login.is_valid:
            login_user(login.lookup_user, remember=remember_user)
            flash('You have logged in successfully.', 'success')
            #return redirect(url_for('admin'))
            return redirect(url_for('home'))
        else:
            flash('Incorrect email/password', 'danger')

    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    flash("You have logged out.", 'info')
    return redirect(url_for('home'))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user


