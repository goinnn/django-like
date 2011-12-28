.. contents::

===========
Django Like
===========

Information
===========

Django Like is a Django application that adds other useful fields.

It is distributed under the terms of the GNU Lesser General Public
License <http://www.gnu.org/licenses/lgpl.html>


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

Or apply the next `Patch <http://github.com/goinnn/django-like/blob/master/src/patch/patch.r17282>`_ (This is not neccesary, you can install the app)

Usage
=====

Anything that you can to do with `like <http://en.wikipedia.org/wiki/Where_(SQL)#LIKE>`_ sentence in SQL

::

    MyModel.objects.filter(field_name__like='xx%yy%zz')
    User.objects.filter(username__like='a%in')

It is more quick that something like this, and more readable:

::

    MyModel.objects.filter(field_name__regex='^xx.*yy.*zz$')


Development
===========

You can get the leading edge version of django-like by doing a checkout
of its repository:

  https://github.com/goinnn/django-like
