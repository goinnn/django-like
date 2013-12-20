.. contents::

===========
django-like
===========

Information
===========

django-like is a Django application that adds other useful fields.

It is distributed under the terms of the GNU Lesser General Public
License <http://www.gnu.org/licenses/lgpl.html>


.. image:: https://travis-ci.org/goinnn/django-like.png?branch=master
    :target: https://travis-ci.org/goinnn/django-like

.. image:: https://coveralls.io/repos/goinnn/django-like/badge.png?branch=master
    :target: https://coveralls.io/r/goinnn/django-like

.. image:: https://badge.fury.io/py/django-like.png
    :target: https://badge.fury.io/py/django-like

.. image:: https://pypip.in/d/django-like/badge.png
    :target: https://pypi.python.org/pypi/django-like


Requeriments
============

* `Django <http://pypi.python.org/pypi/django/>`_ (>=1.1). It's possible that works with other versions lower 1.1


Installation
============

In your settings.py
-------------------

::

    INSTALLED_APPS = (

        'django_like',

    )

Or apply some of the next patches (This is not neccesary, you can only install the app):
    * `Django 1.4 <http://github.com/goinnn/django-like/blob/master/patches/patch.r17282>`_
    * `Django 1.5 <https://github.com/goinnn/django-like/blob/master/patches/patch.2847ae>`_
    * `Django 1.6 <https://github.com/goinnn/django-like/blob/master/patches/patch.6691ab>`_

Usage
=====

Something that you can to do with `like <http://en.wikipedia.org/wiki/Where_(SQL)#LIKE>`_ sentence

::

    MyModel.objects.filter(field_name__like='xx%YY%zz')
    MyModel.objects.filter(field_name__ilike='xx%yy%zz')
    User.objects.filter(username__like='a%in')

It is more quick and more readable that something like this:

::

    MyModel.objects.filter(field_name__regex='^xx.*YY.*zz$')

This app provider two new `lookups <http://docs.djangoproject.com/en/dev/topics/db/queries/#field-lookups>`_: like and ilike.

Now you can compare the time it takes to run the same query, many times, with like and with regex

::

    python manage.py benchmark_like


These are a results executing the `benchmark_like <https://github.com/goinnn/django-like/blob/master/django_like/management/commands/benchmark_like.py>`_ in my machine:

========================== =============== ================= ================= ==============
Type & result \\ Database  postgres        mysql             sqllite           oracle
========================== =============== ================= ================= ==============
like                       0:00:50.727005  0:00:14.025656    0:01:36.089407    ?:??:??.??????
regex                      0:01:38.410019  0:02:57.255685    0:09:39.527765    ?:??:??.??????
Improvement                254%            600%              503%              ???%          
========================== =============== ================= ================= ==============

Reported
========

 * `Stack overflow <http://stackoverflow.com/questions/8644146/django-query-how-to-write-where-field-like-10-8-0>`_
 * `Ticket in Django <https://code.djangoproject.com/ticket/17473>`_
 * `Pull request <https://github.com/django/django-old/pull/99>`_
 * `Post in a blog <http://www.yaco.es/blog/en/contribuciones/2012/02/a-simple-and-impossible-query-in-django/>`_

Development
===========

You can get the bleeding edge version of django-like by doing a clone
of its repository

::

  git clone git://github.com/goinnn/django-like.git


Example project
===============

In the source tree, you will find a directory called  `example <https://github.com/goinnn/django-like/tree/master/example/>`_. It contains
a readily setup project that uses django-like. You can run it as usual:

::

    python manage.py syncdb --noinput
    python manage.py runserver
