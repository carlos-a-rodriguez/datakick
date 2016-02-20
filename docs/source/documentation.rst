.. _api:

API Documentation
=================

.. module :: datakick

This part of the documentation covers all the methods, classes and exceptions
in the datakick package.

Main Interface
--------------

All of datakick's functionality can be accessed by these 5 methods.

.. autofunction:: add_image
.. autofunction:: add_product
.. autofunction:: find_product
.. autofunction:: list_products
.. autofunction:: search

Model(s)
--------

.. autoclass:: datakick.models.DatakickProduct
   :inherited-members:

Exceptions
----------

.. autoexception:: datakick.exceptions.ImageTooLargeError
.. autoexception:: datakick.exceptions.InvalidImageFormatError
