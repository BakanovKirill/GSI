# -*- coding: utf-8 -*-
import os
import stat
import time
import shutil
from subprocess import call, Popen
from datetime import datetime
import magic
import multiprocessing

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from gsi.settings import EXECUTE_FE_COMMAND, PROCESS_NUM, STATIC_DIR, FE_SUBMIT, EXEC_RUNS, PATH_RUNS_SCRIPTS
from core.multithreaded import MultiprocessingCards


class UnicodeNameMixin(object):
	"""**Class inheritance for other classes of models.**

    :Functions:
        When inheriting displays the model name

    """

	def __unicode__(self):
		return _(u"%s") % self.name


def validate_status(status):
	"""**The method makes the validation status for the API.**

	:Functions:
		Checks whether there is obtaining the status of the list of possible statuses.

	:Arguments:
		* *status*: Current status

    """

	from gsi.models import STATES

	states = [st[0] for st in STATES]

	if not status or status not in states:
		return {
			'status': False,
			'message': 'Invalid or missing "status" GET parameter.'
		}

	return {'status': status}


def get_copy_name(name):
	"""**The method returns the principal name.**

	:Functions:
		It is used when creating a copy card in the object CardSequence.

	:Arguments:
		* *name*: Card name

    """

	if '*cp' in name:
		return name.split('*cp')[0]
	else:
		return name


def execute_fe_command(params, flag='cards'):
	"""**The method returns the principal name.**

	:Functions:
		It is used when creating a copy card in the object CardSequence.

	:Arguments:
		* *params*: Current options for the execute
		* *flag*: Specifies to which the entity of the process is performed is started

	"""

	queue = multiprocessing.JoinableQueue()  # create queue of the tasks
	num_process = len(params) / 2
	processes = num_process

	for param in params:
		queue.put(param)

	for i in xrange(processes):
		t = MultiprocessingCards(queue, flag)  # Create process
		t.start()
		time.sleep(0.1)
	queue.join()  # suspend the execution of code until the queue is emptied


def slash_remove_from_path(path):
	"""**The method removes superfluous slashes in path.**

	:Functions:
		Checks whether there is in the transmission path of the extra slashes. If found, it replaces them with the standard one.

	:Arguments:
		* *path*: Path (string)

	"""

	result = path
	if '//' in path:
		result = path.replace('//', '/')
	elif '///' in path:
		result = path.replace('///', '/')

	return result


def create_symlink(src, dest, path):
	"""**The method creates a symlink to transmit directory.**

	:Functions:
		Check whether there is already such a symlink. If not, create.

	:Arguments:
		* *src*: Folder which do symlink
		* *dest*: The folder from which make a symlink
		* *path*: The path for check the existence of symbolic link

	"""

	if not os.path.exists(path):
		symlink = call("ln -s {0} {1}".format(dest, src), shell=True)
	else:
		pass


def get_dir_root_static_path():
	"""**Method for get the symbolic link.**"""

	from gsi.models import HomeVariables

	home_var = HomeVariables.objects.all()
	user_dir_root = home_var[0].USER_DATA_DIR_ROOT
	static_dir_root = user_dir_root.split('/')[-1]

	if not static_dir_root:
		static_dir_root = user_dir_root.split('/')[-2:-1]

	static_dir_root_path = STATIC_DIR + '/' + static_dir_root
	static_dir_root_path = slash_remove_from_path(static_dir_root_path)

	return {
		'static_dir_root': static_dir_root,
		'static_dir_root_path': static_dir_root_path,
	}


def convert_size_file(size):
	"""**Method convert a numeric value of the file size in the text designations: B, KB, MB.**"""

	kb = 1024.0
	mb = 1024.0 * 1024.0

	if size < kb:
		size_file = "%.2f B" % (size)

	if size > mb:
		size = size / mb
		size_file = "%.2f MB" % (size)

	if size > kb:
		size = float(size) / kb
		size_file = "%.2f KB" % (size)

	return size_file


def get_type_file(mime_type):
	"""**The method determines the mime-type of file: image, text, pdf, msword, doc, archive.**"""

	if mime_type[0] == 'image':
		type_file = mime_type[0]
	elif mime_type[0] == 'text':
		type_file = mime_type[0]
	elif mime_type[0] == 'application':
		if mime_type[1] == 'pdf':
			type_file = mime_type[1]
		elif mime_type[1] == 'msword':
			type_file = 'doc'
		elif mime_type[1] == 'octet-stream':
			type_file = 'bin'
		else:
			type_file = 'archive'

	return type_file


def get_files_dirs(url_path, full_path):
	"""**The method to get a list of all files and directories from a given path.**"""

	dict_dirs = {}
	all_dirs = {}
	dict_files = {}
	all_files = {}
	info_message = False

	try:
		root, dirs, files = os.walk(full_path).next()

		for d in dirs:
			date_modification = datetime.fromtimestamp(os.path.getmtime(full_path))
			format_date_modification = datetime.strftime(date_modification, "%Y/%m/%d %H:%M:%S")

			dict_dirs['name'] = d
			dict_dirs['date'] = format_date_modification
			all_dirs[d] = dict_dirs
			dict_dirs = {}

		for f in files:
			file_path = os.path.join(url_path, f)
			full_file_path = os.path.join(full_path, f)
			size_file = convert_size_file(os.path.getsize(full_file_path))
			date_modification = datetime.fromtimestamp(os.path.getmtime(full_file_path))
			format_date_modification = datetime.strftime(date_modification, "%Y/%m/%d %H:%M:%S")
			mime_type = magic.from_file(full_file_path, mime=True)
			type_file = get_type_file(mime_type.split('/'))

			dict_files['name'] = f
			dict_files['path'] = file_path
			dict_files['size'] = size_file
			dict_files['date'] = format_date_modification
			dict_files['type'] = type_file

			all_files[f] = dict_files
			dict_files = {}
	except StopIteration, e:
		info_message = True
	except OSError, e:
		info_message = True

	return all_dirs, all_files, info_message


def create_sub_dir(path):
	"""**Method to create directorys: Results, Scores, Trees.**"""
	from gsi.models import HomeVariables

	error_message = ''

	try:
		home_variables = HomeVariables.objects.all()
		path_root = home_variables[0].USER_DATA_DIR_ROOT
		sub_directories = ['Results', 'Scores', 'Trees']
		path_sub_directories = os.path.join(str(path_root), str(path))

		try:
			for d in sub_directories:
				full_path_sub_directories = os.path.join(str(path_sub_directories), str(d))
				os.makedirs(full_path_sub_directories)
		except OSError, e:
			error_message = 'Permission denied: "{0}""'.format(path)
	except Exception, e:
		error_message = 'Error creating a sub-directorys. Please check "Top Level for user data dir" in the Home Variables.'

	return error_message


