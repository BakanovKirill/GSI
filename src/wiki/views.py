# -*- coding: utf-8 -*-
from datetime import datetime
import os
import shutil
# import getpass
# from datetime import datetime
# import magic
# import copy

from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import FormView
from django.contrib.contenttypes.models import ContentType


@login_required
@render_to('wiki/wiki.html')
def wiki(request):
    title = 'Wiki'

    data = {'title': title,}

    return data
