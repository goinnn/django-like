.. contents::

===========
Django Like
===========

Information
===========

Django Like is a Django application that adds other useful fields.

It is distributed under the terms of the GNU Lesser General Public
License <http://www.gnu.org/licenses/lgpl.html>

.. image:: https://badge.fury.io/py/django-like.png
    :target: https://badge.fury.io/py/django-like

.. image:: https://pypip.in/d/django-like/badge.png
    :target: https://pypi.python.org/pypi/django-like


Requeriments
============

Django 1.1 (or higher). It's possible that works with other versions lower 1.1


Installation
============

In your settings.py
-------------------

::

    INSTALLED_APPS = (

        'django_like',

    )

Or apply some of the next patches (This is not neccesary, you can install the app):
    * `Django 1.4 <http://github.com/goinnn/django-like/blob/master/src/patch/patch.r17282>`_
    * `Django 1.5 <https://github.com/goinnn/django-like/blob/master/src/patch/patch.2847ae>`_

Usage
=====

Anything that you can to do with `like <http://en.wikipedia.org/wiki/Where_(SQL)#LIKE>`_ sentence in SQL

::

    MyModel.objects.filter(field_name__like='xx%YY%zz')
    MyModel.objects.filter(field_name__ilike='xx%yy%zz')
    User.objects.filter(username__like='a%in')

It is more quick that something like this, and more readable:

::

    MyModel.objects.filter(field_name__regex='^xx.*YY.*zz$')

This app provider two new `lookups <http://docs.djangoproject.com/en/dev/topics/db/queries/#field-lookups>`_: like and ilike.

Now you can compare the time it takes to run the same query, many times, with like and with regex

::

    python manage.py benchmark_like


These are a results executing the benchmark_like in my machine:

========================== =============== ================= ================= ==============
Type & result \\ Data base postgres        mysql             sqllite           oracle
========================== =============== ================= ================= ==============
like                       0:00:50.727005  0:00:14.025656    0:01:36.089407    ?:??:??.??????
regex                      0:01:38.410019  0:02:57.255685    0:09:39.527765    ?:??:??.??????
Improvement                254%            600%              503%              ???%          
========================== =============== ================= ================= ==============

Reported
========

 * `Stack overflow <http://stackoverflow.com/questions/8644146/django-query-how-to-write-where-field-like-10-8-0>`_
 * Ticket in `Django <https://code.djangoproject.com/ticket/17473>`_
 * `Pull request <https://github.com/django/django-old/pull/99>`_
 * `Post in a blog <http://www.yaco.es/blog/en/contribuciones/2012/02/a-simple-and-impossible-query-in-django/>`_

Development
===========

You can get the bleeding edge version of django-like by doing a clone
of its repository:

  git clone git://github.com/goinnn/django-like.git
