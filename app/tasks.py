from app import scheduler, db
from app.models import Article

from app.model import Model

@scheduler.task('cron', id="train_model", day_of_week=6, hour=0, minute=0, second=0)
def train():
    with db.app.app_context():
        model = Model()
        articles = Article.query.all()
        data = [(a.body, 1 if a.flag_use else 0) for a in articles]

@scheduler.task('interval', id="predict_score", minutes=1)
def predict():
    with db.app.app_context():
        model = Model()
        articles = Article.query.all()
        for a in articles:
            if a.score<0:
                score = model.predict(a)
                a.score = score
        db.session.commit()