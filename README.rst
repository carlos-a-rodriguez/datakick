========
datakick
========

.. image:: https://travis-ci.org/carlos-a-rodriguez/datakick.svg?branch=master
    :target: https://travis-ci.org/carlos-a-rodriguez/datakick

datakick is a python wrapper for the `Datakick <https://www.datakick.org>`_
open product database API.

Usage
=====

Installation:
-------------
::

    python setup.py install

or

::

    pip install datakick

Sample Code:
------------
First import the module:

.. code-block:: python

    >>> import datakick

Search for products by barcode: 

.. code-block:: python

    >>> gtin14 = "037000062219"
    >>> product = datakick.find_product(gtin14)
    >>> print("{} - {}".format(product.brand_name, product.name))
    'Crest Pro-Health Clean Mint Toothpaste'

Search for products with a key:

.. code-block:: python

    >>> products = datakick.search("Toothpaste")
    >>> for product in products:
    ...    print("{} - {}".format(product.brand_name, product.name))
    'Crest Pro-Health Clean Mint Toothpaste'
    'Sensodyne Fresh Impact Toothpaste'
    # etc.

Add/modify products in the database:

.. code-block:: python

    >>> gtin14 = "011110491503"
    >>> product = datakick.add_product(
    ... gtin14, brand_name="Big K", name="Diet Cola", size="355mL"
    ... )

    >>> print("{} - {} - {}".format(
    ... product.brand_name, product.name, product.size)
    ... )
    'Big K Diet Cola 355mL'

Add images to products in the database:

.. code-block:: python

    >>> gtin14 = "011110491503"
    >>> img_path = "path/to/your/image/cola.jpg"  # only .jpg or .jpeg allowed!
    >>> img_url = datakick.add_image(gtin14, img_path)

    >>> print(img_url)
    'https://d2b9vdin3yve6y.cloudfront.net/1a888191-e530-4d55-a871-00a0994d75c0.jpg'

List the products (on a page):

.. code-block:: python

    >>> products = datakick.list_products(5)  # each page returns 100 products

    >>> for product in products:
    ...     print(product.gtin14)
    '016000437692'
    '016000439894'
    # etc.

Optional Parameters for Adding/Modifying a product:
---------------------------------------------------

======================  =========    ========== ========================
Optional Parameters     Type         Units      Example
======================  =========    ========== ========================
name                    string       n/a        "Toothpaste"
brand_name              string       n/a        "Colgate"
size                    string       n/a        "20oz"
ingredients             string       n/a        "Milk, Chocolate, Sugar"
serving_size            string       n/a        "2 tbsp."
servings_per_container  string       n/a        "2 cookies"
calories                int          n/a        200
fat_calories            int          n/a        100
fat                     int/float    grams      10
saturated_fat           int/float    grams      10
trans_fat               int/float    grams      0
polyunsaturated_fat     int/float    grams      5
monounsaturated_fat     int/float    grams      5
cholesterol             int          milligrams 20
sodium                  int          milligrams 40
potassium               int          milligrams 60
carbohydrate            int          grams      20
fiber                   int          grams      10
sugars                  int          grams      6
protein                 int          grams      4
author                  string       n/a        "First M. Last"
publisher               string       n/a        "MyPublisher"
pages                   int          n/a        400
alcohol_by_volume       int/float    percent    20
======================  =========    ========== ========================

Exceptions:
-----------

- **datakick.exceptions.ImageTooLarge** - Will be thrown if the image provided to datakick.add_image is too large (>1MB)

- **datakick.exceptions.InvalidImageFormat** - Will be thrown if the image provided to datakick.add_image is of the wrong file format (only .jpg or .jpeg allowed).

- **requests.exceptions.HTTPError** - Will be thrown if the gtin14 provided is invalid or not found in the product database.
