'''

Copyright (C) 2017-2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from django.shortcuts import render
from django.template.context import RequestContext
from django.http import HttpResponseNotFound, HttpResponseServerError


def handler404(request, exception):
    return HttpResponseNotFound(render(request, 'base/404.html'))

def handler500(request):
    return HttpResponseServerError(render(request, 'base/500.html'))
