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
    Raises :class:`InvalidImageFormatError` if the image doesn't have one of the
    valid image extensions.

    :param img_path: the path to the image
    :raises InvalidImageFormatError: if the image doesn't have one of
    the valid image extensions.
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
    Raises :class:`ImageTooLargeError` if the image is larger 1MB.

    :param img_path: the path to the image
    :raises ImageTooLargeError: if the image is too large.
    :return: None
    """
    megabyte = 1048576

    if os.path.getsize(img_path) > megabyte:
        raise ImageTooLargeError("Image must be <= 1MB in size.")


def add_image(gtin14, img_path):
    """
    Adds an image to the product on the Datakick database and returns the url to
    that image.

    :param gtin14: barcode (ean/upc)
    :param img_path: path to the image
    :raises requests.HTTPError: if the gtin14 is invalid
    :raises datakick.exceptions.ImageTooLarge: if the image is larger
        than 1MB
    :raises datakick.exceptions.InvalidImageFormat: if the image format is not
        one of the approved formats.
    :return: url :class:`str <str>`
    :rtype: :class:`str <str>`
    """
    _check_image_ext(img_path)
    _check_image_size(img_path)

    url = _ADD_IMAGE_URL.format(gtin14=gtin14)

    files = {"image": open(img_path, "rb")}

    resp = requests.post(url, files=files)
    resp.raise_for_status()

    return resp.json().get("image_url")


def add_product(gtin14, **kwargs):
    """
    Adds or modifies a product on the Datakick database and returns it.

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
    :return: :class:`DatakickProduct <DatakickProduct>` object
    :rtype: datakick.models.DatakickProduct
    """
    url = _ADD_PRODUCT_URL.format(gtin14=gtin14)

    resp = requests.put(url, params=kwargs)
    resp.raise_for_status()

    return DatakickProduct(resp.json())


def find_product(gtin14):
    """
    Finds and returns the product from the Datakick database matching the
    barcode supplied.

    :param gtin14: barcode (ean/upc)
    :raises requests.HTTPError: if the gtin14 is invalid or the product is not
        found in the database
    :return: :class:`DatakickProduct <DatakickProduct>` object
    :rtype: datakick.models.DatakickProduct
    """
    url = _FIND_PRODUCT_URL.format(gtin14=gtin14)

    resp = requests.get(url)
    resp.raise_for_status()

    return DatakickProduct(resp.json())


def list_products(page=1):
    """
    Returns a list of products found on the page specified.

    :param page: page of products to retrieve
    :type page: int
    :return: a :class:`list <list>` of :class:`DatakickProduct<DatakickProduct>`
        objects
    :rtype: :class:`list <list>`
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

    :param key: the query to search for
    :return: a :class:`list <list>` of :class:`DatakickProduct<DatakickProduct>`
        objects
    :rtype: :class:`list <list>`
    """
    url_safe_key = key.replace(" ", "+")

    url = _SEARCH_URL.format(key=url_safe_key)

    resp = requests.get(url)
    resp.raise_for_status()

    return [DatakickProduct(product) for product in resp.json()]
