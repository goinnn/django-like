# -*- coding: utf-8 -*-
# Copyright (c) 2013 by Pablo Martín <goinnn@gmail.com>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.db.models.sql.constants import QUERY_TERMS
from django.test import TestCase


if isinstance(QUERY_TERMS, set):
    QUERY_TERMS.add('error')
else:
    QUERY_TERMS['error'] = None


class DjangoLikeTestCase(TestCase):

    def test_like(self):
        users_like = User.objects.filter(username__like="u%r%")
        users_regex = User.objects.filter(username__regex="^u.*r.$")
        self.assertEqual(list(users_like), list(users_regex))
        self.assertEqual(users_like.count(), 4)

    def test_ilike(self):
        users_ilike = User.objects.filter(username__ilike="U%R%")
        users_regex1 = User.objects.filter(username__regex="^[Uu].*[Rr].$")
        self.assertEqual(list(users_ilike), list(users_regex1))
        self.assertEqual(users_ilike.count(), 4)

        users_regex2 = User.objects.filter(username__regex="^U.*R.$")
        self.assertNotEqual(list(users_ilike), list(users_regex2))
        self.assertNotEqual(list(users_regex2), 0)
        if 'sqlite3' not in settings.DATABASES['default']['ENGINE']:
            users_like = User.objects.filter(username__like="U%R%")
            self.assertEqual(list(users_like), list(users_regex2))

    def test_lookup_error(self):
        try:
            User.objects.filter(username__error="u%r%")
            raise AssertionError("The before query should have failed")
        except TypeError:
            pass

    def test_benchmark_like(self):
        if not 'django_like' in settings.INSTALLED_APPS:
            return  # Running the tests with Django patched
        call_command('benchmark_like', num_users=10, num_queries=10)

    def test_index_example(self):
        response = self.client.get(reverse('app_index'))
        self.assertEqual(response.status_code, 200)

    def test_total_seconds(self):
        if not 'django_like' in settings.INSTALLED_APPS or not hasattr(datetime.timedelta, 'total_seconds'):
            return  # Running the tests with Django patched or python 2.6
        from django_like.management.commands.benchmark_like import total_seconds, total_seconds_backward_compatible
        tds = [datetime.timedelta(1),
               datetime.timedelta(1000),
               datetime.timedelta(0.1),
               datetime.timedelta(10000000),
               datetime.timedelta(0.000001)]
        for td in tds:
            self.assertEqual(td.total_seconds(), total_seconds(td))
            self.assertEqual(td.total_seconds(), total_seconds_backward_compatible(td))
