from .. import db, login_manager

class Article(db.Model):
    __tablename__ = 'atricles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    body = db.Column(db.Text)
    score = db.Column(db.Float)
    pub_date = db.Column(db.DateTime)
    category = db.Column(db.String(32))
    area = db.Column(db.String(32))
    source = db.Column(db.String(32))
    author = db.Column(db.String(32))
    flag_use = db.Column(db.Boolean, default=False)
    count = db.Column(db.Integer, default=0) # record reading
    tags = db.Column(db.String(32))

    def __init__(self, title, body, score=-1, pub_date=None, category=None, source=None, author=None, area=None, flag_use=None, count=0, tags=None):
        self.title = title
        self.body = body
        self.score = score
        self.pub_date = pub_date
        self.category = category
        self.source = source
        self.author = author
        self.area = area
        self.flag_use = flag_use
        self.count = count
        self.tags = tags

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
                category = fake.word(ext_word_list=['类别1','类别2','类别3']),
                source = fake.word(ext_word_list=['来源1','来源2','来源3']),
                author = fake.word(ext_word_list=['作者1','作者2','作者3']),
                area = fake.word(ext_word_list=['地区1','地区2','地区3']),
                flag_use = choice([True, False]),
                tags = fake.word(ext_word_list=['重要','正向','负向','体育','娱乐','美食','生活','学习','金融','艺术'])
                )
            db.session.add(a)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<Article \'%s\'>' % self.title
