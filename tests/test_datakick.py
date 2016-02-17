"""Unittest for datakick.api module."""

import copy
import datakick.api as dk
import six
import sys
import unittest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from datakick.exceptions import ImageTooLargeError, InvalidImageFormatError
from datakick.models import DatakickProduct


class TestDatakick(unittest.TestCase):

    valid_gtin14 = "000000000000"

    valid_add_params = {
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
    }

    valid_add_image_response = {
        "id": 701,
        "image_url": "https://someimgurl.jpg"
    }

    def test__check_image_ext_exception(self):
        bad_img_ext = "/path/to/my/image.png"

        self.assertRaises(
            InvalidImageFormatError, dk._check_image_ext, bad_img_ext
        )

    def test__check_image_ext_pass(self):
        img_path = "/path/to/my/image{}"

        for ext in dk.VALID_IMAGE_EXT:
            self.assertEqual(None, dk._check_image_ext(img_path.format(ext)))

    @mock.patch("os.path.getsize", return_value=2*1024*1024)
    def test__check_image_size_exception(self, getsize):
        self.assertRaises(
            ImageTooLargeError, dk._check_image_size, "image.jpg"
        )

    @mock.patch("os.path.getsize", return_value=1024)
    def test__check_image_size_pass(self, getsize):
        self.assertEqual(None, dk._check_image_size("image.jpg"))

    @mock.patch("requests.post")
    @mock.patch("os.path.getsize", return_value=1024)
    def test_add_image_pass(self, getsize, post_request):
        img = "/path/to/image.jpg"
        url = "https://www.datakick.org/api/items/000000000000/images"

        mock_file = mock.mock_open()

        with mock.patch("six.moves.builtins.open", mock_file):
            dk.add_image(self.valid_gtin14, img)
            mock_file.assert_called_once_with(img, "rb")

        self.assertEqual(
            [mock.call(url, files={"image": mock_file()})],
            post_request.call_args_list
        )

    @mock.patch("requests.post")
    @mock.patch("os.path.getsize", return_value=1024)
    def test_add_image_return_pass(self, getsize, post_request):
        img = "/path/to/image.jpg"
        url = "https://www.datakick.org/api/items/000000000000/images"

        mock_file = mock.mock_open()
        post_request.return_value.json = mock.MagicMock(
            return_value=self.valid_add_image_response
        )

        with mock.patch("six.moves.builtins.open", mock_file):
            response = dk.add_image(self.valid_gtin14, img)
            mock_file.assert_called_once_with(img, "rb")

        self.assertEqual(
            self.valid_add_image_response["image_url"],
            response
        )

    @mock.patch("requests.put")
    def test_add_product_call_pass(self, put_request):
        put_request.return_value.json = mock.MagicMock(return_value=None)

        dk.add_product(self.valid_gtin14, **self.valid_add_params)

        url = "https://www.datakick.org/api/items/000000000000"

        self.assertEqual(
            [mock.call(url, params=self.valid_add_params)],
            put_request.call_args_list
        )

    @mock.patch("requests.put")
    def test_add_product_return_pass(self, put_request):
        product = dk.add_product(self.valid_gtin14, **self.valid_add_params)

        self.assertEqual(DatakickProduct, type(product))

    @mock.patch("requests.get")
    def test_find_product_pass(self, get_request):
        url = "https://www.datakick.org/api/items/000000000000"

        get_request.return_value.json = mock.MagicMock(return_value=None)

        dk.find_product(self.valid_gtin14)

        self.assertEqual(
            [mock.call(url)],
            get_request.call_args_list
        )

    @mock.patch("requests.get")
    def test_find_product_return(self, get_request):
        product = dk.find_product(self.valid_gtin14)

        self.assertEqual(DatakickProduct, type(product))

    @mock.patch("requests.get")
    def test_list_products_negative_page(self, get_request):
        url = "https://www.datakick.org/api/items?page=1"

        products = dk.list_products(-2)

        self.assertEqual(
            [mock.call(url)],
            get_request.call_args_list
        )

    @mock.patch("requests.get")
    def test_list_products_pass(self, get_request):
        url = "https://www.datakick.org/api/items?page=5"

        products = dk.list_products(5)

        self.assertEqual(
            [mock.call(url)],
            get_request.call_args_list
        )

    @mock.patch("requests.get")
    def test_list_products_return(self, get_request):
        get_request.return_value.json = mock.MagicMock(return_value=[])

        products = dk.list_products(1)

        self.assertEqual(list, type(products))

    @mock.patch("requests.get")
    def test_search_pass(self, get_request):
        query = "Peanut Butter"

        url = "https://www.datakick.org/api/items?query=Peanut+Butter"

        products = dk.search(query)

        self.assertEqual(
            [mock.call(url)],
            get_request.call_args_list
        )

    @mock.patch("requests.get")
    def test_search_return(self, get_request):
        query = "Peanut Butter"

        get_request.return_value.json = mock.MagicMock(return_value=[])

        products = dk.search(query)

        self.assertEqual(list, type(products))
