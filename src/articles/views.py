# -*- coding: utf-8 -*-
from django.utils.decorators import method_decorator
from django.forms import ModelForm
from django.views.generic import UpdateView, DeleteView

from django.utils.translation import ugettext_lazy as _

from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Button, Field, ButtonHolder, HTML

from articles.models import Article


@login_required
@render_to('articles/wiki_show.html')
def wiki_show(request):
    ''' View Wiki Show '''
    title = 'Wiki'
    articles = Article.objects.all()

    data = {
        'title': title,
        'articles': articles,
    }

    return data


class ArticleUpdateForm(ModelForm):
    ''' View ArticleUpdateForm '''
    class Meta:
        model = Article
        fields = ('title', 'content',)

    def __init__(self, *args, **kwargs):
        super(ArticleUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('wiki_edit',
            kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'form_update_wiki'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-1 control-label'
        self.helper.field_class = 'col-sm-11'

        self.helper.layout = Layout(
            Field('title'),
            Field('content'),
            ButtonHolder(
                Submit('add_button', _(u'Save'), css_class="btn btn-success"),
                Submit('cancel_button', _(u'Cancel'), css_class="btn btn-primary"),
            )
        )


class WikiUpdateView(UpdateView):
    ''' View WikiUpdateView '''

    model = Article
    template_name = 'articles/wiki_edit.html'
    form_class = ArticleUpdateForm

    def __init__(self, *args, **kwargs):
        super(WikiUpdateView, self).__init__(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(WikiUpdateView, self).get_form_kwargs()
        return kwargs

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
@render_to('articles/wiki_edit.html')
def wiki_edit(request, wiki_id):
    ''' View wiki_edit '''
    title = 'Wiki Edit'
    url_name = 'wiki_edit'
    form = None

    if request.method == "POST":
        data_post = request.POST
        form = WikiForm(data_post)

    data = {'title': title,}

    return data
