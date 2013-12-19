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

from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext


def total_seconds(td):
    # https://github.com/whimboo/mozdownload/commit/f1c524a50265f931c8954d1ea2b10b8fb845ea18
    # Keep backward compatibility with Python 2.6 which doesn't have
    # this method
    if hasattr(td, 'total_seconds'):
        return td.total_seconds()
    else:
        return (float(td.microseconds) +
                (td.seconds + td.days * 24 * 3600) * 10 ** 6) / 10 ** 6


def app_index(request):
    datetime_regex_start = datetime.datetime.now()
    users_regex = list(User.objects.filter(username__regex="^[uU].*[rR].$"))
    time_regex = total_seconds(datetime.datetime.now() - datetime_regex_start) * 1000

    datetime_like_start = datetime.datetime.now()
    users_like = list(User.objects.filter(username__ilike="u%r%"))
    time_like = total_seconds(datetime.datetime.now() - datetime_like_start) * 1000

    improvement = (100 * float(time_regex - time_like) / time_like)
    return render_to_response('test_app/app_index.html',
                              {'users_like': users_like,
                               'users_regex': users_regex,
                               'time_like': time_like,
                               'time_regex': time_regex,
                               'improvement': improvement,
                               },
                              context_instance=RequestContext(request))
