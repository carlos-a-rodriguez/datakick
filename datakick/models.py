"""
datakick.model
--------------

This module contains the primary model(s) used to return information from the
Datakick database.

"""

import copy


class DatakickProduct(object):
    """Object which contains all the attributes of a product from the Datakick
    database."""

    def __init__(self, json_response):
        """Creates a :class:`DatakickProduct <DatakickProduct>` object using the
        json response from the request to the Datakick database."""
        self._response = json_response

        # convert images from list of dictionaries to list of urls
        self._response["images"] = [
            dct["url"] for dct in self._response.get("images", [])
        ]

    @property
    def alcohol_by_volume(self):
        """Alcohol by volume as a percent."""
        return self._response.get("alcohol_by_volume")

    def as_dict(self):
        """:class:`dict <dict>` of all the attributes."""
        return copy.deepcopy(self._response)

    @property
    def author(self):
        """Name of the author (of the book)."""
        return self._response.get("author")

    @property
    def brand_name(self):
        """The brand name."""
        return self._response.get("brand_name")

    @property
    def calories(self):
        """Amount of calories."""
        return self._response.get("calories")
    
    @property
    def carbohydrate(self):
        """Amount of carbohydrates."""
        return self._response.get("carbohydrate")
    
    @property
    def cholesterol(self):
        """Amount of cholesterol in milligrams (mg)."""
        return self._response.get("cholesterol")
    
    @property
    def fat(self):
        """Amount of fat in grams (g)."""
        return self._response.get("fat")
    
    @property
    def fat_calories(self):
        """Amount of calories from fat."""
        return self._response.get("fat_calories")
    
    @property
    def fiber(self):
        """Amount of fiber in grams (g)."""
        return self._response.get("fiber")
    
    @property
    def gtin14(self):
        """The barcode (ean/upc)."""
        return self._response.get("gtin14")

    @property
    def images(self):
        """:class:`list <list>` of urls to each image."""
        return self._response.get("images", [])
    
    @property
    def ingredients(self):
        """:class:`str <str>` of ingredients."""
        return self._response.get("ingredients")
    
    @property
    def monounsaturated_fat(self):
        """Amount of monounsaturated fat in grams (g)."""
        return self._response.get("monounsaturated_fat")
    
    @property
    def name(self):
        """Name of the product."""
        return self._response.get("name")

    @property
    def pages(self):
        """Number of pages (in the book)."""
        return self._response.get("pages")
    
    @property
    def polyunsaturated_fat(self):
        """Amount of polyunsaturated fat in grams (g)."""
        return self._response.get("polyunsaturated_fat")
    
    @property
    def potassium(self):
        """Amount of potassium in milligrams (mg)."""
        return self._response.get("potassium")
    
    @property
    def protein(self):
        """Amount of protein in grams (g)."""
        return self._response.get("protein")
    
    @property
    def publisher(self):
        """Name of the (book) publisher."""
        return self._response.get("publisher")
    
    @property
    def saturated_fat(self):
        """Amount of saturated fat in grams (g)."""
        return self._response.get("saturated_fat")
    
    @property
    def serving_size(self):
        """The serving size."""
        return self._response.get("serving_size")
    
    @property
    def servings_per_container(self):
        """The servings per container."""
        return self._response.get("servings_per_container")
    
    @property
    def size(self):
        """The net weight or volume."""
        return self._response.get("size")
    
    @property
    def sodium(self):
        """Amount of sodium in milligrams (mg)."""
        return self._response.get("sodium")
    
    @property
    def sugars(self):
        """Amount of sugar in grams (g)."""
        return self._response.get("sugars")
    
    @property
    def trans_fat(self):
        """Amount of trans fat in grams (g)."""
        return self._response.get("trans_fat")
