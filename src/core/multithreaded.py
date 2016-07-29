#coding: utf8
import multiprocessing
import time
from multiprocessing import Process
import Queue
import traceback
from subprocess import Popen, PIPE

from django.shortcuts import get_object_or_404

from gsi.settings import EXECUTE_FE_COMMAND


class MultiprocessingCards(multiprocessing.Process):
	def __init__(self,queue):
		multiprocessing.Process.__init__(self)
		self.__queue = queue # Queue of the tasks
		self.kill_received = False # If I'll want stoped variable
	def run(self):
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
		# print 'RES ========================== ', param

		param_list = param.split('%')
		run_id = param_list[0]
		card_id = param_list[1]

		# print 'run_id ========================== ', run_id
		# print 'card_id ========================== ', card_id

		ex_fe_com = Popen(
	        'nohup {0} {1} {2} &'.format(
	            EXECUTE_FE_COMMAND,
	            run_id,
	            card_id
	        ),
	        shell=True,
	    )

# def run_process_cards(run_id, card_id, num=1):
# 	queue = multiprocessing.JoinableQueue() # создаем очередь заданий
# 	processes = 10
# 	urls = []
# 	# Урлы по которым надо будет перейти в браузере
# 	for n in xrange(30):
# 		urls.append(n)
#
# 	# p = multiprocessing.Pool()
#
# 	# results = p.map(func, urls)
# 	# p.close()
# 	# p.join()
#
#
# 	for url in urls:
# 		queue.put(url) # заносим данные в очередь
#
#
#
# 	for i in xrange(processes):
# 	    t = Serfer(queue) # создаем процесс
# 	    t.start() # стартуем
# 	    time.sleep(0.1)
# 	queue.join() # приостанавливаем дальнейшее выполнение кода, пока очередь не опустошится
# 	print "Done"
# # if __name__ == '__main__':
# main()