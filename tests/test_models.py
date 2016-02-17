"""Unittest for datakick.models module."""

import copy
import six
import unittest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from datakick.models import DatakickProduct


class TestModels(unittest.TestCase):

    def setUp(self):
        self.json_response = {
            "gtin14": "000000000000",
            "brand_name": "MyBrand",
            "name": "MyName",
            "size": "21oz",
            "ingredients": "Chocolate",
            "serving_size": "34g",
            "servings_per_container": 10,
            "calories": 200,
            "fat_calories": 5,
            "fat": 5,
            "saturated_fat": 5,
            "trans_fat": 5,
            "polyunsaturated_fat": 5,
            "monounsaturated_fat": 5,
            "cholesterol": 5,
            "sodium": 5,
            "potassium": 5,
            "carbohydrate": 5,
            "fiber": 5,
            "sugars": 5,
            "protein": 5,
            "author": "AuthName",
            "publisher": "MyPublisher",
            "pages": 5,
            "alcohol_by_volume": 5,
            "images": [
                {"url": "someurl_1"},
                {"url": "someurl_2"},
            ]
        }

        self.product = DatakickProduct(self.json_response)

    def test_alcohol_by_volume(self):
        self.assertEqual(
            self.json_response.get("alcohol_by_volume"),
            self.product.alcohol_by_volume
        )

    def test_as_dict(self):
        self.assertEqual(self.json_response, self.product.as_dict())

    def test_author(self):
        self.assertEqual(
            self.json_response.get("author"), self.product.author
        )

    def test_brand_name(self):
        self.assertEqual(
            self.json_response.get("brand_name"), self.product.brand_name
        )

    def test_calories(self):
        self.assertEqual(
            self.json_response.get("calories"), self.product.calories
        )

    def test_carbohydrate(self):
        self.assertEqual(
            self.json_response.get("carbohydrate"), self.product.carbohydrate
        )

    def test_cholesterol(self):
        self.assertEqual(
            self.json_response.get("cholesterol"), self.product.cholesterol
        )

    def test_fat(self):
        self.assertEqual(
            self.json_response.get("fat"), self.product.fat
        )

    def test_fat_calories(self):
        self.assertEqual(
            self.json_response.get("fat_calories"), self.product.fat_calories
        )

    def test_fiber(self):
        self.assertEqual(
            self.json_response.get("fiber"), self.product.fiber
        )

    def test_gtin14(self):
        # trim leading zeros
        actual = int(self.product.gtin14)
        expected = int(self.json_response.get("gtin14"))

        self.assertEqual(expected, actual)

    def test_images(self):
        expected = ["someurl_1", "someurl_2"]

        self.assertEqual(expected, self.product.images)

    def test_images_empty(self):
        json_response = copy.deepcopy(self.json_response)
        json_response["images"] = []

        product = DatakickProduct(json_response)

        self.assertEqual([], product.images)

    def test_ingredients(self):
        self.assertEqual(
            self.json_response.get("ingredients"), self.product.ingredients
        )

    def test_monounsaturated_fat(self):
        self.assertEqual(
            self.json_response.get("monounsaturated_fat"),
            self.product.monounsaturated_fat
        )

    def test_name(self):
        self.assertEqual(
            self.json_response.get("name"), self.product.name
        )

    def test_pages(self):
        self.assertEqual(
            self.json_response.get("pages"), self.product.pages
        )

    def test_polyunsaturated_fat(self):
        self.assertEqual(
            self.json_response.get("polyunsaturated_fat"),
            self.product.polyunsaturated_fat
        )

    def test_potassium(self):
        self.assertEqual(
            self.json_response.get("potassium"), self.product.potassium
        )

    def test_protein(self):
        self.assertEqual(
            self.json_response.get("protein"), self.product.protein
        )
        
    def test_publisher(self):
        self.assertEqual(
            self.json_response.get("publisher"), self.product.publisher
        )

    def test_saturated_fat(self):  
        self.assertEqual(
            self.json_response.get("saturated_fat"), self.product.saturated_fat
        )

    def test_serving_size(self):
        self.assertEqual(
            self.json_response.get("serving_size"), self.product.serving_size
        )

    def test_servings_per_container(self):
        self.assertEqual(
            self.json_response.get("servings_per_container"),
            self.product.servings_per_container
        )

    def test_size(self):
        self.assertEqual(
            self.json_response.get("size"), self.product.size
        )

    def test_sodium(self):
        self.assertEqual(
            self.json_response.get("sodium"), self.product.sodium
        )
        
    def test_sugars(self):
        self.assertEqual(
            self.json_response.get("sugars"), self.product.sugars
        )
        
    def test_trans_fat(self):
        self.assertEqual(
            self.json_response.get("trans_fat"), self.product.trans_fat
        )
