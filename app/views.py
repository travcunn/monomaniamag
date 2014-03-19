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
from config import ALBUM_REVIEWS_PER_PAGE, ARTIST_REVIEWS_PER_PAGE, \
        NEWS_ARTICLES_PER_PAGE, REVIEWS_PER_PAGE,TRACK_REVIEWS_PER_PAGE, \
        VIDEOS_PER_PAGE
from forms import AlbumReviewForm, AlbumReviewFormDelete, \
        AlbumReviewFormEdit, ArtistReviewForm, ArtistReviewFormDelete, \
        ArtistReviewFormEdit, LoginValidator, NewsForm, \
        NewsFormDelete, NewsFormEdit, TrackReviewForm, \
        TrackReviewFormDelete, TrackReviewFormEdit, VideoForm, VideoFormDelete
from models import AlbumReview, Article, ArtistReview, TrackReview, User, \
        Video


login_manager.login_view = 'login'

@app.route('/')
def home():

    first_featured = Article.query.options(defer('content'))
    filtered_first = first_featured.filter_by(featured=True)
    one_featured = filtered_first.order_by(Article.pub_date.desc()).first()

    featured_articles = Article.query.options(defer('content'))
    filtered_featured = featured_articles.filter_by(featured=True)
    ordered_featured_articles = \
            filtered_featured.order_by(Article.pub_date.desc())
    featured_news = ordered_featured_articles.slice(1, 3).all()

    news_articles = Article.query.options(defer('content'))
    ordered_articles = news_articles.order_by(Article.pub_date.desc())
    filtered_articles = ordered_articles.filter_by(featured=False)
    panel_news = filtered_articles.paginate(0, 4, False)

    # Album reviews query
    album_reviews = AlbumReview.query.options(defer('content'))
    ordered_album_reviews = \
            album_reviews.order_by(AlbumReview.pub_date.desc())
    panel_album_reviews = ordered_album_reviews.paginate(0, 4, False)

    # Track reviews query
    track_reviews = TrackReview.query.options(defer('content'))
    ordered_track_reviews = \
            track_reviews.order_by(TrackReview.pub_date.desc())
    panel_track_reviews = ordered_track_reviews.paginate(0, 4, False)

    # Artist reviews query
    artist_reviews = ArtistReview.query.options(defer('content'))
    ordered_artist_reviews = \
            artist_reviews.order_by(ArtistReview.pub_date.desc())
    panel_artist_reviews = ordered_artist_reviews.paginate(0, 4, False)

    videos = Video.query.options(defer('content'))
    ordered_videos = videos.order_by(Video.pub_date.desc())
    shown_videos1 = ordered_videos.paginate(1, 3, False)
    shown_videos2 = ordered_videos.paginate(2, 3, False)

    return render_template('home.html',
                           panel_album_reviews=panel_album_reviews,
                           panel_track_reviews=panel_track_reviews,
                           panel_artist_reviews=panel_artist_reviews,
                           one_featured=one_featured,
                           featured_news=featured_news,
                           news=panel_news, videos1=shown_videos1,
                           videos2=shown_videos2)

