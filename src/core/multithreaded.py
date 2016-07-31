#coding: utf8
import os
import multiprocessing
import time
from multiprocessing import Process
import Queue
import traceback
from subprocess import Popen, PIPE

from django.shortcuts import get_object_or_404

from gsi.settings import EXECUTE_FE_COMMAND


class MultiprocessingCards(multiprocessing.Process):
	def __init__(self, queue, flag='cards'):
		multiprocessing.Process.__init__(self)
		self.__queue = queue # Queue of the tasks
		self.kill_received = False # If I'll want stoped variable
		self.flag = flag
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
		param_list = param.split('%')

		if self.flag == 'cards':
			run_id = param_list[0]
			card_id = param_list[1]

			ex_fe_com = Popen(
		        'nohup {0} {1} {2} &'.format(
		            EXECUTE_FE_COMMAND,
		            run_id,
		            card_id
		        ),
		        shell=True,
		    )

		if self.flag == 'file':
			fd = open(param_list[0], 'w+')
			fd.write(param_list[2])

            # fd.write('# Sequence: {0}, card: {1} - Generated {2} \n\n'.\
            #          format(sequence.name, card.card_item, step.start_date))
            # fd.writelines('. ' + RESOLUTION_ENV_SCRIPT + '\n\n')
            # fd.writelines(export_home_var + '\n\n')
            # fd.writelines(LOCAL_VAR_GROUPS + '\n\n')
            # fd.writelines(ENVIROMENT_OVERRIDE + '\n\n')
            # fd.writelines(EXECUTABLE[n])
			os.chmod(param_list[0], 0777)
			os.chmod(param_list[1], 0777)
			fd.close()

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