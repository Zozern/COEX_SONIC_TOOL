import device_dependent_actions 
import SystemCoex_host_dependent_actions 
from SystemCoex_Customized_Tkinter_Widgets import systemcoex_customized_tkinter_widgets
from CheckLog import SystemCoex_Log
from Check_LoadCycler_Log import systemcoex_loadcycler_log
import tkinter as tk
import re, os
import matplotlib.pyplot as plt

ASTRO_PATH = "/var/logs/Astro/"
loadcycler_select_key_list = ['GG_StateOfCharge','GG_Temperature','C26_STATUS','GG_Voltage','GG_AverageCurrent']



class systemcoex_check_systemcoex_logs_module():
	def __init__(self, check_systemcoex_logs_module_layout,device_information_module, device_default_cmd, font_type, font_size, widget_space_x, widget_space_y,):

		self.font_type = font_type
		self.font_size = font_size
		self.widget_space_x = widget_space_x
		self.widget_space_y = widget_space_y
		self.coex_tk = systemcoex_customized_tkinter_widgets(font_type, font_size, widget_space_x, widget_space_y)

		self.check_systemcoex_logs_module_layout = check_systemcoex_logs_module_layout
		
		self.device_default_cmd = device_default_cmd
		self.device_information_module = device_information_module
		self.dda = device_dependent_actions.device_dependent_actions(device_information_module.sshconnect, device_default_cmd)

	def create_module_frame(self, parent_frame, width_in_pixel, height_in_pixel, border_width, relief_style ):
		
		module_frame , body_frame = self.coex_tk.create_ModuleLabelFrame(  parent_frame, width_in_pixel, height_in_pixel, border_width, relief_style, 
																									module_title_name="Check Systemcoex Logs")
        
		browse_systemcoex_logs_frame, self.systemcoex_logs_dir_StringVar = self.create_browse_systemcoex_logs_frame(body_frame)

		find_error_button_in_frame, find_error_button = self.create_find_error_button(body_frame, self.check_systemcoex_logs_module_layout)

		check_loadcycler_button_in_frame, check_loadcycler_button = self.create_check_loadcycler_button(body_frame, self.check_systemcoex_logs_module_layout)

		check_brownout_button_in_frame, check_brownout_button = self.create_check_brownout_button(body_frame, self.check_systemcoex_logs_module_layout)



		return module_frame


	def create_browse_systemcoex_logs_frame(self, parent_frame):
		browse_systemcoex_logs_frame_width, browse_systemcoex_logs_frame_height = self.coex_tk.Calculate_SubFrame_width_and_height(parent_frame, self.check_systemcoex_logs_module_layout, "browse_systemcoex_logs_frame", self.coex_tk.widget_space_x/2, self.coex_tk.widget_space_y/2)
		browse_systemcoex_logs_frame, systemcoex_logs_dir_StringVar = self.coex_tk.create_directory_browse_frame(	parent_frame, browse_systemcoex_logs_frame_width, browse_systemcoex_logs_frame_height, 
																													key_name=self.check_systemcoex_logs_module_layout['browse_systemcoex_logs_frame']['key_name_string'], 
																													key_label_in_same_row=False)

		browse_systemcoex_logs_frame.grid(	row=self.check_systemcoex_logs_module_layout['browse_systemcoex_logs_frame']['row'],
											column=self.check_systemcoex_logs_module_layout['browse_systemcoex_logs_frame']['column'],
											padx=self.coex_tk.widget_space_x/2, pady=self.coex_tk.widget_space_y/2, sticky='w')

		return browse_systemcoex_logs_frame, systemcoex_logs_dir_StringVar

	def create_find_error_button(self, parent_frame, check_systemcoex_logs_module_layout):
		find_error_button_width, find_error_button_height = self.coex_tk.Calculate_SubFrame_width_and_height(parent_frame, self.check_systemcoex_logs_module_layout, "find_errors_button", self.coex_tk.widget_space_x/2, self.coex_tk.widget_space_y/2)
		find_error_button_in_frame, find_error_button = self.coex_tk.create_button_in_frame(parent_frame, 
																							button_name=check_systemcoex_logs_module_layout["find_errors_button"]["button_name_string"], 
																							width_in_pixel=find_error_button_width, 
																							height_in_pixel=find_error_button_height, 
																							padx=self.coex_tk.widget_space_x/2, pady=self.coex_tk.widget_space_y/2)

		find_error_button_in_frame.grid(row=self.check_systemcoex_logs_module_layout['find_errors_button']['row'],
										column=self.check_systemcoex_logs_module_layout['find_errors_button']['column'],
										padx=self.coex_tk.widget_space_x/2, pady=self.coex_tk.widget_space_y/2, sticky='w')

		find_error_button['command'] = lambda: self.find_error_button_command(parent_frame, self.systemcoex_logs_dir_StringVar.get())

		return find_error_button_in_frame, find_error_button


	def find_error_button_command(self, parent_frame, systemcoex_logs_dir_path):
		print(systemcoex_logs_dir_path)
		if systemcoex_logs_dir_path:
			systemCoex_log = SystemCoex_Log()
			systemCoex_log.SystemCoex_Log_Path = systemcoex_logs_dir_path

			systemCoex_log.import_ignore_list()
			systemCoex_log.import_error_keyword_list()

			systemCoex_log.find_files_to_be_checked()
			systemCoex_log.sort_files_to_be_checked_dictionary()

			systemCoex_log.find_all_errors()
			
			if len(systemCoex_log.All_Errors_dictionary) > 0 :
				systemCoex_log.All_Errors_dictionary_to_Dataframe()
				systemCoex_log.dataframe_to_excel()
				message_text = f'DONE!\n Errors found export to {systemCoex_log.All_Errors_excel_output_path}'
				note_window = self.coex_tk.message_window(	parent_frame, 
															width=parent_frame['width'] - parent_frame['bd']*2 - self.coex_tk.widget_space_x, 
															height=parent_frame['height'] - parent_frame['bd']*2 - self.coex_tk.widget_space_y,
															message_text=message_text, message_color='red', 
															font_size=self.coex_tk.font_size)
				
				self.__create_open_errorfound_report_button(note_window, systemCoex_log.All_Errors_excel_output_path)

			else:
				message_text = f'No error found.'
				self.coex_tk.message_window(parent_frame, 
											width=parent_frame['width'] - parent_frame['bd']*2 - self.coex_tk.widget_space_x, 
											height=parent_frame['height'] - parent_frame['bd']*2 - self.coex_tk.widget_space_y,
											message_text=message_text, message_color='red', 
											font_size=self.coex_tk.font_size)			

		else:
			message_text = 'Please selecte a valide directory path'
			self.coex_tk.message_window(parent_frame, 
											width=parent_frame['width'] - parent_frame['bd']*2 - self.coex_tk.widget_space_x, 
											height=parent_frame['height'] - parent_frame['bd']*2 - self.coex_tk.widget_space_y,
											message_text=message_text, message_color='red', 
											font_size=self.coex_tk.font_size)


	def __create_open_errorfound_report_button(self, parent_frame, errorfound_report_path):
		open_errorfound_report_button_frame, open_errorfound_report_button = self.coex_tk.create_button_in_frame(	parent_frame, button_name='Open Report', 
																													width_in_pixel=parent_frame['width']*2/5, 
																													height_in_pixel=parent_frame['height']/3, 
																													button_action=lambda: os.system(f'open {errorfound_report_path}'))
		open_errorfound_report_button_frame.grid(row=1, column=1, columnspan=1)


	def create_check_loadcycler_button(self, parent_frame, check_systemcoex_logs_module):
		check_loadcycler_button_width, check_loadcycler_button_height = self.coex_tk.Calculate_SubFrame_width_and_height(parent_frame, self.check_systemcoex_logs_module_layout, "check_loadcycler_button", self.coex_tk.widget_space_x/2, self.coex_tk.widget_space_y/2)
		check_loadcycler_button_in_frame, check_loadcycler_button = self.coex_tk.create_button_in_frame(parent_frame, 
																										button_name=check_systemcoex_logs_module["check_loadcycler_button"]["button_name_string"], 
																										width_in_pixel=check_loadcycler_button_width, 
																										height_in_pixel=check_loadcycler_button_height, 
																										padx=self.coex_tk.widget_space_x/2, pady=self.coex_tk.widget_space_y/2)

		check_loadcycler_button_in_frame.grid(	row=self.check_systemcoex_logs_module_layout['check_loadcycler_button']['row'],
												column=self.check_systemcoex_logs_module_layout['check_loadcycler_button']['column'],
												padx=self.coex_tk.widget_space_x/2, pady=self.coex_tk.widget_space_y/2, sticky='w')

		check_loadcycler_button['command'] = lambda: self.__check_loadcycler_button_command(parent_frame)

		return check_loadcycler_button_in_frame, check_loadcycler_button


	def __check_loadcycler_button_command(self, parent_frame):
		if self.device_information_module.SSHactive:
			loadcycler_log = systemcoex_loadcycler_log(self.device_information_module.sshconnect, self.device_default_cmd)
			
			loadcycler_csv_file = loadcycler_log.find_loadCycle_csv_file_in_device()
			if loadcycler_csv_file:
				systemcoex_loadcycler_log.parse_loadCycle_csv_file(loadcycler_csv_file)
			else:
				self.coex_tk.message_window(parent_frame, 
											width=parent_frame['width'] - parent_frame['bd']*2 - self.coex_tk.widget_space_x, 
											height=parent_frame['height'] - parent_frame['bd']*2 - self.coex_tk.widget_space_y,
											message_text='Cannot find loadcycler log !', message_color='red', 
											font_size=self.coex_tk.font_size + 5)
				
		else:
			self.coex_tk.No_connection_window(	parent_frame, 
												width=parent_frame['width'] - parent_frame['bd']*2 - self.coex_tk.widget_space_x, 
												height=parent_frame['height'] - parent_frame['bd']*2 - self.coex_tk.widget_space_y 	)







	def create_check_brownout_button(self, parent_frame, check_systemcoex_logs_module):
		check_brownout_button_width, check_brownout_button_height = self.coex_tk.Calculate_SubFrame_width_and_height(parent_frame, self.check_systemcoex_logs_module_layout, "check_brownout_button", self.coex_tk.widget_space_x/2, self.coex_tk.widget_space_y/2)
		check_brownout_button_in_frame, check_brownout_button = self.coex_tk.create_button_in_frame(parent_frame, 
																									button_name=check_systemcoex_logs_module["check_brownout_button"]["button_name_string"], 
																									width_in_pixel=check_brownout_button_width, 
																									height_in_pixel=check_brownout_button_height, 
																									padx=self.coex_tk.widget_space_x/2, pady=self.coex_tk.widget_space_y/2)

		check_brownout_button_in_frame.grid(row=self.check_systemcoex_logs_module_layout['check_brownout_button']['row'],
											column=self.check_systemcoex_logs_module_layout['check_brownout_button']['column'],
											padx=self.coex_tk.widget_space_x/2, pady=self.coex_tk.widget_space_y/2, sticky='w')

		return check_brownout_button_in_frame, check_brownout_button




