import os, re, datetime
from pathlib import Path
import pandas as pd
import json

# ===================================================================================================
# ===================================================================================================
class SystemCoex_Log():
	def __init__(self):
		self.SystemCoex_Log_Path = '' 
		self.ignore_list_filePath = ''
		self.All_Errors_excel_output_path = ''
		self.error_keyword_classcification = False
		self.ignore_list = []
		self.SCRIPT_DIR = Path(os.path.dirname(__file__))

	# ===================================================================================================
	# only interested in files under    - sysval directiory, or 
	#                                   - coal_loadCycler log file, or
	#                                   - coal_brownout log file, or
	#                                   - grapenfcsota directory
	def find_station(self, fileName, dirName):
		coex_station_match_sysval_dirName = re.search(r'sysval_(\S+?)_\S+', dirName)
		coex_station_match_merlot_dirName = re.match(r'grapenfcsota', dirName)
		coex_station_match_loadcycler_fileName = re.match(r'coal_loadCycler_\S+', fileName)
		coex_station_match_brownout_fileName = re.match(r'coal_brownout_\S+', fileName)

		if coex_station_match_sysval_dirName:
			coex_station_seq = coex_station_match_sysval_dirName.group(1)
		elif coex_station_match_merlot_dirName:
			coex_station_seq = 'Merlot'
		elif coex_station_match_loadcycler_fileName:
			coex_station_seq = 'coal_loadCycler'
		elif coex_station_match_brownout_fileName:
			coex_station_seq = 'coal_brownout'
		else:
			coex_station_seq = False

		return coex_station_seq


	# ===================================================================================================
	def find_files_to_be_checked(self):
		files_to_be_checked_dictionary = {}
		for dirPath, folder_under_dirPath, file_under_dirPath in os.walk(self.SystemCoex_Log_Path):  # folders and files under dirPath
			for fileName in file_under_dirPath:
				dirName = os.path.split(os.path.normpath(dirPath))[1]
				filePath = os.path.join(dirPath, fileName)

				coex_station = self.find_station(fileName, dirName)
				is_gz = re.search(r'\.gz$', fileName)

				if coex_station and not is_gz:
					if not coex_station in files_to_be_checked_dictionary:
						files_to_be_checked_dictionary[coex_station] = {}

					files_to_be_checked_dictionary[coex_station][fileName] = {'filePath': filePath, 'dirName':dirName}

		self.files_to_be_checked_dictionary = files_to_be_checked_dictionary

	# ===================================================================================================
	def sort_files_to_be_checked_dictionary(self):
		sorted_files_to_be_checked_dictionary = {}
		sorted_coex_station_list = sorted(self.files_to_be_checked_dictionary)

		for coex_station in sorted_coex_station_list:
			sorted_files_to_be_checked_dictionary[coex_station] =	self.files_to_be_checked_dictionary[coex_station]

		self.files_to_be_checked_dictionary = sorted_files_to_be_checked_dictionary

	# ===================================================================================================
	def import_ignore_list(self):
		errors_to_be_ignored_json_filePath =f'{self.SCRIPT_DIR}/errors_to_be_ignored.json'

		with open(errors_to_be_ignored_json_filePath, 'r') as f:
			errors_to_be_ignored_dictionary = json.load(f)

		for error_type in errors_to_be_ignored_dictionary:
			for error_keyword in errors_to_be_ignored_dictionary[error_type]:
				for error in errors_to_be_ignored_dictionary[error_type][error_keyword]:
					self.ignore_list.append(error)

	# ===================================================================================================
	def import_error_keyword_list(self):
		with open (f"{self.SCRIPT_DIR}/error_keyword_list.json","r") as f:
			self.error_keyword_list = json.load(f)['error_keyword_list']


	# ===================================================================================================
	def is_new_error(self , line):
		new_error = True
		for ignored_error in self.ignore_list:
			if ignored_error in line:
				new_error = False
				break
		return new_error

	# ===================================================================================================
	def is_error_found_unique(self, coex_station, fileName, line):
		unique_error_found = True
		for line_number in self.All_Errors_dictionary[coex_station][fileName]:
			if line.rstrip('\n') == self.All_Errors_dictionary[coex_station][fileName][line_number]:
				unique_error_found = False
				break
		return unique_error_found


	# ===================================================================================================
	def look_for_error_keyword(self, coex_station, fileName, line_number, line ):
	    
		for error_keyword in self.error_keyword_list:
			if error_keyword in line:

				if self.is_new_error(line):

					if self.error_keyword_classcification:

						if not error_keyword in self.All_Errors_dictionary:
							self.All_Errors_dictionary[error_keyword] = {}
						if not coex_station in self.All_Errors_dictionary[error_keyword]:
							self.All_Errors_dictionary[error_keyword][coex_station] = {}
						if not fileName in self.All_Errors_dictionary[error_keyword][coex_station]:
							self.All_Errors_dictionary[error_keyword][coex_station][fileName] = {}

						self.All_Errors_dictionary[error_keyword][coex_station][fileName][f'line {line_number}'] = line.rstrip('\n')

					else:

						if not coex_station in self.All_Errors_dictionary:
							self.All_Errors_dictionary[coex_station] = {}
						if not fileName in self.All_Errors_dictionary[coex_station]:
							self.All_Errors_dictionary[coex_station][fileName] = {}


						if self.is_error_found_unique(coex_station, fileName, line):
							self.All_Errors_dictionary[coex_station][fileName][f'line {line_number}'] = line.rstrip('\n')                    


	# ===================================================================================================
	def check_single_file(self, coex_station, fileName, filePath):
		with open (filePath, 'r') as f:
			line_number = 0

			for line in f:
				line_number += 1
				self.look_for_error_keyword(coex_station, fileName, line_number, line)

	# ===================================================================================================
	def find_all_errors(self):

		self.All_Errors_dictionary = {}

		for coex_station in self.files_to_be_checked_dictionary:
			print(f'{datetime.datetime.now()}: >>>>>>>>>>>>>Start: Checking {coex_station}>>>>>>>>>>>>>')

			for fileName in self.files_to_be_checked_dictionary[coex_station]:
				filePath = self.files_to_be_checked_dictionary[coex_station][fileName]['filePath']

				self.check_single_file(coex_station, fileName, filePath)

			print(f'{datetime.datetime.now()}: >>>>>>>>>>>>>End: Checking {coex_station}>>>>>>>>>>>>>\n')

	# ===================================================================================================
	def All_Errors_dictionary_to_Dataframe(self):
		index_list = []
		error_list = []
		for coex_station in self.All_Errors_dictionary:

			for fileName in self.All_Errors_dictionary[coex_station]:

				for line_number in self.All_Errors_dictionary[coex_station][fileName]:
					index = [coex_station, fileName, line_number]
					index_list.append(index)

					error = self.All_Errors_dictionary[coex_station][fileName][line_number]
					error_list.append(error)

		Index_dataframe = pd.DataFrame(index_list, columns = ['SystemCoex Sequence', 'fileName', 'number_of_line'])
		Index = pd.MultiIndex.from_frame(Index_dataframe)
		self.All_Errors_dataframe = pd.DataFrame(error_list, columns = ['error found'], index = Index)

	# ===================================================================================================
	def dataframe_to_excel(self):
		self.All_Errors_excel_output_path = os.path.join(	os.path.split(os.path.normpath(self.SystemCoex_Log_Path))[0], 
															f'Error_Found_{os.path.split(os.path.normpath(self.SystemCoex_Log_Path))[1]}.xlsx')
		

		
		writer = pd.ExcelWriter(self.All_Errors_excel_output_path, engine = 'openpyxl')
		print('All_Errors_excel_output_path ', self.All_Errors_excel_output_path)
		self.All_Errors_dataframe.to_excel(excel_writer = writer)
		writer.save()
		writer.close()
		print('done')



# def check_log_button_function(dir_path_of_coex_to_be_checked): 
def check_log_button_function(systemcoex_log_path_host):
	systemCoex_log = SystemCoex_Log()
	systemCoex_log.SystemCoex_Log_Path = systemcoex_log_path_host

	systemCoex_log.import_ignore_list()
	systemCoex_log.import_error_keyword_list()

	systemCoex_log.find_files_to_be_checked()
	systemCoex_log.sort_files_to_be_checked_dictionary()

	systemCoex_log.find_all_errors()
	
	if len(systemCoex_log.All_Errors_dictionary) > 0 :
		systemCoex_log.All_Errors_dictionary_to_Dataframe()
		systemCoex_log.dataframe_to_excel()
		command_result = rf'DONE! Errors found export to {systemCoex_log.All_Errors_excel_output_path}'
	else:
		command_result = rf'No error found.'

	return command_result





