# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from gsi.settings import NUM_PAGINATIONS


# paginations finction
def paginations(request, model_name):
	"""**The method generates a page-pagination.**

    :Arguments:
        * *request*: The request form the server
        * *model_name*: The Model object

    """

	paginator = Paginator(model_name, NUM_PAGINATIONS)
	page = request.GET.get('page')

	try:
		model_name = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		model_name = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver
		# last page of results.
		model_name = paginator.page(paginator.num_pages)

	return model_name
