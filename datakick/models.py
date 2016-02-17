"""
datakick.model
--------------

This module contains the primary model(s) used to return information from the
datakick service.

"""

import copy


class DatakickProduct(object):

    def __init__(self, json_response):
        self._response = json_response

    @property
    def alcohol_by_volume(self):
        return self._response.get("alcohol_by_volume")

    def as_dict(self):
        return copy.deepcopy(self._response)

    @property
    def author(self):
        return self._response.get("author")

    @property
    def brand_name(self):
        return self._response.get("brand_name")

    @property
    def calories(self):
        return self._response.get("calories")
    
    @property
    def carbohydrate(self):
        return self._response.get("carbohydrate")
    
    @property
    def cholesterol(self):
        return self._response.get("cholesterol")
    
    @property
    def fat(self):
        return self._response.get("fat")
    
    @property
    def fat_calories(self):
        return self._response.get("fat_calories")
    
    @property
    def fiber(self):
        return self._response.get("fiber")
    
    @property
    def gtin14(self):
        return self._response.get("gtin14")

    @property
    def images(self):
        images = self._response.get("images")

        if images:
            return [dictionary["url"] for dictionary in images]

        return []
    
    @property
    def ingredients(self):
        return self._response.get("ingredients")
    
    @property
    def monounsaturated_fat(self):
        return self._response.get("monounsaturated_fat")
    
    @property
    def name(self):
        return self._response.get("name")

    @property
    def pages(self):
        return self._response.get("pages")
    
    @property
    def polyunsaturated_fat(self):
        return self._response.get("polyunsaturated_fat")
    
    @property
    def potassium(self):
        return self._response.get("potassium")
    
    @property
    def protein(self):
        return self._response.get("protein")
    
    @property
    def publisher(self):
        return self._response.get("publisher")
    
    @property
    def saturated_fat(self):
        return self._response.get("saturated_fat")
    
    @property
    def serving_size(self):
        return self._response.get("serving_size")
    
    @property
    def servings_per_container(self):
        return self._response.get("servings_per_container")
    
    @property
    def size(self):
        return self._response.get("size")
    
    @property
    def sodium(self):
        return self._response.get("sodium")
    
    @property
    def sugars(self):
        return self._response.get("sugars")
    
    @property
    def trans_fat(self):
        return self._response.get("trans_fat")
