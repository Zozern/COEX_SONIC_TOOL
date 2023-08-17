from SystemCoex_Customized_Tkinter_Widgets import systemcoex_customized_tkinter_widgets
from device_dependent_actions import device_dependent_actions
from SystemCoex_host_dependent_actions import host_dependent_actions 
import tkinter as tk
import os


class systemcoex_irysnc_systemcoex_logs_module():
	def __init__(self, station_list, irysnc_systemcoex_logs_module_layout:dict, device_information_module, device_default_cmd):
		
		self.default_Astro_dir_path = '/var/logs/Astro'
		self.default_OfflinePanda_dir_path = '/AppleInternal/Diags/Logs/Smokey/OfflinePanda'
		self.default_coexpanda_offline_dir_path = '/AppleInternal/Diags/Logs/Smokey/coexpanda_offline'
		self.default_localhost_target_dir_path = '~/systemcoex_logs'

		self.station_list = station_list.copy()
		self.station_list.append('Astro')
		self.station_list.append('Smokey')
		self.station_list.append('All')

		self.device_information_module = device_information_module
		self.device_default_cmd = device_default_cmd
		self.irysnc_systemcoex_logs_module_layout = irysnc_systemcoex_logs_module_layout

	def create_module_frame(self, parent_frame, font_type, font_size, widget_space_x, widget_space_y, width_in_pixel, height_in_pixel, border_width, relief_style ):
		self.coex_tk = systemcoex_customized_tkinter_widgets(font_type, font_size, widget_space_x, widget_space_y)
		module_frame , body_frame = self.coex_tk.create_ModuleLabelFrame(  parent_frame, width_in_pixel, height_in_pixel, border_width, relief_style, 
																									module_title_name="Irysnc Systemcoex Logs")


		directory_path_StringVar, prefix_text_StringVar = self.create_setup_host_target_path_block(body_frame, widget_space_x, widget_space_y)

		

		self.create_rsync_systemcoex_logs_block(directory_path_StringVar, prefix_text_StringVar, body_frame, widget_space_x, widget_space_y)


		return module_frame

	def create_setup_host_target_path_block(self, parent_frame, widget_space_x, widget_space_y):

		block_title_label_width, block_title_label_height = self.coex_tk.Calculate_SubFrame_width_and_height(parent_frame, self.irysnc_systemcoex_logs_module_layout, "setup_host_target_path_label", widget_space_x/2, widget_space_y/2)
		block_title_label_frame, block_title_label = self.coex_tk.create_label_in_frame(	parent_frame, textvariable=tk.StringVar(value=self.irysnc_systemcoex_logs_module_layout['setup_host_target_path_label']['key_name_string']), 
																width_in_pixel=block_title_label_width, height_in_pixel=block_title_label_height)

		block_title_label_frame.grid(	row=self.irysnc_systemcoex_logs_module_layout['setup_host_target_path_label']['row'],
										column=self.irysnc_systemcoex_logs_module_layout['setup_host_target_path_label']['column'],
										columnspan=self.irysnc_systemcoex_logs_module_layout['setup_host_target_path_label']['columnspan'],
										padx=widget_space_x/2, pady=widget_space_y/2, sticky='w')


		browse_host_path_frame_width, browse_host_path_frame_height = self.coex_tk.Calculate_SubFrame_width_and_height(parent_frame, self.irysnc_systemcoex_logs_module_layout, "browse_host_path_frame", widget_space_x/2, widget_space_y/2)
		browse_host_path_frame, directory_path_StringVar = self.coex_tk.create_directory_browse_frame(	parent_frame, browse_host_path_frame_width, browse_host_path_frame_height, 
																										key_name=self.irysnc_systemcoex_logs_module_layout['browse_host_path_frame']['key_name_string'], 
																										key_label_in_same_row=True, default_dir_path=self.default_localhost_target_dir_path)

		browse_host_path_frame.grid(row=self.irysnc_systemcoex_logs_module_layout['browse_host_path_frame']['row'],
									column=self.irysnc_systemcoex_logs_module_layout['browse_host_path_frame']['column'],
									columnspan=self.irysnc_systemcoex_logs_module_layout['browse_host_path_frame']['columnspan'],
									padx=widget_space_x/2, pady=widget_space_y/2, sticky='w')


		entry_box_frame_width, entry_box_frame_height =  self.coex_tk.Calculate_SubFrame_width_and_height(parent_frame, self.irysnc_systemcoex_logs_module_layout, "prefix_setup_frame", widget_space_x/2, widget_space_y/2)
		entry_box_frame, prefix_text_StringVar = self.coex_tk.create_Entry_box_frame(	parent_frame, entry_box_frame_width, entry_box_frame_height, 
																						key_name=self.irysnc_systemcoex_logs_module_layout['prefix_setup_frame']['key_name_string'], 
																						key_label_in_same_row=True)

		entry_box_frame.grid(	row=self.irysnc_systemcoex_logs_module_layout['prefix_setup_frame']['row'],
								column=self.irysnc_systemcoex_logs_module_layout['prefix_setup_frame']['column'],
								columnspan=self.irysnc_systemcoex_logs_module_layout['prefix_setup_frame']['columnspan'],
								padx=widget_space_x/2, pady=widget_space_y/2, sticky='w')

		return directory_path_StringVar, prefix_text_StringVar



	def create_rsync_systemcoex_logs_block(self, directory_path_StringVar, prefix_text_StringVar, parent_frame, widget_space_x, widget_space_y):

		choose_logs_for_irysnc_combobox_frame_width, choose_logs_for_irysnc_combobox_rame_height = self.coex_tk.Calculate_SubFrame_width_and_height(parent_frame, self.irysnc_systemcoex_logs_module_layout, "choose_logs_for_irysnc_combobox_frame", widget_space_x/2, widget_space_y/2)
		choose_logs_for_irysnc_combobox_frame, choose_logs_for_irysnc_combobox = self.coex_tk.create_combobox_in_frame(	parent_frame, choose_logs_for_irysnc_combobox_frame_width, choose_logs_for_irysnc_combobox_rame_height)

		choose_logs_for_irysnc_combobox.set('Astro')
		choose_logs_for_irysnc_combobox['value'] = self.station_list
		choose_logs_for_irysnc_combobox_frame.grid(	row=self.irysnc_systemcoex_logs_module_layout['choose_logs_for_irysnc_combobox_frame']['row'],
													column=self.irysnc_systemcoex_logs_module_layout['choose_logs_for_irysnc_combobox_frame']['column'],
													columnspan=self.irysnc_systemcoex_logs_module_layout['choose_logs_for_irysnc_combobox_frame']['columnspan'],
													padx=widget_space_x/2, pady=widget_space_y/2, sticky='w')




		rsync_logs_button_width, rsync_logs_button_height = self.coex_tk.Calculate_SubFrame_width_and_height(parent_frame, self.irysnc_systemcoex_logs_module_layout, "irysnc_logs_button", widget_space_x/2, widget_space_y/2)
		rysnc_logs_button_frame, rsync_logs_button = self.coex_tk.create_button_in_frame(	parent_frame, self.irysnc_systemcoex_logs_module_layout['irysnc_logs_button']["text"], 
																							rsync_logs_button_width, rsync_logs_button_height)
		rysnc_logs_button_frame.grid(	row=self.irysnc_systemcoex_logs_module_layout['irysnc_logs_button']['row'],
										column=self.irysnc_systemcoex_logs_module_layout['irysnc_logs_button']['column'],
										rowspan=self.irysnc_systemcoex_logs_module_layout['irysnc_logs_button']['rowspan'],
										padx=widget_space_x/2, pady=widget_space_y/2, sticky='w')

		rsync_logs_button['command'] = lambda: self.rsync_logs_button_command(	parent_frame,
																				directory_path=directory_path_StringVar.get(), 
																				prefix_text=prefix_text_StringVar.get(),
																				product_code=self.device_information_module.unit_info_dict['Product Code'].get(),
																				config=self.device_information_module.unit_info_dict['Config'].get(),
																				serial_number=self.device_information_module.unit_info_dict['SN'].get(),
																				station=choose_logs_for_irysnc_combobox.get()	)

	def __determine_local_host_target_path(self, station, directory_path, prefix_text, product_code, config, serial_number):
		if prefix_text:
			local_host_target_path = f"{directory_path}/{prefix_text}_{product_code}_{config}_{serial_number}"
		else:
			local_host_target_path = f"{directory_path}/{product_code}_{config}_{serial_number}"

		if station == 'All' or station == 'Astro' or station == 'Smokey':
			pass
		else:
			local_host_target_path += '/Astro'

		return local_host_target_path

	def __determine_source_file_path_according_to_station(self, station, sshconnect):
		if station == 'All':
			source_file_path_list = [ self.default_Astro_dir_path, self.default_coexpanda_offline_dir_path, self.default_OfflinePanda_dir_path ]
		elif station == 'Astro':
			source_file_path_list = [ self.default_Astro_dir_path]
		elif station == 'Smokey':
			source_file_path_list = [ self.default_coexpanda_offline_dir_path, self.default_OfflinePanda_dir_path ]
		elif station == 'merlot':
			source_file_path_list = [f'{self.default_Astro_dir_path}/grapenfcsota']
		elif station == '':
			source_file_path_list = []
		else:
			file_list_in_Astro_dir = self.__determine_file_list_in_Astro_dir(sshconnect, self.device_default_cmd)
			source_file_path_list = self.__determin_file_list_for_rysnc( station, file_list_in_Astro_dir )

		return source_file_path_list


	def __determine_file_list_in_Astro_dir(self, sshconnect, device_default_cmd):
		dda = device_dependent_actions(	sshconnect, device_default_cmd	) 
		cmd = f'ls -rt {self.default_Astro_dir_path}'
		file_list_in_Astro_dir = dda.send_command_to_device(cmd)

		return file_list_in_Astro_dir

	def __determin_file_list_for_rysnc(self, station, file_list_in_Astro_dir):
		source_file_path_list = []
		rsync_flag = False
		for line in file_list_in_Astro_dir:
			filename = line.rstrip('\n')
			if f'{station}_start' in filename:
				rsync_flag = True


			if rsync_flag:
				if 'coal_Dali_' in filename:
					source_file_path = f'{self.default_Astro_dir_path}/coal_Dali_*'
				else:
					source_file_path = f"{self.default_Astro_dir_path}/{filename}"
			
				source_file_path_list.append(source_file_path)

			
			if f'{station}_end' in filename or f'{station}_done' in filename:
				rsync_flag = False
		return source_file_path_list


	


	def rsync_logs_button_command(	self, parent_frame, directory_path, prefix_text, product_code, config, serial_number, station	):
		
		if self.device_information_module.SSHactive:

			local_host_target_path = self.__determine_local_host_target_path(station, directory_path, prefix_text, product_code, config, serial_number)

			source_file_path_list = self.__determine_source_file_path_according_to_station( station, self.device_information_module.sshconnect )
			
			hda = host_dependent_actions()
			for source_file_path in source_file_path_list:

				hda.rsync_device_file_2_host(src_path=source_file_path ,tar_path=local_host_target_path, retries = 5)

		else:
			self.coex_tk.No_connection_window(	parent_frame, 
												width=parent_frame['width'] - parent_frame['bd']*2 - self.coex_tk.widget_space_x, 
												height=parent_frame['height'] - parent_frame['bd']*2 - self.coex_tk.widget_space_y)