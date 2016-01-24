# -*- coding: utf-8 -*-
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django import forms
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator
from django.conf import settings

from gsi.models import RunBase, Resolution

TITLES = {
    'home': ['Home', 'index'],
    'setup_run': ['GSI Run Setup', 'run_setup'],
    'edit_run': ['GSI Edit Run', 'run_update'],
    'new_run': ['GSI New Run', 'new_run'],
}


class RunUpdateForm(forms.ModelForm):
    """ form for editing RunBase """
    def __init__(self, *args, **kwargs):
        super(RunUpdateForm, self).__init__(*args, **kwargs)

    # name = forms.CharField(label=u'Name', attrs={'class': 'form-control'})
    name = forms.CharField(
            label=u'Name',
            widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
            widget=forms.Textarea(attrs={'rows': '5', 'class': 'form-control'}),
            required=False,
            label=u'Description'
    )
    purpose = forms.CharField(
            widget=forms.Textarea(attrs={'rows': '5', 'class': 'form-control'}),
            required=False,
            label=u'Purpose of Run'
    )
    directory_path = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control'}),
            required=False,
            label=u'Directory path',
            help_text=u'Directory path is the name of the directory \
                that result will be stored'
    )
    resolution = forms.ModelChoiceField(
            widget=forms.Select(attrs={"class": 'form-control'}),
            queryset=Resolution.objects.all(),
            label=u'Resolution',
    )

    class Meta:
        model = RunBase
        fields = [
            'name',
            'author',
            'description',
            'purpose',
            'directory_path',
            'resolution',
        ]


@render_to('gsi/blocking.html')
def blocking(request):
    data = {}
    return data


@login_required
@render_to('gsi/index.html')
def index(request):
    title = 'GSI Main Menu'
    data = {'title': title}
    return data


@login_required
@render_to('gsi/run_setup.html')
def run_setup(request):
    title = TITLES['setup_run'][0]
    breadcrumbs = {TITLES['home'][0]: TITLES['home'][1]}
    run_bases = RunBase.objects.all()
    data = {
        'title': title,
        'run_bases': run_bases,
        'breadcrumbs': breadcrumbs
    }

    return data


@login_required
@render_to('gsi/new_run.html')
def new_run(request):
    title = TITLES['new_run'][0]
    breadcrumbs = {TITLES['new_run'][0]: TITLES['new_run'][1]}
    run_bases = RunBase.objects.all()
    data = {
        'title': title,
        'breadcrumbs': breadcrumbs
    }

    return data


@login_required
@render_to('gsi/run_update.html')
def run_update(request, run_id):
    title = '{0}ID {1}'.format(TITLES['edit_run'][0], run_id)
    run_base = get_object_or_404(RunBase, pk=run_id)
    form = None
    breadcrumbs = {
        TITLES['home'][0]: TITLES['home'][1],
        TITLES['setup_run'][0]: TITLES['setup_run'][1]
    }

    if request.method == "POST":
        if request.POST.get('save_button') is not None:
            form = RunUpdateForm(request.POST)

            if form.is_valid():
                run_base.name = form.cleaned_data["name"]
                run_base.description = form.cleaned_data["description"]
                run_base.purpose = form.cleaned_data["purpose"]
                run_base.directory_path = form.cleaned_data["directory_path"]
                run_base.resolution = form.cleaned_data["resolution"]
                run_base.save()

                return HttpResponseRedirect(
                        u'%s?status_message=%s' % (reverse('run_setup'),
                        (u"RunID {0} updated successfully".format(run_id)))
                )
        elif request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(
                    u'%s?status_message=%s' % (reverse('run_setup'),
                    (u"RunID {0} addition canceled".format(run_id)))
            )
    else:
        form = RunUpdateForm(instance=run_base)

    data = {
        'title': title,
        'run_base': run_base,
        'breadcrumbs': breadcrumbs,
        'form': form
    }

    return data