def create_new_folder(dir):
	"""The method to create a new directory for the model Input Data Directory"""

	from gsi.models import HomeVariables as Home

	try:
		home_var = Home.objects.all()

		if home_var[0].RF_AUXDATA_DIR:
			full_path = os.path.join(home_var[0].RF_AUXDATA_DIR, dir)
		else:
			full_path = '/' + dir
		os.makedirs(full_path)
	except OSError, e:
		print '*** FOLDER EXIST ***: ', e

	return full_path


def get_files(path, file_extension):
	"""**The method to get a list of files from a specified directory and file extension.**

	Returns a list of files and errors in the preparation of a list of files

	:Arguments:
		* *path*: The path to the file
		* *file_extension*: The file extension

	"""

	list_files = []
	error = None
	try:
		root, dirs, files = os.walk(path).next()
		list_files = filter(lambda x: x.endswith(file_extension), files)
	except StopIteration, e:
		error = e
	except OSError, e:
		error = e

	return list_files, error


def update_root_list_files():
	"""**The method updates the list of files to ListTestFiles model.**"""

	from gsi.models import HomeVariables as Home
	from gsi.models import ListTestFiles

	home_var = Home.objects.all()
	root_path = home_var[0].RF_AUXDATA_DIR

	try:
		files, errors = get_files(root_path, '.tif')
		tif_files = filter(lambda x: x.endswith('.tif'), files)
		files_exclude = ListTestFiles.objects.filter(input_data_directory=None).exclude(name__in=tif_files).delete()
		files_include = ListTestFiles.objects.filter(input_data_directory=None).values_list('name')

		for f in tif_files:
			file_path = os.path.join(root_path, f)

			if (f,) not in files_include:
				obj = ListTestFiles.objects.create(name=f, input_data_directory=None)
				obj.size = convert_size_file(os.path.getsize(file_path))
				obj.date_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
				obj.save()
	except StopIteration, e:
		pass
	except OSError, e:
		pass


def update_list_files(obj_dir):
	"""**The method updates the list of files from a specified directory to the model ListTestFiles.**"""

	from gsi.models import HomeVariables as Home
	from gsi.models import ListTestFiles

	update_list_dirs()
	home_var = Home.objects.all()
	root_path = home_var[0].RF_AUXDATA_DIR

	ListTestFiles.objects.filter(input_data_directory=None).delete()

	if obj_dir is not None:
		full_dir_path = os.path.join(obj_dir.full_path)
	else:
		full_dir_path = os.path.join(root_path)

	try:
		root, dirs, files = os.walk(full_dir_path).next()
		tif_files = filter(lambda x: x.endswith('.tif'), files)

		files_exclude = ListTestFiles.objects.filter(input_data_directory=obj_dir).exclude(name__in=tif_files).delete()
		files_include = ListTestFiles.objects.filter(input_data_directory=obj_dir).values_list('name')

		for f in tif_files:
			full_file_path = os.path.join(full_dir_path, f)

			if (f,) not in files_include:
				obj = ListTestFiles.objects.create(name=f, input_data_directory=obj_dir)
				file_path = os.path.join(full_dir_path, f)
				obj.size = convert_size_file(os.path.getsize(file_path))
				obj.date_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
				obj.save()
	except StopIteration, e:
		print 'UPDATE LIST StopIteration =========================== ', e
		pass
	except OSError, e:
		print 'UPDATE LIST OSError =========================== ', e
		pass


def update_list_dirs():
	"""The method updates the list of files and directory for the ListTestFiles and the InputDataDirectory models."""
	from gsi.models import InputDataDirectory, ListTestFiles
	from gsi.models import HomeVariables as Home

	home_var = Home.objects.all()
	root_path = home_var[0].RF_AUXDATA_DIR
	all_dirs = InputDataDirectory.objects.all()

	try:
		for dr in all_dirs:
			dir_path = os.path.join(root_path, dr.name)
			# obj_full_path = dr.full_path

			if dir_path != dr.full_path:
				dr.full_path = dir_path
				dr.save()

			# if not os.path.exists(obj_full_path):
			# 	dr.full_path = dir_path
			# 	dr.save()
				# if not os.path.exists(dir_path):
				# 	dr.delete()
				# else:
				# 	dr.full_path = dir_path
				# 	dr.save()
					# create_new_folder(dr.name)
	except OSError, e:
		print 'update_list_dirs ERROR ========================= ', e
		return


def get_path_folder_run(run):
	"""**The method receives to the logs folder a run.**"""
	from gsi.models import HomeVariables as Home

	home_var = Home.objects.all()
	path = {}

	# # home dir scripts
	# GSI_HOME = settings.SCRIPTS_HOME
	# path_runs_logs = GSI_HOME + 'scripts/runs/R_{0}/LOGS'.format(run.id)

	# path to scripts for runs and runs log
	path['path_runs'] = PATH_RUNS_SCRIPTS + '/R_{0}/'.format(run.id)
	path['path_runs_logs'] = PATH_RUNS_SCRIPTS + '/R_{0}/LOGS'.format(run.id)

	return path


def copy_file(src, dest, card_name):
	"""**The method copies the file specification.**"""

	message_error = None
	err_mess = 'No specification file "PreprocSpec location"'

	try:
		shutil.copy2(src, dest)
	except AttributeError, e:
		message_error = 'For Card "{0}": {1}'.format(card_name, err_mess)
	# eg. src and dest are the same file
	except shutil.Error as e:
		err_mess = str(e).split(']')[1]
		err_mess = err_mess.replace('`', '"')
		message_error = 'For Card "{0}": {1}'.format(card_name, err_mess)
	# eg. source or destination doesn't exist
	except IOError as e:
		message_error = 'For Card "{0}": {1}'.format(card_name, err_mess)

	return message_error


def create_open_master_script(path_runs, card_id, num):
	"""**The method creates a script file and set it permissions 777.**"""
	num_file = 1
	execute_master_script = '{0}_master_{1}'.format(card_id, num)
	master_script_name = 'card_{0}_master_{1}.sh'.format(card_id, num)
	master_script_path = path_runs + master_script_name

	master_script = open(master_script_path, 'w+')
	os.chmod(master_script_path, 0777)

	return master_script, execute_master_script


