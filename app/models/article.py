from .. import db, login_manager

class Article(db.Model):
    __tablename__ = 'atricles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    category = db.Column(db.String(32))
    source = db.Column(db.String(32))
    flag_use = db.Column(db.Boolean, default=False)

    def __init__(self, title, body, pub_date=None, category=None, source=None, flag_use=None):
        self.title = title
        self.body = body
        self.pub_date = pub_date
        self.category = category
        self.source = source
        self.flag_use = flag_use

    @staticmethod
    def generate_fake(count=100, **kwargs):
        """Generate a number of fake users for testing."""
        from sqlalchemy.exc import IntegrityError
        from random import seed,choice
        from faker import Faker

        fake = Faker(locale='zh_CN')

        seed()
        for i in range(count):
            a = Article(
                title=fake.sentence(nb_words=5, variable_nb_words=True, ext_word_list=None),
                body=fake.text(max_nb_chars=256, ext_word_list=None),
                pub_date=fake.date_time(),
                category = fake.word(ext_word_list=['美','日','台']),
                source = fake.word(ext_word_list=['传真','五官']),
                flag_use = choice([True, False])
                )
            db.session.add(a)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @staticmethod
    def get_unused():
        return Article.query.filter_by(flag_use=False)

    @staticmethod
    def get_used():
        return Article.query.filter_by(flag_use=True)

    def __repr__(self):
        return '<Article \'%s\'>' % self.title
