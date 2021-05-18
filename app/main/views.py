from flask import Blueprint, render_template, request

from app.models import EditableHTML, Article

from app import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'main/about.html', editable_html_obj=editable_html_obj)


@main.route('/recommand', methods=['GET', 'POST'])
def recommand():
    not_used = Article.query.filter_by(flag_use=False).order_by(Article.score.desc())
    used = Article.query.filter_by(flag_use=True).order_by(Article.pub_date)
    return render_template('main/recommand.html', not_used=not_used, used=used)


@main.route('/accepted', methods=['GET', 'POST'])
def accepted():
    not_used = Article.query.filter_by(flag_use=False).order_by(Article.score.desc())
    used = Article.query.filter_by(flag_use=True).order_by(Article.pub_date)
    return render_template('main/accepted.html', not_used=not_used, used=used)


@main.route('/articles/<token>', methods=['GET', 'POST'])
def articles(token):
    article = Article.query.filter_by(id=token).first()
    article.count += 1
    print(request.method)
    if request.method=='POST':
        flag = False if request.form['flag']=='false' else True
        article.flag_use = flag
    db.session.commit()
    return render_template('main/articles.html', article=article)