def make_run(run_base, user):
	"""**The method starts work on card processing script.**"""

	from gsi.models import Run, Log, RunStep, OrderedCardItem, SubCardItem
	from gsi.models import HomeVariables as Home

	now = datetime.now()
	step = RunStep.objects.none()
	scripts = []
	first_script = {}
	path_test_data = ''
	message_error = None

	run = Run.objects.create(run_base=run_base, user=user)
	home_var = Home.objects.all()
	resolution = run.run_base.resolution
	directory_path = run.run_base.directory_path
	all_card = OrderedCardItem.objects.filter(sequence__runbase=run.run_base).order_by('order')

	try:
		# <USER_DATA_DIR_ROOT>/<resolution>
		path_test_data = home_var[0].USER_DATA_DIR_ROOT + '/' + str(resolution) + '/' + str(directory_path) + '/'
		path_test_data = path_test_data.replace('//', '/')

		try:
			os.makedirs(path_test_data, 0777)
		except OSError, e:
			pass
	except Exception, e:
		pass

	for card in all_card:
		step = RunStep.objects.create(parent_run=run, card_item=card)

		#TODO: make scripts for each step
		sequence = step.parent_run.run_base.card_sequence

		# create the scripts for the each cards
		script = create_scripts(run, sequence, card, step)

		if script['error']:
			message_error = script['error']

		# if variable script is empty than remove the Run object
		if not script:
			run.delete()
			step.delete()
			return False
		script['step'] = step
		scripts.append(script)

	# if variable script is not empty than execute first element script variable
	# the other scripts are run in the api
	if scripts:
		first_script = scripts[0]
		params = []

		try:
			if first_script['card'].run_parallel:
				for n in first_script['execute_master_scripts']:
					ex_fe_com = Popen(
							'nohup {0} {1} {2} &'.format(
								EXECUTE_FE_COMMAND,
								first_script['run'].id,
								n
							),
							shell=True,
						)
				first_script['step'].state = 'running'
				first_script['step'].save()
				first_script['run'].state = 'running'
				first_script['run'].save()
			else:
				ex_fe_com = Popen(
					'nohup {0} {1} {2} &'.format(
						EXECUTE_FE_COMMAND,
						first_script['run'].id,
						first_script['card'].id
					),
					shell=True,
				)
				first_script['step'].state = 'running'
				first_script['step'].save()
				first_script['run'].state = 'running'
				first_script['run'].save()
		except Exception, e:
			print 'Exception make_run ==================================== ', e
			pass

		# record in the log model of gsi app path to script
		log_name = '{0}_{1}.log'.format(run.id, first_script['card'].id)
		path_log = first_script['path_runs_logs']
		write_log(log_name, run, path_log)

	return {'run': run, 'step': step, 'error': message_error}


def create_scripts(run, sequence, card, step):
	"""**The method for create a scripts at startup RunBase object for the each cards.**"""

	from gsi.models import HomeVariables as Home
	
	####################### write log file
    log_file = '/home/gsi/LOGS/create_scripts.log'
    log_create_scripts = open(log_file, 'w+')
    #######################

	card_model = None
	message_error = None
	execute_master_scripts = []
	home_var = Home.objects.all()
	export_home_var = ''
	LOCAL_VAR_GROUPS = ''

	# home dir scripts
	GSI_HOME = settings.SCRIPTS_HOME

	# <RESOLUTION_ENV_SCRIPT>
	resolution = run.run_base.resolution
	RESOLUTION_ENV_SCRIPT = GSI_HOME + 'bin/' + str(resolution) + '_config'

	# <HOME_ENV_OVERRIDES>
	for hv in home_var:
		export_home_var += 'export SAT_TIF_DIR=' + hv.SAT_DIF_DIR_ROOT + '\n'
		export_home_var += 'export RF_DIR=' + hv.RF_DIR_ROOT + '\n'
		export_home_var += 'export USER_DATA_DIR=' + hv.USER_DATA_DIR_ROOT + '\n'
		export_home_var += 'export MODIS_DIR=' + hv.MODIS_DIR_ROOT + '\n'
		export_home_var += 'export RF_AUXDATA_DIR=' + hv.RF_AUXDATA_DIR + '\n'
		export_home_var += 'export SAT_DIF_DIR=' + hv.SAT_DIF_DIR_ROOT

	# <LOCAL_ENV_OVERRIDES>
	try:
		local_var_groups = (run.run_base.card_sequence.environment_base.environment_variables).replace('\r\n', '\n')
		local_var_groups = local_var_groups.splitlines()
		LOCAL_VAR_GROUPS = ''

		for line in local_var_groups:
			if line != '':
				ln = line.replace('export ', '')
				LOCAL_VAR_GROUPS += u'export {0}\n'.format(ln)
	except Exception, e:
		LOCAL_VAR_GROUPS = ''

	# <ENVIROMENT OVERRIDE>
	try:
		env_override = (run.run_base.card_sequence.environment_override).replace('\r\n', '\n')
		env_override = env_override.splitlines()
		ENVIROMENT_OVERRIDE = ''

		for line in env_override:
			if line != '':
				ln = line.replace('export ', '')
				ENVIROMENT_OVERRIDE += u'export {0}\n'.format(ln)
	except Exception, e:
		ENVIROMENT_OVERRIDE = ''

	# <EXECUTABLE>
	try:
		card_item = step.card_item.card_item
		card_model = card_item.content_type.model
		run_parallel, EXECUTABLE = get_executable(run, sequence, card, card_item)
	except Exception, e:
		EXECUTABLE = ''
		run_parallel = False

	# path to scripts for runs and runs log
	path_runs = get_path_folder_run(run)['path_runs']
	path_runs_logs = get_path_folder_run(run)['path_runs_logs']

	# path_runs = GSI_HOME + 'scripts/runs/R_{0}/'.format(run.id)
	# path_runs_logs = GSI_HOME + 'scripts/runs/R_{0}/LOGS'.format(run.id)

	# <USER_DATA_DIR_ROOT>/<resolution>
	try:
		os.makedirs(path_runs)
		os.makedirs(path_runs_logs)
	except OSError, e:
		print 'Exception OSError ==================================== ', e
		log_create_scripts.writelines('OSError 1: {0}'.format(e))
		pass
	finally:
		try:
			if card_model == 'preproc' or card_model == 'calcstats':
				card_name = card.card_item.content_object
				cur_card = get_card_model(card_model, card_name)
				from_path_spec_location = cur_card.path_spec_location
				to_path_spec_location = path_runs
				message_error = copy_file(from_path_spec_location, to_path_spec_location, card_name)

			if run_parallel:
				params = []
				num_file = 1
				count = 0
				master_script, execute_master = create_open_master_script(path_runs, card.id, num_file)
				execute_master_scripts.append(execute_master)

				for n in EXECUTABLE:
					file_contents = ''
					script_name = 'card_{0}.sh'.format(n)
					script_path = path_runs + script_name
					card_line = '{0} {1} {2}\n'.format(FE_SUBMIT, run.id, n)
					execute_runs = count % EXEC_RUNS

					if not execute_runs and count:
						num_file += 1
						master_script.close()
						master_script, execute_master = create_open_master_script(path_runs, card.id, num_file)
						execute_master_scripts.append(execute_master)

					master_script.write(card_line)


					file_contents += '# Sequence: {0}, card: {1} - Generated {2}\n\n'.\
										format(sequence.name, card.card_item, step.start_date)
					file_contents += 'umask 000\n\n'
					file_contents += 'cd {0}\n\n'.format(path_runs)
					file_contents += '. ' + RESOLUTION_ENV_SCRIPT + '\n\n'
					file_contents += export_home_var + '\n\n'
					file_contents += LOCAL_VAR_GROUPS + '\n\n'
					file_contents += ENVIROMENT_OVERRIDE + '\n\n'
					file_contents += EXECUTABLE[n]


					fd = open(script_path, 'w+')
					fd.write(file_contents)
					fd.close()
					os.chmod(script_path, 0777)
					os.chmod(path_runs_logs, 0777)
					count += 1

				master_script.close()
			else:
				script_name = 'card_{0}.sh'.format(step.card_item.id)
				script_path = path_runs + script_name
				fd = open(script_path, 'w+')
				fd.write('# Sequence: {0}, card: {1} - Generated {2} \n\n'.\
						 format(sequence.name, card.card_item, step.start_date))
				fd.writelines('umask 000\n\n')
				fd.writelines('cd {0}\n\n'.format(path_runs))
				fd.writelines('. ' + RESOLUTION_ENV_SCRIPT + '\n\n')
				fd.writelines(export_home_var + '\n\n')
				fd.writelines(LOCAL_VAR_GROUPS + '\n\n')
				fd.writelines(ENVIROMENT_OVERRIDE + '\n\n')
				fd.writelines(EXECUTABLE)
				os.chmod(script_path, 0777)
				os.chmod(path_runs_logs, 0777)
				fd.close()
		except OSError, e:
			pass
			log_create_scripts.writelines('OSError 2: {0}'.format(e))
			return False
			
	log_create_scripts.close()

	return {
		'script_path': script_path,
		'path_runs_logs': path_runs_logs,
		'script_name': script_name,
		'run': run,
		'card': card,
		'error': message_error,
		'execute_master_scripts': execute_master_scripts
	}


