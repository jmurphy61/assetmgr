import datakick, gc, os
from requests.exceptions import HTTPError
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

BASE = declarative_base()

class Database():
    DEFAULT_URL = "sqlite:///{}".format(os.path.join(
        os.path.split(__file__)[0], "..", "resources", "main.db"))

    def __init__(self, *args, **kwargs):
        self.url = args[0] if len(args) == 1 else Database.DEFAULT_URL
        self.engine = create_engine(self.url, echo=True)
        BASE.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.commit()
        self.session.close()
        del self

    def insert(self, row):
        self.session.merge(row)
    
    def close(self):
        # Dispose of the database object without exception
        self.__exit__(exc_type=None, exc_value=None, traceback=None)

class Item(BASE):
    __tablename__ = "item"

    id = Column('id', Integer, primary_key=True)
    gtin14 = Column('gtin14', String, unique=True, nullable=False)
    location = Column("location", Integer)
    quantity = Column('quantity', Integer, nullable=False)
    minimum_stock = Column("minimum_stock", Integer, nullable=False)

    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        try:
            self.data = datakick.find_product(self.gtin14)
        except HTTPError:
            self.data = datakick.add_product(self.gtin14,
                name=kwargs.get('name'),
                brand_name=kwargs.get('brand_name'),
                size=kwargs.get('size'),
                ingredients=kwargs.get('ingredients'),
                serving_size=kwargs.get('serving_size'),
                servings_per_container=kwargs.get('servings_per_container'),
                calories=kwargs.get('calories'),
                fat_calories=kwargs.get('fat_calories'),
                fat=kwargs.get('fat'),
                saturated_fat=kwargs.get('saturated_fat'),
                trans_fat=kwargs.get('trans_fat'),
                polyunsaturated_fat=kwargs.get('polyunsaturated_fat'),
                monounsaturated_fat=kwargs.get('monounsaturated_fat'),
                cholesterol=kwargs.get('cholesterol'),
                sodium=kwargs.get('sodium'),
                potassium=kwargs.get('potassium'),
                carbohydrate=kwargs.get('carbohydrate'),
                fiber=kwargs.get('fiber'),
                sugars=kwargs.get('sugars'),
                protein=kwargs.get('protein'),
                author=kwargs.get('author'),
                publisher=kwargs.get('publisher'),
                pages=kwargs.get('pages'),
                alcohol_by_volume=kwargs.get('alcohol_by_volume')
            )