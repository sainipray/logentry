===============
Logentry
===============

.. image:: https://img.shields.io/pypi/v/logentry.svg
    :target: https://pypi.python.org/pypi/logentry

.. image:: https://img.shields.io/pypi/pyversions/logentry.svg
    :target: https://pypi.python.org/pypi/logentry

Overview
========

- Showing users admin history also saved history of deleted users

Documentation
=============

- Installation -
   * Run ::

      pip install logentry

   * Add 'logentry' to your INSTALLED_APPS ::

      'logentry',

   * Execute migrate command ::

      'python manage.py migrate logentry'

   * Now you access admin log history in admin ::

      'http://example.com/admin/logentry/customlogentry/'

License
=======

Djsingleton is an Open Source project licensed under the terms of the `MIT license <https://github.com/sainipray/django-logentry/blob/master/LICENSE>`_
