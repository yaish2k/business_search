from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
import pkgutil


class Dal(object):
    def __init__(self):
        self.session = None
        self.engine = None

    def connect(self, username=None, password=None, host=None, db=None):
        self.create_engine(username=username, password=password, host=host, db=db)
        self.create_models()
        self.create_session()

    def create_engine(self, username=None, password=None, host=None, db=None):
        db = db or os.environ['DB_NAME']
        username = username or os.environ['USERNAME']
        password = password or os.environ['PASSWORD']
        host = host or os.environ['HOST']
        self.engine = create_engine('postgresql+psycopg2://{user_name}:{password}@{host}/{db}'.format(
            user_name=username,
            password=password,
            host=host,
            db=db
        ))

    def create_models(self):
        pkg_dir = os.path.dirname(__file__)
        for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
            module = __import__(name=name) if '_model' in name  else ''
            if module:
                class_name = name.replace('_model', '').capitalize()
                class_ref = module.__dict__[class_name]
                getattr(class_ref, 'metadata').create_all(bind=self.engine)

    def create_session(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    @property
    def query(self):
        return self.session.query

    def add(self, entity):
        self.session.add(entity)
        self.session.commit()

    def add_all(self, entities):
        self.session.add_all(entities)
        self.session.commit()