def write_log(log_name, run, path_log):
	"""**The method writes a Log model GSI app.**"""

	from gsi.models import Log

	log = Log.objects.create(name=log_name)
	log.log_file_path = path_log
	log.log_file = log_name
	log.save()
	run.log = log
	run.save()


def get_years(name):
	"""**The method geting all year from an object YearGroup.**"""

	from gsi.models import YearGroup

	year_group = YearGroup.objects.get(name=name)
	return year_group.years.through.objects.filter(yeargroup=year_group)


def get_area_tiles(name):
	"""**The method geting all tiles from an object Area.**"""

	from gsi.models import Area

	card_area = Area.objects.get(name=name)
	return card_area.tiles.through.objects.filter(area=card_area)


def get_statistical_method(remap_obj):
	"""**The method geting statistical method.**"""

	stat_methods = []

	if remap_obj.conditional_mean:
		stat_methods.append('ConditionalMean')
	if remap_obj.conditional_min:
		stat_methods.append('ConditionalMin')
	if remap_obj.conditional_median:
		stat_methods.append('ConditionalMedian')
	if remap_obj.conditional_max:
		stat_methods.append('ConditionalMax')
	if remap_obj.lower_quartile:
		stat_methods.append('LowerQuartile')
	if remap_obj.upper_quartile:
		stat_methods.append('UpperQuartile')

	return stat_methods


def get_card_model(card_model, card_name):
	"""**The method geting type model for the card.**"""

	from cards.models import (RFScore, RFTrain, QRF,
							  Remap, YearFilter, PreProc,
							  Collate, MergeCSV, RandomForest,
							  CalcStats)
	card = None

	if card_model == 'rfscore':
		card = RFScore.objects.get(name=card_name)
	if card_model == 'rftrain':
		card = RFTrain.objects.get(name=card_name)
	if card_model == 'qrf':
		card = QRF.objects.get(name=card_name)
	if card_model == 'remap':
		card = Remap.objects.get(name=card_name)
	if card_model == 'yearfilter':
		card = YearFilter.objects.get(name=card_name)
	if card_model == 'preproc':
		card = PreProc.objects.get(name=card_name)
	if card_model == 'collate':
		card = Collate.objects.get(name=card_name)
	if card_model == 'randomforest':
		card = RandomForest.objects.get(name=card_name)
	if card_model == 'calcstats':
		card = CalcStats.objects.get(name=card_name)

	return card


def is_run_parallel(card):
	"""**The method checks the type of start-up cards: parallel or in series.**"""

	run_parallel = False

	try:
		run_parallel = card.run_parallel
	except Exception:
		pass

	return run_parallel


def create_sub_card_item(name, run_id, card_id):
	"""**The method creates a new object model SubCardItem.**"""

	from gsi.models import SubCardItem

	try:
		sub_card_item = SubCardItem.objects.create(
				name=name,
				run_id=run_id,
				card_id=card_id
		)
	except Exception, e:
		pass