@app.route('/news')
@app.route('/news/page/<int:page>', methods = ['GET'])
def news(page=1):
    album_reviews = Article.query.options(defer('content'))

    ordered_reviews = album_reviews.order_by(Article.pub_date.desc())
    panel_album_reviews = ordered_reviews.paginate(page,
                                                   NEWS_ARTICLES_PER_PAGE,
                                                   False)

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

        review = Article(page_title=form.title.data,
                         preview=form.preview.data,
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
    article = Article.query.filter_by(url=article_url).first()
    if article is None:
        abort(404)

    side_articles = Article.query.options(defer('content'))
    sorted_side_articles = side_articles.order_by(Article.pub_date.desc())
    shown_side_articles = sorted_side_articles.paginate(0, 6, False)

    delete_form = NewsFormDelete()

    return render_template('news-article.html', title=article.page_title,
                           article=article, side_articles=shown_side_articles,
                           delete_form=delete_form)


@app.route('/news/<article_url>/<action>', methods=['GET', 'POST'])
def article_action(article_url, action):
    article = Article.query.filter_by(url=article_url).first()
    if article is None:
        abort(404)

    if action == "edit":
        form = NewsFormEdit()
        if request.method == 'POST':
            if form.validate_on_submit():
                article.preview = form.preview.data
                article.featured = form.featured.data
                article.content = form.content.data

                article.url = form.title.data.replace(" ", "-").lower()
                article.page_title = form.title.data

                db.session.commit()

                flash('Saved successfully.', 'success')
                return redirect(url_for('single_news_article',
                                        article_url=article.url))

        return render_template('edit-news-article.html', title="Edit Article",
                               article=article, form=form)

    elif action == "delete":
        form = NewsFormDelete()
        if request.method == 'POST':
            if form.validate_on_submit():
                # delete the article image
                img_path = os.path.join(app.config['BASEDIR'],
                                        'static/news/',
                                        article.photo)
                try:
                    os.remove(img_path)
                except OSError:
                    # the file is already deleted
                    pass

                db.session.delete(article)
                db.session.commit()

                flash('Deleted successfully.', 'success')
                return redirect(url_for('news'))
            else:
                return redirect(url_for('single_news_article',
                                        article_url=article.url))
        else:
            abort(404)

@app.route('/videos')
def videos():
    videos_first = Video.query.options(defer('content')).filter_by(category=1)
    ordered_videos = videos_first.order_by(Video.pub_date.desc())
    videos1 = ordered_videos.paginate(1, 4, False)
    videos2 = ordered_videos.paginate(2, 4, False)
    videos3 = ordered_videos.paginate(3, 4, False)

    videos_second = Video.query.options(defer('content')) \
            .filter_by(category=2)
    ordered_videos = videos_second.order_by(Video.pub_date.desc())
    videos4 = ordered_videos.paginate(1, 4, False)
    videos5 = ordered_videos.paginate(2, 4, False)
    videos6 = ordered_videos.paginate(3, 4, False)

    videos_third = Video.query.options(defer('content')).filter_by(category=3)
    ordered_videos = videos_third.order_by(Video.pub_date.desc())
    videos7 = ordered_videos.paginate(1, 4, False)
    videos8 = ordered_videos.paginate(2, 4, False)
    videos9 = ordered_videos.paginate(3, 4, False)

    return render_template('videos.html', videos1=videos1,
                           videos2=videos2, videos3=videos3, videos4=videos4,
                           videos5=videos5, videos6=videos6, videos7=videos7,
                           videos8=videos8, videos9=videos9)

@app.route('/videos/<video_url>')
def single_video(video_url):
    video = Video.query.filter_by(url=video_url).first()
    if video is None:
        abort(404)

    delete_form = VideoFormDelete()

    return render_template('video.html', title=video.title,
                           video=video, delete_form=delete_form)

@app.route('/videos/new', methods=['GET', 'POST'])
@login_required
def add_video():
    form = VideoForm()
    if form.validate_on_submit():
        video_url = form.title.data.replace(" ", "-").lower()

        video = Video(title=form.title.data,
                      category=form.category.data,
                      youtube_id=form.youtube_id.data,
                      content=form.content.data,
                      pub_date=datetime.datetime.utcnow(),
                      url=video_url, author=g.user)
        db.session.add(video)
        db.session.commit()
        flash('The video was published.')
        return redirect(url_for('videos'))

    return render_template('new-video.html', title='Add Video',
                           form=form)

@app.route('/videos/<video_url>/<action>', methods=['GET', 'POST'])
def video_action(video_url, action):
    review = AlbumReview.query.filter_by(url=video_url).first()
    if review is None:
        abort(404)

    if action == "edit":
        form = AlbumReviewFormEdit()
        if request.method == 'POST':
            if form.validate_on_submit():
                review.artist = form.artist.data
                review.album = form.album.data
                review.content = form.content.data

                review_title = "%s - %s - Album Review" % (form.artist.data,
                                                         form.album.data)
                url_base = "%s %s Album Review" % (form.artist.data,
                                                   form.album.data)
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
                try:
                    os.remove(img_path)
                except OSError:
                    # the file is already deleted
                    pass

                db.session.delete(review)
                db.session.commit()

                flash('Deleted successfully.', 'success')
                return redirect(url_for('album_reviews'))
            else:
                return redirect(url_for('single_album_review',
                                        review_url=review.url))
        else:
            abort(404)

@app.route('/reviews')
def reviews():
    album_reviews = AlbumReview.query.options(defer('content'))
    sorted_album_reviews = album_reviews.order_by(AlbumReview.pub_date.desc())
    shown_album_reviews = sorted_album_reviews.paginate(0,
                                REVIEWS_PER_PAGE,
                                False)

    track_reviews = TrackReview.query.options(defer('content'))
    sorted_track_reviews = track_reviews.order_by(TrackReview.pub_date.desc())
    shown_track_reviews = sorted_track_reviews.paginate(0,
                                REVIEWS_PER_PAGE,
                                False)

    artist_reviews = ArtistReview.query.options(defer('content'))
    sorted_artist_reviews = \
            artist_reviews.order_by(ArtistReview.pub_date.desc())
    shown_artist_reviews = sorted_artist_reviews.paginate(0,
                                REVIEWS_PER_PAGE,
                                False)

    return render_template('reviews.html', title='Reviews',
                           album_reviews=shown_album_reviews,
                           track_reviews=shown_track_reviews,
                           artist_reviews=shown_artist_reviews)

@app.route('/reviews/album')
@app.route('/reviews/album/page/<int:page>', methods = ['GET'])
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
@app.route('/reviews/track/page/<int:page>', methods = ['GET'])
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
@app.route('/reviews/artist/page/<int:page>', methods = ['GET'])
def artist_reviews(page=1):
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
def single_artist_review(review_url):
    review = ArtistReview.query.filter_by(url=review_url).first()
    if review is None:
        abort(404)

    side_reviews = ArtistReview.query.options(defer('content'))
    sorted_side_reviews = side_reviews.order_by(ArtistReview.pub_date.desc())
    shown_side_reviews = sorted_side_reviews.paginate(0, 6, False)

    delete_form = ArtistReviewFormDelete()

    return render_template('artist-review.html', title=review.page_title,
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

                review_title = "%s - %s - Album Review" % (form.artist.data,
                                                         form.album.data)
                url_base = "%s %s Album Review" % (form.artist.data,
                                                   form.album.data)
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
                try:
                    os.remove(img_path)
                except OSError:
                    # the file is already deleted
                    pass

                db.session.delete(review)
                db.session.commit()

                flash('Deleted successfully.', 'success')
                return redirect(url_for('album_reviews'))
            else:
                return redirect(url_for('single_album_review',
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
                review.content = form.content.data

                review_title = "%s - Artist Review" % (form.artist.data,)
                url_base = "%s Artist Review" % (form.artist.data)
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

                try:
                    os.remove(img_path)
                except OSError:
                    # the file is already deleted
                    pass
                db.session.delete(review)
                db.session.commit()

                flash('Deleted successfully.', 'success')
                return redirect(url_for('artist_reviews'))
            else:
                return redirect(url_for('single_artist_review',
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

                review_title = "%s - %s - Track Review" % (form.artist.data,
                                                           form.name.data)
                url_base = "%s %s Track Review" % (form.artist.data,
                                                   form.name.data)
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
                try:
                    os.remove(img_path)
                except OSError:
                    # the file is already deleted
                    pass

                db.session.delete(review)
                db.session.commit()

                flash('Deleted successfully.', 'success')
                return redirect(url_for('track_reviews'))
            else:
                return redirect(url_for('single_track_review',
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
        review_url = url_base.replace(" ", "-").lower()

        review = TrackReview(artist=form.artist.data, album=form.album.data,
                             name=form.name.data, photo=filename,
                             content=form.content.data,
                             pub_date=datetime.datetime.utcnow(),
                             author=g.user, page_title=review_title,
                             url=review_url)
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
        review_url = url_base.replace(" ", "-").lower()

        review = ArtistReview(artist=form.artist.data,
                              photo=filename, content=form.content.data,
                              page_title=review_title,
                              url=review_url,
                              pub_date=datetime.datetime.utcnow(),
                              author=g.user)
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


