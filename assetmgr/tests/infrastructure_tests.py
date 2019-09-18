import logging, mock, optparse, pdb
from requests.exceptions import HTTPError
from source.infrastructure import Database, Item
from unittest import TestCase, main

class TestDatabase(TestCase):
    def setUp(self):
        logging.debug("Initiating infrastructure.Database TestCase")
        self.db = Database()
    
    def test_constructor(self):
        self.assertIsNotNone(self.db)
        self.assertIsInstance(self.db, Database)

    def tearDown(self):
        self.db.close()
        logging.debug("infrastructure.Database TestCase complete.")

class TestItem(TestCase):
    def setUp(self):
        logging.debug("Initiating infrastructure.Item TestCase")
    
    @mock.patch('source.infrastructure.datakick')
    def test_constructor(self, mock_datakick):
        def find_product_side_effect(*args, **kwargs):
            logging.debug(f"mock method for datakick.find_product called. args: {args} kwargs: {kwargs}")
            if args[0] in (None, '') and kwargs.get('gtin14') is None:
                raise HTTPError(f"400 Client Error: Bad Request for url: https://www.datakick.org/api/items/{args[0]}")
            if args[0] is None and kwargs.get('gtin14') in (None, ''):
                raise HTTPError(f"400 Client Error: Bad Request for url: https://www.datakick.org/api/items/{kwargs.get('gtin14')}")

        def add_product_side_effect(*args, **kwargs):
            logging.debug(f"mock method for datakick.add_product called. args: {args} kwargs: {kwargs}")
            if not args[0] and not kwargs:
                raise HTTPError("404 Client Error: Not Found for url: https://www.datakick.org/api/items/")

        mock_datakick.find_product.side_effect = find_product_side_effect
        with self.assertRaises(HTTPError):
            Item()
        
        mock_datakick.find_product.assert_called_with(None)
    
        gtin14 = '00000000000000'
        item = Item(gtin14=gtin14)
        mock_datakick.find_product.assert_called_with(gtin14)
        self.assertIsInstance(item, Item)
    
    @mock.patch('source.infrastructure.datakick')
    def test_add_new(self, mock_datakick):
        # TODO implement
        pass
        
    
    def tearDown(self):
        logging.debug("infrastructure.Item TestCase complete.")

if __name__ == "__main__":
    main()