def get_executable(run, sequence, card, card_item):
	"""**The method gets a value for the variable EXECUTABLE for the each card for the create_scripts method.**"""

	from cards.models import (RFScore, RFTrain, QRF, Remap, YearFilter, PreProc,
							Collate, MergeCSV, RandomForest, CalcStats)
	from gsi.models import Year, Tile, ListTestFiles

	card_model = card_item.content_type.model
	EXECUTABLE = ''
	EXECUTABLE_DICT = {}
	EXEC = ''
	pid = 1
	all_num = 1
	run_parallel = False

	if card_model == 'rfscore':
		#  u'RFscore <Tile> [[MyDir]] [<BiasCorrn>] [<QRFopts>] [<RefTarget>] [<CleanName>]'
		data_card = RFScore.objects.get(name=card.card_item.content_object)
		years = get_years(data_card.year_group.name)
		area_tiles = get_area_tiles(data_card.area)
		all_num = len(years) * len(area_tiles)
		run_parallel = is_run_parallel(data_card)

		for year in years:
			year_card = Year.objects.get(id=year.year_id)

			for tile in area_tiles:
				tile_card = Tile.objects.get(id=tile.tile_id)

				if run_parallel:
					EXEC = '$RF_EXEC_DIR/RFscore {0} {1} {2} {3} {4} {5} -s {6}.{7}.{8}.{9}.{10}\n'.format(
						tile_card,
						run.run_base.directory_path,
						data_card.bias_corrn,
						year_card,
						data_card.number_of_threads,
						data_card.QRFopts,
						run.id,
						sequence.id,
						card.id,
						pid,
						all_num
					)
					script_name = '{0}_{1}'.format(card.id, pid)
					EXECUTABLE_DICT[script_name] = EXEC
					create_sub_card_item(script_name, run.id, card.id)
					pid += 1
				else:
					EXECUTABLE += '$RF_EXEC_DIR/RFscore {0} {1} {2} {3} {4} {5} -s {6}.{7}.{8}.{9}.{10}\n'.format(
						tile_card,
						run.run_base.directory_path,
						data_card.bias_corrn,
						year_card,
						data_card.number_of_threads,
						data_card.QRFopts,
						run.id,
						sequence.id,
						card.id,
						pid,
						all_num
					)
					pid += 1

	if card_model == 'rftrain':
		# u'RFtrain <Tile> [<Ntrees>] [<training>] [<Nvar>] [<Nthread>]'
		data_card = RFTrain.objects.get(name=card.card_item.content_object)

		EXECUTABLE += '$RF_EXEC_DIR/RFtrain {0} {1} {2} {3} {4} -s {5}.{6}.{7}.{8}.{9}\n'.format(
			data_card.value,
			data_card.number_of_trees,
			data_card.training,
			data_card.number_of_variable,
			data_card.number_of_thread,
			run.id,
			sequence.id,
			card.id,
			pid,
			1)
		pid += 1

	if card_model == 'qrf':
		# u'QRF [<QRFinterval>] [<ntrees>] [<nthreads>] [<MyDir>]'
		data_card = QRF.objects.get(name=card.card_item.content_object)

		EXECUTABLE += '$RF_EXEC_DIR/QRF {0} {1} {2} {3} -s {4}.{5}.{6}.{7}.{8}\n'.format(
							data_card.interval,
							data_card.number_of_trees,
							data_card.number_of_threads,
							data_card.directory,
							run.id,
							sequence.id,
							card.id,
							pid,
							1,
						)
		pid += 1

	if card_model == 'remap':
		# Remap <FileSpec> <RoI> <OutRoot>[,<OutSuffix>] [<Scale>[,<Xsize>,<Ysize>]] [<Output>] [<ColourTable>] [<RefStatsFile>] [<RefStatsScale>]
		years = None
		data_card = Remap.objects.get(name=card.card_item.content_object)
		stat_methods = get_statistical_method(data_card)
		run_parallel = is_run_parallel(data_card)
		model_name_suff = ''
		file_spec = data_card.file_spec
		output_root = data_card.output_root
		refstats_scale = data_card.refstats_scale or ''
		all_num = 1

		if data_card.model_name and data_card.output_suffix:
			model_name_suff = str(data_card.model_name) + data_card.output_suffix

		if data_card.model_name and not data_card.output_suffix:
			model_name_suff = str(data_card.model_name)

		if not data_card.model_name and data_card.output_suffix:
			model_name_suff = data_card.output_suffix

		if data_card.year_group is not None:
			years = get_years(data_card.year_group.name)

		if years is not None:
			years_num = len(years) or 1
			methods_num = len(stat_methods) or 1
			all_num = years_num * methods_num

			for year in years:
				year_card = Year.objects.get(id=year.year_id)
				if stat_methods:
					for m in stat_methods:
						if model_name_suff:
							method_file_spec = str(year_card) + '_' + m + '_' + model_name_suff
						else:
							method_file_spec = str(year_card) + '_' + m
						method = str(year_card) + '_' + m
						cur_file_spec = os.path.join(str(file_spec), method_file_spec)
						cur_output_root = os.path.join(str(output_root), method)

						if run_parallel:
							EXEC = '$RF_EXEC_DIR/Remap {0} {1} {2} {3} {4} {5} {6} {7} -s {8}.{9}.{10}.{11}.{12}\n'.format(
								cur_file_spec,
								data_card.roi,
								cur_output_root,
								data_card.scale,
								data_card.output,
								data_card.color_table,
								data_card.refstats_file,
								refstats_scale,
								run.id,
								sequence.id,
								card.id,
								pid,
								all_num,
							)
							script_name = '{0}_{1}'.format(card.id, pid)
							EXECUTABLE_DICT[script_name] = EXEC
							create_sub_card_item(script_name, run.id, card.id)
							pid += 1
						else:
							EXECUTABLE += '$RF_EXEC_DIR/Remap {0} {1} {2} {3} {4} {5} {6} {7} -s {8}.{9}.{10}.{11}.{12}\n'.format(
								cur_file_spec,
								data_card.roi,
								cur_output_root,
								data_card.scale,
								data_card.output,
								data_card.color_table,
								data_card.refstats_file,
								refstats_scale,
								run.id,
								sequence.id,
								card.id,
								pid,
								all_num,
							)
							pid += 1
				else:
					if model_name_suff:
						full_path = str(year_card) + '_' + model_name_suff
						cur_file_spec = os.path.join(str(file_spec), full_path)
					else:
						cur_file_spec = os.path.join(str(file_spec), str(year_card))
					cur_output_root = os.path.join(str(output_root), str(year_card))
					if run_parallel:
						EXEC = '$RF_EXEC_DIR/Remap {0} {1} {2} {3} {4} {5} {6} {7} -s {8}.{9}.{10}.{11}.{12}\n'.format(
							cur_file_spec,
							data_card.roi,
							cur_output_root,
							data_card.scale,
							data_card.output,
							data_card.color_table,
							data_card.refstats_file,
							refstats_scale,
							run.id,
							sequence.id,
							card.id,
							pid,
							all_num,
						)
						script_name = '{0}_{1}'.format(card.id, pid)
						EXECUTABLE_DICT[script_name] = EXEC
						create_sub_card_item(script_name, run.id, card.id)
						pid += 1
					else:
						EXECUTABLE += '$RF_EXEC_DIR/Remap {0} {1} {2} {3} {4} {5} {6} {7} -s {8}.{9}.{10}.{11}.{12}\n'.format(
							cur_file_spec,
							data_card.roi,
							cur_output_root,
							data_card.scale,
							data_card.output,
							data_card.color_table,
							data_card.refstats_file,
							refstats_scale,
							run.id,
							sequence.id,
							card.id,
							pid,
							all_num,
						)
						pid += 1
		else:
			if stat_methods:
				all_num = len(stat_methods)

				for m in stat_methods:
					if model_name_suff:
						full_path = m + '_' + model_name_suff
						cur_file_spec = os.path.join(str(file_spec), full_path)
					else:
						cur_file_spec = os.path.join(str(file_spec), m)
					cur_output_root = os.path.join(str(output_root), m)
					if run_parallel:
						EXEC = '$RF_EXEC_DIR/Remap {0} {1} {2} {3} {4} {5} {6} {7} -s {8}.{9}.{10}.{11}.{12}\n'.format(
							cur_file_spec,
							data_card.roi,
							cur_output_root,
							data_card.scale,
							data_card.output,
							data_card.color_table,
							data_card.refstats_file,
							refstats_scale,
							run.id,
							sequence.id,
							card.id,
							pid,
							all_num,
						)
						script_name = '{0}_{1}'.format(card.id, pid)
						EXECUTABLE_DICT[script_name] = EXEC
						create_sub_card_item(script_name, run.id, card.id)
						pid += 1
					else:
						EXECUTABLE += '$RF_EXEC_DIR/Remap {0} {1} {2} {3} {4} {5} {6} {7} -s {8}.{9}.{10}.{11}.{12}\n'.format(
							cur_file_spec,
							data_card.roi,
							cur_output_root,
							data_card.scale,
							data_card.output,
							data_card.color_table,
							data_card.refstats_file,
							refstats_scale,
							run.id,
							sequence.id,
							card.id,
							pid,
							all_num,
						)
						pid += 1
			else:
				if model_name_suff:
					cur_file_spec = os.path.join(str(file_spec), model_name_suff)
				else:
					cur_file_spec = str(file_spec)
				if run_parallel:
					EXEC = '$RF_EXEC_DIR/Remap {0} {1} {2} {3} {4} {5} {6} {7} -s {8}.{9}.{10}.{11}.{12}\n'.format(
						cur_file_spec,
						data_card.roi,
						data_card.output_root,
						data_card.scale,
						data_card.output,
						data_card.color_table,
						data_card.refstats_file,
						refstats_scale,
						run.id,
						sequence.id,
						card.id,
						pid,
						1,
					)
					script_name = '{0}_{1}'.format(card.id, pid)
					EXECUTABLE_DICT[script_name] = EXEC
					create_sub_card_item(script_name, run.id, card.id)
					pid += 1
				else:
					EXECUTABLE += '$RF_EXEC_DIR/Remap {0} {1} {2} {3} {4} {5} {6} {7} -s {8}.{9}.{10}.{11}.{12}\n'.format(
						cur_file_spec,
						data_card.roi,
						data_card.output_root,
						data_card.scale,
						data_card.output,
						data_card.color_table,
						data_card.refstats_file,
						refstats_scale,
						run.id,
						sequence.id,
						card.id,
						pid,
						1,
					)
					pid += 1

	if card_model == 'yearfilter':
		# u'YearFilter <Tile> <FileType> [<Filter>] [<FiltOut>] [<ExtendStart>] [<InpFourier>] [<OutDir>] [<InpDir>]'
		data_card = YearFilter.objects.get(name=card.card_item.content_object)
		area_tiles = get_area_tiles(data_card.area)
		all_num = len(area_tiles)
		run_parallel = is_run_parallel(data_card)

		for tile in area_tiles:
			tile_card = Tile.objects.get(id=tile.tile_id)

			if run_parallel:
				EXEC = '$RF_EXEC_DIR/YearFilter {0} {1} {2} {3} {4} {5} {6} {7} -s {8}.{9}.{10}.{11}.{12}\n'.format(
					tile_card,
					data_card.filetype,
					data_card.filter,
					data_card.filter_output,
					data_card.extend_start,
					data_card.input_fourier,
					data_card.output_directory,
					data_card.input_directory,
					run.id,
					sequence.id,
					card.id,
					pid,
					all_num,
				)
				script_name = '{0}_{1}'.format(card.id, pid)
				EXECUTABLE_DICT[script_name] = EXEC
				create_sub_card_item(script_name, run.id, card.id)
				pid += 1
			else:
				EXECUTABLE += '$RF_EXEC_DIR/YearFilter {0} {1} {2} {3} {4} {5} {6} {7} -s {8}.{9}.{10}.{11}.{12}\n'.format(
					tile_card,
					data_card.filetype,
					data_card.filter,
					data_card.filter_output,
					data_card.extend_start,
					data_card.input_fourier,
					data_card.output_directory,
					data_card.input_directory,
					run.id,
					sequence.id,
					card.id,
					pid,
					all_num,
				)
				pid += 1

	if card_model == 'preproc':
		# u'PreProc [<Tile>|<file.hdf>] [<Year>] [<Mode>]'
		data_card = PreProc.objects.get(name=card.card_item.content_object)
		years = None
		area_tiles = None

		if data_card.year_group:
			years = get_years(data_card.year_group.name)

		if data_card.area:
			area_tiles = get_area_tiles(data_card.area)
		run_parallel = is_run_parallel(data_card)

		if years:
			len_years = len(years)
		else:
			len_years = 1

		if area_tiles:
			len_area_tiles = len(area_tiles)
		else:
			len_area_tiles = 1

		all_num = len_years * len_area_tiles

		if run_parallel:
			card.run_parallel = True
			card.number_sub_cards = all_num
			card.save()

		if years and area_tiles:
			for year in years:
				year_card = Year.objects.get(id=year.year_id)

				for tile in area_tiles:
					tile_card = Tile.objects.get(id=tile.tile_id)
					if run_parallel:
						EXEC = '$RF_EXEC_DIR/PreProc {0} {1} {2} -s {3}.{4}.{5}.{6}.{7}\n'.format(
							tile_card,
							year_card,
							data_card.mode,
							run.id,
							sequence.id,
							card.id,
							pid,
							all_num,
						)
						script_name = '{0}_{1}'.format(card.id, pid)
						EXECUTABLE_DICT[script_name] = EXEC
						create_sub_card_item(script_name, run.id, card.id)
						pid += 1
					else:
						EXECUTABLE += '$RF_EXEC_DIR/PreProc {0} {1} {2} -s {3}.{4}.{5}.{6}.{7}\n'.format(
							tile_card,
							year_card,
							data_card.mode,
							run.id,
							sequence.id,
							card.id,
							pid,
							all_num,
						)
						pid += 1
		if years and not area_tiles:
			if run_parallel:
				EXEC = '$RF_EXEC_DIR/PreProc {0} {1} -s {2}.{3}.{4}.{5}.{6}\n'.format(
					year_card,
					data_card.mode,
					run.id,
					sequence.id,
					card.id,
					pid,
					all_num,
				)
				script_name = '{0}_{1}'.format(card.id, pid)
				EXECUTABLE_DICT[script_name] = EXEC
				create_sub_card_item(script_name, run.id, card.id)
				pid += 1
			else:
				EXECUTABLE += '$RF_EXEC_DIR/PreProc {0} {1} -s {2}.{3}.{4}.{5}.{6}\n'.format(
					year_card,
					data_card.mode,
					run.id,
					sequence.id,
					card.id,
					pid,
					all_num,
				)
				pid += 1
		elif area_tiles and not years:
			for tile in area_tiles:
				tile_card = Tile.objects.get(id=tile.tile_id)
				if run_parallel:
					EXEC = '$RF_EXEC_DIR/PreProc {0} {1} -s {2}.{3}.{4}.{5}.{6}\n'.format(
						tile_card,
						data_card.mode,
						run.id,
						sequence.id,
						card.id,
						pid,
						all_num,
					)
					script_name = '{0}_{1}'.format(card.id, pid)
					EXECUTABLE_DICT[script_name] = EXEC
					create_sub_card_item(script_name, run.id, card.id)
					pid += 1
				else:
					EXECUTABLE += '$RF_EXEC_DIR/PreProc {0} {1} -s {2}.{3}.{4}.{5}.{6}\n'.format(
						tile_card,
						data_card.mode,
						run.id,
						sequence.id,
						card.id,
						pid,
						all_num,
					)
					pid += 1
		else:
			if run_parallel:
				EXEC = '$RF_EXEC_DIR/PreProc {0} -s {1}.{2}.{3}.{4}.{5}\n'.format(
					data_card.mode,
					run.id,
					sequence.id,
					card.id,
					pid,
					all_num,
				)
				script_name = '{0}_{1}'.format(card.id, pid)
				EXECUTABLE_DICT[script_name] = EXEC
				create_sub_card_item(script_name, run.id, card.id)
			else:
				EXECUTABLE += '$RF_EXEC_DIR/PreProc {0} -s {1}.{2}.{3}.{4}.{5}\n'.format(
					data_card.mode,
					run.id,
					sequence.id,
					card.id,
					pid,
					all_num,
				)

	if card_model == 'collate':
		# u'Collate <Tile> [<Mode>] [<InpFile>] [<OutDirFile>] [<InpScale>]'
		from gsi.models import HomeVariables as Home

		####################### write log file
		log_file = '/home/gsi/LOGS/collate.log'
		f_collate = open(log_file, 'w+')
		#######################

		home_var = Home.objects.all()
		root_path = home_var[0].RF_AUXDATA_DIR
		files = []
		data_card = Collate.objects.get(name=card.card_item.content_object)
		area_tiles = get_area_tiles(data_card.area)
		files_list = Collate.input_files.through.objects.filter(collate=data_card)
		run_parallel = is_run_parallel(data_card)
		all_num = len(area_tiles)

		for f in files_list:
			file_obj = ListTestFiles.objects.get(id=f.listtestfiles_id)
			f_name = file_obj.name.split('.')
			f_subdir = os.path.join(data_card.output_tile_subdir, f_name[0])
			# file_obj_path = os.path.join(data_card.input_data_directory, file_obj.name)

			file_obj_path = str(data_card.input_data_directory) + '/' + str(file_obj.name)
			# temp = [file_obj.name, f_subdir]
			temp = [file_obj_path, f_subdir]
			files.append(temp)

			#######################
			f_collate.writelines('RUN ID == {0}\n\n'.format(run.id))
			f_collate.writelines('file_obj_path == {0}\n\n'.format(file_obj_path))
			f_collate.writelines('data_card.input_scale_factor == {0}\n\n'.format(data_card.input_scale_factor))
			#######################
		if files:
			all_num *= len(files)

		for tile in area_tiles:
			tile_card = Tile.objects.get(id=tile.tile_id)

			if files:
				for f in files:

					# f_collate.writelines('f[0] == {0}\n\n'.format(f[0]))
					# f_collate.writelines('f[1] == {0}\n\n'.format(f[1]))


					if run_parallel:
						EXEC = '$RF_EXEC_DIR/Collate {0} {1} {2} {3} {4} -s {5}.{6}.{7}.{8}.{9}\n'.format(
							tile_card,
							data_card.mode,
							f[0],
							f[1],
							data_card.input_scale_factor,
							run.id,
							sequence.id,
							card.id,
							pid,
							all_num,
						)
						script_name = '{0}_{1}'.format(card.id, pid)
						EXECUTABLE_DICT[script_name] = EXEC
						create_sub_card_item(script_name, run.id, card.id)
						pid += 1
					else:
						EXECUTABLE += '$RF_EXEC_DIR/Collate {0} {1} {2} {3} {4} -s {5}.{6}.{7}.{8}.{9}\n'.format(
							tile_card,
							data_card.mode,
							f[0],
							f[1],
							data_card.input_scale_factor,
							run.id,
							sequence.id,
							card.id,
							pid,
							all_num,
						)
						pid += 1
			else:
				if run_parallel:
					EXEC = '$RF_EXEC_DIR/Collate {0} {1} {2} -s {3}.{4}.{5}.{6}.{7}\n'.format(
						tile_card,
						data_card.mode,
						data_card.input_scale_factor,
						run.id,
						sequence.id,
						card.id,
						pid,
						all_num,
					)
					script_name = '{0}_{1}'.format(card.id, pid)
					EXECUTABLE_DICT[script_name] = EXEC
					create_sub_card_item(script_name, run.id, card.id)
					pid += 1
				else:
					EXECUTABLE += '$RF_EXEC_DIR/Collate {0} {1} {2} -s {3}.{4}.{5}.{6}.{7}\n'.format(
						tile_card,
						data_card.mode,
						data_card.input_scale_factor,
						run.id,
						sequence.id,
						card.id,
						pid,
						all_num,
					)
					pid += 1

		f_collate.close()

	if card_model == 'randomforest':
		# RunRandomForestModels.sh <AoI_Name> <Satellite> <ParamSet> <RunSet>
		data_card = RandomForest.objects.get(name=card.card_item.content_object)

		EXECUTABLE += 'export MODELDIR=/lustre/w23/mattgsi/satdata/RF/Projects/Models\n'
		EXECUTABLE += '''export CSVFILE=/lustre/w23/mattgsi/satdata/RF/Projects/Lane/Data/ref/Model${0}.csv >> $MODELDIR/ParamSet_CSVbands.sh\n'''.format(data_card.model)
		EXECUTABLE += 'export MVRF_TOTAL={0} >> $MODELDIR/ParamSet_CSV"$XSET".sh\n'.format(data_card.mvrf)
		EXECUTABLE += 'RunRandomForestModels.sh {0} {1} {2} {3} -s {4}.{5}.{6}.{7}.{8}\n'.format(
			data_card.aoi_name,
			data_card.satellite,
			data_card.param_set,
			data_card.run_set,
			run.id,
			sequence.id,
			card.id,
			pid,
			1,
		)
		pid += 1

	if card_model == 'calcstats':
		#CalcStats <Tile> [<Year>] [<Period>] [<Filter>] [<FiltOut>] [OutDir]
		data_card = CalcStats.objects.get(name=card.card_item.content_object)
		period = data_card.period
		run_parallel = is_run_parallel(data_card)

		if period == 'doy':
			period = data_card.doy_variable

		try:
			years = get_years(data_card.year_group.name)
		except Exception, e:
			years_num = 1
			years = None

		try:
			areas = get_area_tiles(data_card.area.name)
		except Exception, e:
			areas_num = 1
			areas = None

		if years and areas:
			all_num = len(years) * len(areas)

			for year in years:
				year_card = Year.objects.get(id=year.year_id)

				for area in areas:
					area_card = Tile.objects.get(id=area.tile_id)

					if run_parallel:
						EXEC = '$RF_EXEC_DIR/CalcStats {0} {1} {2} {3} {4} {5} {6} -s {7}.{8}.{9}.{10}.{11}\n'.format(
							area_card,
							year_card,
							period,
							data_card.filter,
							data_card.filter_out,
							data_card.input_fourier,
							data_card.out_dir,
							run.id,
							sequence.id,
							card.id,
							pid,
							all_num
						)
						script_name = '{0}_{1}'.format(card.id, pid)
						EXECUTABLE_DICT[script_name] = EXEC
						create_sub_card_item(script_name, run.id, card.id)
						pid += 1
					else:
						EXECUTABLE += '$RF_EXEC_DIR/CalcStats {0} {1} {2} {3} {4} {5} {6} -s {7}.{8}.{9}.{10}.{11}\n'.format(
							area_card,
							year_card,
							period,
							data_card.filter,
							data_card.filter_out,
							data_card.input_fourier,
							data_card.out_dir,
							run.id,
							sequence.id,
							card.id,
							pid,
							all_num
						)
						pid += 1
		elif years and not areas:
			all_num = len(years)
			for year in years:
				year_card = Year.objects.get(id=year.year_id)
				if run_parallel:
					EXEC = '$RF_EXEC_DIR/CalcStats {0} {1} {2} {3} {4} {5} -s {6}.{7}.{8}.{9}.{10}\n'.format(
						year_card,
						period,
						data_card.filter,
						data_card.filter_out,
						data_card.input_fourier,
						data_card.out_dir,
						run.id,
						sequence.id,
						card.id,
						pid,
						all_num
					)
					script_name = '{0}_{1}'.format(card.id, pid)
					EXECUTABLE_DICT[script_name] = EXEC
					create_sub_card_item(script_name, run.id, card.id)
					pid += 1
				else:
					EXECUTABLE += '$RF_EXEC_DIR/CalcStats {0} {1} {2} {3} {4} {5} -s {6}.{7}.{8}.{9}.{10}\n'.format(
						year_card,
						period,
						data_card.filter,
						data_card.filter_out,
						data_card.input_fourier,
						data_card.out_dir,
						run.id,
						sequence.id,
						card.id,
						pid,
						all_num
					)
					pid += 1
		elif not years and areas:
			all_num = len(areas)
			for area in areas:
				area_card = Tile.objects.get(id=area.tile_id)

				if run_parallel:
					EXEC = '$RF_EXEC_DIR/CalcStats {0} {1} {2} {3} {4} {5} -s {6}.{7}.{8}.{9}.{10}\n'.format(
						area_card,
						period,
						data_card.filter,
						data_card.filter_out,
						data_card.input_fourier,
						data_card.out_dir,
						run.id,
						sequence.id,
						card.id,
						pid,
						all_num
					)
					script_name = '{0}_{1}'.format(card.id, pid)
					EXECUTABLE_DICT[script_name] = EXEC
					create_sub_card_item(script_name, run.id, card.id)
					pid += 1
				else:
					EXECUTABLE += '$RF_EXEC_DIR/CalcStats {0} {1} {2} {3} {4} {5} -s {6}.{7}.{8}.{9}.{10}\n'.format(
						area_card,
						period,
						data_card.filter,
						data_card.filter_out,
						data_card.input_fourier,
						data_card.out_dir,
						run.id,
						sequence.id,
						card.id,
						pid,
						all_num
					)
					pid += 1
		else:
			if run_parallel:
				EXEC = '$RF_EXEC_DIR/CalcStats {0} {1} {2} {3} {4} {5} -s {6}.{7}.{8}.{9}.{10}\n'.format(
					data_card.output_tile_subdir,
					period,
					data_card.filter,
					data_card.filter_out,
					data_card.input_fourier,
					data_card.out_dir,
					run.id,
					sequence.id,
					card.id,
					pid,
					all_num
				)
				script_name = '{0}_{1}'.format(card.id, pid)
				EXECUTABLE_DICT[script_name] = EXEC
				create_sub_card_item(script_name, run.id, card.id)
				pid += 1
			else:
				EXECUTABLE += '$RF_EXEC_DIR/CalcStats {0} {1} {2} {3} {4} {5} -s {6}.{7}.{8}.{9}.{10}\n'.format(
					data_card.output_tile_subdir,
					period,
					data_card.filter,
					data_card.filter_out,
					data_card.input_fourier,
					data_card.out_dir,
					run.id,
					sequence.id,
					card.id,
					pid,
					all_num
				)
				pid += 1

	if run_parallel:
		card.run_parallel = True
		card.number_sub_cards = all_num
	elif not run_parallel:
		card.run_parallel = False
		card.number_sub_cards = 0
	card.save()


	if run_parallel:
		return run_parallel, EXECUTABLE_DICT
	else:
		return run_parallel, EXECUTABLE
