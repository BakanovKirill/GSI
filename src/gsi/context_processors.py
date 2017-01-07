# -*- coding: utf-8 -*-
import datetime


def get_current_year(request):
	"""Get the current year"""
	now_date = datetime.date.today()
	cur_year = now_date.year

	return {"CURRENT_YEAR": cur_year}
