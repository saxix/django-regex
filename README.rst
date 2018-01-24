================================
Django Regex
================================

.. image:: https://badge.fury.io/py/django-regex.png
    :target: http://badge.fury.io/py/django-regex

.. image:: https://travis-ci.org/saxix/django-regex.png?branch=master
    :target: https://travis-ci.org/saxix/django-regex

.. image:: https://pypip.in/d/django-regex/badge.png
    :target: https://pypi.python.org/pypi/django-regex


Fields and utilities to work with regular expression in Django

Components
----------

RegexField
~~~~~~~~~~
 Django field to store regular expressions

.. code-block:: python

    class DemoModel(models.Model):
        regex = RegexField()


    o = DemoModel.objects.create(regex='^1$')
    o.regex.match('1')


RegexList
~~~~~~~~~
list that matches content against valid regular expressions

.. code-block:: python

    rules = RegexList(['\d*'])
    1 in rules  # True
    '1' in rules  # True
    'a' in rules  # False



Links
~~~~~

+--------------------+----------------+--------------+----------------------------+
| Stable             | |master-build| | |master-cov| |                            |
+--------------------+----------------+--------------+----------------------------+
| Development        | |dev-build|    | |dev-cov|    |                            |
+--------------------+----------------+--------------+----------------------------+
| Project home page: |https://github.com/saxix/django-regex                       |
+--------------------+------------------------------------------------------------+
| Issue tracker:     |https://github.com/saxix/django-regex/issues?sort           |
+--------------------+------------------------------------------------------------+
| Download:          |http://pypi.python.org/pypi/django-regex/                   |
+--------------------+------------------------------------------------------------+


.. |master-build| image:: https://secure.travis-ci.org/saxix/django-regex.png?branch=master
    :target: http://travis-ci.org/saxix/django-regex/

.. |master-cov| image:: https://codecov.io/gh/saxix/django-regex/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/saxix/django-regex

.. |dev-build| image:: https://secure.travis-ci.org/saxix/django-regex.png?branch=develop
    :target: http://travis-ci.org/saxix/django-regex/

.. |dev-cov| image:: https://codecov.io/gh/saxix/django-regex/branch/develop/graph/badge.svg
    :target: https://codecov.io/gh/saxix/django-regex



