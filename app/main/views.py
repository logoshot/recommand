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
    not_used = Article.get_unused()
    used = Article.get_used()
    return render_template('main/recommand.html', not_used=not_used, used=used)


@main.route('/articles/<token>', methods=['GET', 'POST'])
def articles(token):
    article = Article.query.filter_by(id=token).first()
    print(request.method)
    if request.method=='POST':
        flag = False if request.form['flag']=='false' else True
        article.flag_use = flag
        db.session.add(article)
        db.session.commit()
    return render_template('main/articles.html', article=article)