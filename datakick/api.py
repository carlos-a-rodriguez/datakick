"""
datakick.api
------------

This module contains the methods that power datakick.

"""

import os
import requests
import six

from .exceptions import ImageTooLargeError, InvalidImageFormatError
from .models import DatakickProduct

_ADD_PRODUCT_URL = "https://www.datakick.org/api/items/{gtin14}"
_ADD_IMAGE_URL = "https://www.datakick.org/api/items/{gtin14}/images"
_FIND_PRODUCT_URL = "https://www.datakick.org/api/items/{gtin14}"
_LIST_PRODUCTS_URL = "https://www.datakick.org/api/items?page={page}"
_SEARCH_URL = "https://www.datakick.org/api/items?query={key}"

VALID_IMAGE_EXT = (".jpeg", ".jpg")


def _check_image_ext(img_path):
    """
    Raises an exception if the image has an invalid extension.

    :param img_path: the path to the image
    :raises datakick.exceptions.InvalidImageFormatError: if the image has an
        invalid image format
    :return None
    """
    _, ext = os.path.splitext(img_path)

    if ext not in VALID_IMAGE_EXT:
        raise InvalidImageFormatError(
            "Image must have one of the following extensions: {}".format(
                VALID_IMAGE_EXT
            )
        )


def _check_image_size(img_path):
    """
    Raises an exception if the image is too large.

    :param img_path: the path to the image
    :raises: datakick.exceptions.ImageTooLargeError: if the image is larger
        than 1MB
    :return: None
    """
    megabyte = 1048576

    if os.path.getsize(img_path) > megabyte:
        raise ImageTooLargeError("Image must be <= 1MB in size.")


def add_image(gtin14, img_path):
    """
    Adds an image to the product on the Datakick database.

    :param gtin14: the product's barcode
    :param img_path: the path to the image
    :raises: requests.HTTPError: if the gtin14 is invalid
    :raises: datakick.exceptions.ImageTooLarge: if the image is too large
    :raises: datakick.exceptions.InvalidImageFormat: if the image has an
        invalid extension
    :return: the url to the newly added image
    :rtype: str
    """
    _check_image_ext(img_path)
    _check_image_size(img_path)

    url = _ADD_IMAGE_URL.format(gtin14=gtin14)

    files = {"image": open(img_path, "rb")}

    resp = requests.post(url, files=files)
    resp.raise_for_status()

    return resp.json().get("image_url")


def add_product(gtin14, brand_name=None, name=None, size=None, ingredients=None,
                serving_size=None, servings_per_container=None, calories=None,
                fat_calories=None, fat=None, saturated_fat=None, trans_fat=None,
                polyunsaturated_fat=None, monounsaturated_fat=None,
                cholesterol=None, sodium=None, potassium=None,
                carbohydrate=None, fiber=None, sugars=None, protein=None,
                author=None, publisher=None, pages=None,
                alcohol_by_volume=None):
    """
    Adds a new product to the Datakick database. If the product already
    exists, it adds or modifies the specified parameters.

    :param gtin14: the product's barcode
    :param name: the product's name
    :param brand_name: the product's brand
    :param size: the size of the product (i.e. 20oz or 500g)
    :param ingredients: a string of the ingredients
    :param serving_size: the serving size of the product
    :param servings_per_container: the number of servings per container
    :param calories: the number of calories
    :param fat_calories: the number of calories from fat
    :param fat: the amount of fat in grams (g)
    :param saturated_fat: the amount of saturated fat in grams (g)
    :param trans_fat: the amount of trans fat in grams (g)
    :param polyunsaturated_fat: the amount of polyunsaturated fat in grams (g)
    :param monounsaturated_fat: the amount of monounsaturated fat in grams (g)
    :param cholesterol: the amount of cholesterol in milligrams (mg)
    :param sodium: the amount of sodium in milligrams (mg)
    :param potassium: the amount of potassium in milligrams (mg)
    :param carbohydrate: the amount of carbohydrates in grams (g)
    :param fiber: the amount of fiber in grams (g)
    :param sugars: the amount of sugar in grams (g)
    :param protein: the amount of protein in grams (g)
    :param author: the name of the author of the book
    :param publisher: the name of the publisher of the book
    :param pages: the number of pages in the book
    :param alcohol_by_volume: the percentage of alcohol
    :return: the newly created or modified product with all associated
        attributes
    :rtype: datakick.models.DatakickProduct
    """
    params = {}

    for key, val in six.iteritems(locals()):
        if key not in ("gtin14", "params"):
            if val:
                params[key] = val

    url = _ADD_PRODUCT_URL.format(gtin14=gtin14)

    resp = requests.put(url, params=params)
    resp.raise_for_status()

    return DatakickProduct(resp.json())


def find_product(gtin14):
    """
    Retrieves the product from the Datakick database matching the gtin14
    supplied.

    :param gtin14: the product's barcode
    :raises: requests.HTTPError: if the gtin14 is invalid or the product is not
        found in the database
    :return: the product from the Datakick database
    :rtype: datakick.models.DatakickProduct
    """
    url = _FIND_PRODUCT_URL.format(gtin14=gtin14)

    resp = requests.get(url)
    resp.raise_for_status()

    return DatakickProduct(resp.json())


def list_products(page=1):
    """
    Returns a list of all the products on the specified page. There are 100
    products per page. If a non-positive page is provided, the first page is
    returned by default. A page number that is too large will return an empty
    list.

    :param page: the page of products to retrieve
    :type page: int
    :return: a list of all the products found on that page
    :rtype: list
    """
    if page < 1:
        page = 1
    
    url = _LIST_PRODUCTS_URL.format(page=page)

    resp = requests.get(url)
    resp.raise_for_status()

    return [DatakickProduct(product) for product in resp.json()]


def search(key):
    """
    Returns a list of all products in the Datakick database matching the
    supplied query.

    :param key: the query to search Datakick for
    :return: a list of all products matching the query
    :rtype: list
    """
    url_safe_key = key.replace(" ", "+")

    url = _SEARCH_URL.format(key=url_safe_key)

    resp = requests.get(url)
    resp.raise_for_status()

    return [DatakickProduct(product) for product in resp.json()]
