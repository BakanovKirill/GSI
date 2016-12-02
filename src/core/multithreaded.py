# -*- coding: utf-8 -*-
import os
import multiprocessing
import time
from datetime import datetime
from multiprocessing import Process
import Queue
import traceback
from subprocess import Popen

from gsi.settings import EXECUTE_FE_COMMAND


class MultiprocessingCards(multiprocessing.Process):
	"""**Class receives a card that you want to run. It creates a queue and starts a multithreaded cards.**"""

	def __init__(self, queue, flag='cards'):
		multiprocessing.Process.__init__(self)
		self.__queue = queue # Queue of the tasks
		self.kill_received = False # If I'll want stoped variable
		self.flag = flag # object type

	def run(self):
		"""**Method run multi-threaded process.**"""
		while not self.kill_received:
			try:
				item = self.__queue.get_nowait() # Wait of data
			except Queue.Empty:
				break

			error = True
			try:
				error = self.multiprocessing_cards(item)
			except:
				traceback.print_exc()

			time.sleep(0.1)
			self.__queue.task_done() # Task ended

			if error:
				self.__queue.put(item) # If the mistake was, then again with that data
		return

	def multiprocessing_cards(self, param):
		"""**The method receives the parameters and starts the implementation process for each type.**"""
		param_list = param.split('%')

		if self.flag == 'cards':
			run_id = param_list[0]
			card_id = param_list[1]

			ex_fe_com = Popen(
				'nohup {0} {1} {2} &'.format(EXECUTE_FE_COMMAND, run_id, card_id),
				shell=True,
			)

		if self.flag == 'file':
			fd = open(param_list[0], 'w+')
			fd.write(param_list[2])
			os.chmod(param_list[0], 0777)
			os.chmod(param_list[1], 0777)
			fd.close()
