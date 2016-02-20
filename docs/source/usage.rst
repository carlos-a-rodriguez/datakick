Usage
=====

This section has code samples for each of datakick's functions. Please follow
along using your favorite Python REPL environment.

Import
------

Before using the module, you must first import it.

.. code-block:: python

    >>> import datakick

Adding Images
-------------

With a barcode and an image, lets add the image to the product:

.. code-block:: python

    >>> barcode = "011111396487"
    >>> img_path = "/path/to/your/image.jpg"  # use a real path in your code
    >>> img_url = datakick.add_image(barcode, img_path)

The function will return the url to the new added image.

.. code-block:: python

    >>> img_url
    'https://d2b9vdin3yve6y.cloudfront.net/8833b379-8ab7-4f03-a392-abd6e844c04c.jpg'

Make sure the images are smaller than 1MB in size and are of type jpeg or jpg.
Otherwise, an :exc:`ImageTooLargeError` or :exc:`InvalidImageFormatError` will
be raised, respectively.

Adding/Modifying Products
-------------------------

Now lets add a product to the Datakick service:

.. code-block:: python

    >>> barcode = "012546304337"
    >>> product = datakick.add_product(barcode, brand_name="Trident", name="Spearmint Gum", sugars=0, serving_size="1 stick")

The newly created product is returned as a :class:`DatakickProduct` object. You
can extract all the information you need from it.

.. code-block:: python

    >>> product.gtin14
    '012546304337'
    >>> product.brand_name
    'Trident'
    >>> product.sugars
    0

If the information is missing, None will be returned.

.. code-block:: python

    >>> product.pages
    >>> # Nothing printed

If the product already exists, any attributes specified will be modified.
Otherwise, a new product will be created with the arguments passed.

Optional Arguments for Adding/Modifying Products:
--------------------------------------------------

There are 24 optional keyword arguments to the :func:`add_product` function, all
of which are listed in the table below along with their types and units of
measure. Lastly, there is an example for each argument in the last column.

======================  =========    ========== ========================
Name                    Type         Units      Example
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
trans_fat               int/float    grams      0.5
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

Searching by Barcode
--------------------

Lets lookup a product using its barcode:

.. code-block:: python

    >>> barcode = "072140012939"
    >>> product = datakick.find_product(barcode)

Now that we have the product, we can checkout its attributes:

.. code-block:: python

    >>> product.brand_name
    'Nivea'
    >>> product.name
    'Original Moisture Body Lotion'
    >>> product.size
    '500mL'

We can also see how many images it has and what are the urls to those images:

.. code-block:: python

    >>> len(product.images)
    2
    >>> for url in product.images:
    ...     print(url)
    'https://d2b9vdin3yve6y.cloudfront.net/fd7b4ad8-405a-4844-9a2e-d231ede28a63.jpg'
    'https://d2b9vdin3yve6y.cloudfront.net/c628781e-2081-4dfd-94e0-51a1b2b7f67d.jpg'

Accessing All the Attributes in Dictionary Form
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you prefer working with a dictionary instead of a :class:`DatakickProduct`
object, just use :func:`as_dict`:

.. code-block:: python

    >>> product.as_dict()
    {'name': 'Original Moisture Body Lotion', 'images': ['https://d2b9vdin3yve6y.cloudfront.net/fd7b4ad8-405a-4844-9a2e-d231ede28a63.jpg', 'https://d2b9vdin3yve6y.cloudfront.net/c628781e-2081-4dfd-94e0-51a1b2b7f67d.jpg'], 'brand_name': 'Nivea', 'gtin14': '00072140012939', 'size': '500mL'}

Handling Exceptions
^^^^^^^^^^^^^^^^^^^

If the product is not found, a :class:`requests.exceptions.HTTPError` will be
raised. To avoid any crashes, surround your code in a try/except block.

.. code-block:: python

    >>> from requests.exceptions import HTTPError
    >>> try:
    ...     barcode = "000000000001"
    ...     product = datakick.find_product(barcode)
    ...     # product handling code here
    ... except HTTPError:
    ...     # product not found code here

Searching by Key
----------------

Instead of searching for one specific item, we can search for any item that
matches what we are looking for. Lets search for peanut butter:

.. code-block:: python

    >>> products = datakick.search("Peanut Butter")

Now lets iterate over the products to print their brand and name:

.. code-block:: python

    >>> for product in products:
    ...     print("{}, {}".format(product.brand_name, product.name))
    'Jif Peanut Butter'
    'Kind Peanut Butter and Strawberry'
    'Market Pantry Creamy Peanut Butter'
    # etc.

If no products are found, an empty :class:`list` is returned.

Listing Products
----------------

Finally, lets download products by the page. Each page of products returns 100
items. Lets fetch the 4\ :sup:`th` page:

.. code-block:: python

    >>> page = datakick.list_products(4)
    >>> for product in page:
    ...     print(product.gtin14)
    '00006903'
    '00009102'
    '00014373'
    # etc.

Finding the Last Page
^^^^^^^^^^^^^^^^^^^^^

Unfortunately Datakick doesn't provide any information regarding the last
page thru its API. A page number too large will return an empty list.

While not a part of this package, you can easily write a script to determine the
last page on Datakick using `Beautiful Soup`_. Install the package and try the
following code:

.. code-block:: python

    >>> import math
    >>> import requests
    >>> from bs4 import BeautifulSoup
    >>> resp = requests.get("http://www.datakick.org/items")
    >>> soup = BeautifulSoup(resp.text, "html.parser")
    >>> items, _ = soup.p.getText().split()
    >>> num_items = int(items)
    >>> num_pages = math.ceil(num_items / 100)  # each page is 100 items

Errors and Exceptions
---------------------

Trying to add an image larger than 1MB will raise a :exc:`datakick.exceptions.ImageTooLargeError`.

Trying to add an image with the wrong file format will raise a
:exc:`datakick.exceptions.InvalidImageFormatError`.

If the barcode supplied is invalid or the product doesn't exist in the Datakick
database, a :exc:`requests.exceptions.HTTPError` will be raised.

.. _page: https://www.datakick.org/items
.. _Beautiful Soup: http://www.crummy.com/software/BeautifulSoup/
