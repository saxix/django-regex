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
        regex = RegexField(flags=re.I)


    o = DemoModel.objects.create(regex='^1$')
    o.regex.match('1')

RegexFlagsField
~~~~~~~~~~~~~~~

As RegexField but allows to set compilation flags (see: https://docs.python.org/2/howto/regex.html#compilation-flags)
It is rendered with proper widget

.. code-block:: python

    from django_regex.validators import compress
    import re

    class DemoModel(models.Model):
        regex = RegexFlagsField()

    o = DemoModel.objects.create(regex=compress(['aa', re.I]))
    o.regex.match('AA')

    o = DemoModel.objects.create(regex=compress(['aa', 'i'])) # use human shortcuts
    o.regex.match('AA')


RegexFlagsField stores pattern and flags in the same db column as string in the format
`<regex.pattern><separator><regex.flags>`

separator is `chr(0)` can be customized using settings `DJANGO_REGEX_SEPARATOR`
or per each field using `flags_separator` argument.

.. code-block:: python

    from django_regex.validators import compress
    import re

    class DemoModel(models.Model):
        regex = RegexFlagsField(flags_separator='/')

    o = DemoModel.objects.create(regex='aa/i')
    o.regex.match('AA')


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



