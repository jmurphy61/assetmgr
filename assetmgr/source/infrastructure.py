import datakick, logging, os, re
from requests.exceptions import HTTPError
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from typing import Optional

BASE = declarative_base()

class Database():
    # TODO doc
    DEFAULT_URL = "sqlite:///{}".format(os.path.join(
        os.path.split(__file__)[0], "..", "resources", "main.db"))

    def __init__(self, *args, **kwargs):
        logging.debug(f"Call to {self.__class__.__name__}(). args: {args} kwargs: {kwargs}")
        self.url = args[0] if len(args) == 1 else Database.DEFAULT_URL
        self.engine = create_engine(self.url, echo=True)
        BASE.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.session.commit()
        self.session.close()

    def insert(self, row) -> None:
    # TODO doc
        self.session.merge(row)
    
    def close(self) -> None:
    # TODO doc
        self.__exit__(exc_type=None, exc_value=None, traceback=None)

class Item(BASE):
    # TODO doc
    __tablename__ = "item"

    id = Column('id', Integer, primary_key=True)
    gtin14 = Column('gtin14', String, unique=True, nullable=False)
    location = Column("location", Integer)
    quantity = Column('quantity', Integer, nullable=False)
    minimum_stock = Column("minimum_stock", Integer, nullable=False)

    def __init__(self, *args, **kwargs):
        logging.debug(f"Call to {self.__class__.__name__}(). args: {args} kwargs: {kwargs}")
        super(Item, self).__init__(*args, **kwargs)
        self.product_data = kwargs.get("product_data")
        if self.product_data is None:
            logging.debug(f"Attempting to obtain product data from datakick API")
            try:
                self.product_data = datakick.find_product(self.gtin14)
            except HTTPError as e:
                # TODO raise an error more specific to this API, such as LookupError
                # This will initially break tests
                raise
    
    @staticmethod
    def add_new(gtin14 : str = None,
    #TODO test
        name : str = None,
        brand_name : str = None,
        size : Optional[str] = None,
        ingredients : Optional[str] = None,
        serving_size : Optional[str] = None,
        servings_per_container : Optional[str] = None,
        calories : Optional[int] = None,
        fat_calories : Optional[int] = None,
        fat : Optional[float] = None,
        saturated_fat : Optional[float] = None,
        trans_fat : Optional[float] = None,
        polyunsaturated_fat : Optional[float] = None,
        monounsaturated_fat : Optional[float] = None,
        cholesterol : Optional[int] = None,
        sodium : Optional[int] = None,
        potassium : Optional[int] = None,
        carbohydrate : Optional[int] = None,
        fiber : Optional[int] = None,
        sugars : Optional[int] = None,
        protein : Optional[int] = None,
        author : Optional[str] = None,
        publisher : Optional[str] = None,
        pages : Optional[int] = None,
        alcohol_by_volume : Optional[float] = None):
        """
        Adds or modifies a product on the Datakick database
        and returns a new Item based on that product.

        :param gtin14: barcode (ean/upc)
        :param name: name
        :param brand_name: brand name
        :param size: net weight or volume (i.e. 20oz or 500g)
        :param ingredients: string of the ingredients
        :param serving_size: serving size of the product
        :param servings_per_container: number of servings per container
        :param calories: number of calories
        :param fat_calories: number of calories from fat
        :param fat: amount of fat in grams (g)
        :param saturated_fat: amount of saturated fat in grams (g)
        :param trans_fat: amount of trans fat in grams (g)
        :param polyunsaturated_fat: amount of polyunsaturated fat in grams (g)
        :param monounsaturated_fat: amount of monounsaturated fat in grams (g)
        :param cholesterol: amount of cholesterol in milligrams (mg)
        :param sodium: amount of sodium in milligrams (mg)
        :param potassium: amount of potassium in milligrams (mg)
        :param carbohydrate: amount of carbohydrates in grams (g)
        :param fiber: amount of fiber in grams (g)
        :param sugars: amount of sugar in grams (g)
        :param protein: amount of protein in grams (g)
        :param author: name of the author of the book
        :param publisher: name of the publisher of the book
        :param pages: number of pages in the book
        :param alcohol_by_volume: percentage of alcohol
        :return: :class:`Item <Item>` object
        :rtype: assetmgr.source.infrastructure.Item
        """
        if not gtin14:
            raise ValueError("Must supply gtin14")

        if not re.compile(r"\d" * 14).fullmatch(gtin14):
            raise ValueError("gtin14 must be a 14 digit integer passed as a string")

        return Item(
            gtin14,
            location,
            quantity,
            minimum_stock,
            product_data=datakick.add_product(
                gtin14,
                name=name,
                brand_name=brand_name,
                size=size,
                ingredients=ingredients,
                serving_size=serving_size,
                servings_per_container=servings_per_container,
                calories=calories,
                fat_calories=fat_calories,
                fat=fat,
                saturated_fat=saturated_fat,
                trans_fat=trans_fat,
                polyunsaturated_fat=polyunsaturated_fat,
                monounsaturated_fat=monounsaturated_fat,
                cholesterol=cholesterol,
                sodium=sodium,
                potassium=potassium,
                carbohydrate=carbohydrate,
                fiber=fiber,
                sugars=sugars,
                protein=protein,
                author=author,
                publisher=publisher,
                pages=pages,
                alcohol_by_volume=alcohol_by_volume))