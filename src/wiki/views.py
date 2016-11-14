# -*- coding: utf-8 -*-
from datetime import datetime
import os
import shutil
# import getpass
# from datetime import datetime
# import magic
# import copy

from django.utils.decorators import method_decorator
from django.forms import ModelForm
from django.views.generic import UpdateView, DeleteView
from django import forms

from django.utils.translation import ugettext_lazy as _

from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import FormView
from django.contrib.contenttypes.models import ContentType

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Button, Field, ButtonHolder, HTML
from crispy_forms.bootstrap import FormActions
# from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

from wiki.models import Wiki
from wiki.wiki_form import WikiForm


@login_required
@render_to('wiki/wiki_show.html')
def wiki_show(request):
    title = 'Wiki'
    wiki = Wiki.objects.all()

    if request.is_ajax():
        data_post = request.POST

        print 'AJAX ============ ', data_post

        if 'wiki_id' in data_post:
            status = 'succes'

            return HttpResponse(status)

    if request.method == "POST":
        data_post = request.POST

        print 'POST ============ ', data_post



    data = {
        'title': title,
        'wiki': wiki,
    }

    return data


class WikiUpdateForm(ModelForm):
    class Meta:
        model = Wiki
        fields = ('content', 'title')

    def __init__(self, *args, **kwargs):
        super(WikiUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('wiki_edit',
            kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-3 control-label'
        self.helper.field_class = 'col-sm-9'

        self.helper.layout = Layout(
            Field('title'),
            HTML("""<img class="button" src="/static/img/bold.gif" name="btnBold" title="Bold" onClick="doAddTags('<strong>','</strong>','id_content')">"""),
            HTML("""<img class="button" src="/static/img/italic.gif" name="btnItalic" title="Italic" onClick="doAddTags('<em>','</em>','id_content')">"""),
            HTML("""<img class="button" src="/static/img/underline.gif" name="btnUnderline" title="Underline" onClick="doAddTags('<u>','</u>','id_content')">"""),
            HTML("""<img class="button" src="/static/img/link.gif" name="btnLink" title="Insert Link" onClick="doURL('id_content')">"""),
            HTML("""<img class="button" src="/static/img/image.gif" name="btnPicture" title="Insert Picture" onClick="doImage('id_content')">"""),
            HTML("""<img class="button" src="/static/img/ordered.gif" name="btnList" title="Ordered List" onClick="doList('<ol>','</ol>','id_content')">"""),
            HTML("""<img class="button" src="/static/img/unordered.gif" name="btnList" title="Unordered List" onClick="doList('<ul>','</ul>','id_content')">"""),
            HTML("""<img class="button" src="/static/img/quote.gif" name="btnQuote" title="Quote" onClick="doAddTags('<blockquote>','</blockquote>','id_content')">"""),
            HTML("""<img class="button" src="/static/img/code.gif" name="btnCode" title="Code" onClick="doAddTags('<code>','</code>','id_content')">"""),
            Field('content'),
            ButtonHolder(
                Submit('add_button', _(u'Save'), css_class="btn btn-success"),
                Submit('cancel_button', _(u'Cancel'), css_class="btn btn-primary"),
            )
        )


class WikiUpdateView(UpdateView):
    model = Wiki
    template_name = 'wiki/wiki_edit.html'
    form_class = WikiUpdateForm

    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse('wiki_show'),
            _(u"Wiki article updated successfully!"))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                u'%s?status_message=%s' % (reverse('wiki_show'),
                _(u"Wiki article update canceled!")))
        else:
            return super(WikiUpdateView, self).post(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WikiUpdateView, self).dispatch(*args, **kwargs)


@login_required
@render_to('wiki/wiki_edit.html')
def wiki_edit(request, wiki_id):
    title = 'Wiki Edit'
    url_name = 'wiki_edit'
    form = None

    if request.method == "POST":
        data_post = request.POST
        form = WikiForm(data_post)

        print 'POST 1 ============ ', data_post

    data = {'title': title,}

    return data
