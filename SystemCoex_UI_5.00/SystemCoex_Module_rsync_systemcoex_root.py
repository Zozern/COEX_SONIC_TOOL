from SystemCoex_Customized_Tkinter_Widgets import systemcoex_customized_tkinter_widgets
from SystemCoex_host_dependent_actions import host_dependent_actions

class systemcoex_rsync_systemcoex_root_module():
	def __init__(self, Irysnc_Systemcoex_Root_module_layout, device_information_module, font_type, font_size, widget_space_x, widget_space_y):
        # self.font_type = font_type
		# self.font_size = font_size
		self.widget_space_x = widget_space_x
		self.widget_space_y = widget_space_y
		self.Irysnc_Systemcoex_Root_module_layout = Irysnc_Systemcoex_Root_module_layout
		self.coex_tk = systemcoex_customized_tkinter_widgets(font_type, font_size, widget_space_x, widget_space_y)
		self.hda = host_dependent_actions()
		self.device_information_module = device_information_module

	def create_module_frame(self, parent_frame, width_in_pixel, height_in_pixel, border_width, relief_style):
        

		module_frame , body_frame = self.coex_tk.create_ModuleLabelFrame(	parent_frame, width_in_pixel, height_in_pixel, border_width, relief_style, 
																			module_title_name="Rsync Root")

		browse_root_dir_frame, systemcoex_root_dir_path_StringVar = self.__create_browse_root_dir_frame(body_frame)
		reboot_device_button_in_frame, reboot_device_button = self.__create_rsync_root_button(body_frame, systemcoex_root_dir_path_StringVar)



		return module_frame


	def __create_browse_root_dir_frame(self, parent_frame):
		browse_root_dir_frame_width, browse_root_dir_frame_height = self.coex_tk.Calculate_SubFrame_width_and_height(	parent_frame, self.Irysnc_Systemcoex_Root_module_layout, 
																											subframe_name='browse_root_path_frame', 
																											padx=self.widget_space_x/2, pady=self.widget_space_y/2)

		browse_root_dir_frame, systemcoex_root_dir_path_StringVar = self.coex_tk.create_directory_browse_frame( parent_frame, browse_root_dir_frame_width, browse_root_dir_frame_height, 
																												key_name=self.Irysnc_Systemcoex_Root_module_layout['browse_root_path_frame']['key_name_string'] )
		browse_root_dir_frame.grid(	row=self.Irysnc_Systemcoex_Root_module_layout['browse_root_path_frame']['row'], 
									column=self.Irysnc_Systemcoex_Root_module_layout['browse_root_path_frame']['column'],
									sticky='w')

		return browse_root_dir_frame, systemcoex_root_dir_path_StringVar

	def __create_rsync_root_button(self, parent_frame, systemcoex_root_dir_path_StringVar):
		rsync_root_button_width, rsync_root_button_height=self.coex_tk.Calculate_SubFrame_width_and_height(	parent_frame, self.Irysnc_Systemcoex_Root_module_layout, 
																											subframe_name='irysnc_root_button', 
																											padx=self.widget_space_x/2, pady=self.widget_space_y/2)

		reboot_device_button_in_frame, reboot_device_button = self.coex_tk.create_button_in_frame(	parent_frame, 
																									button_name=self.Irysnc_Systemcoex_Root_module_layout['irysnc_root_button']['text'], 
																									width_in_pixel=rsync_root_button_width, 
																									height_in_pixel=rsync_root_button_height, 
																									padx=self.widget_space_x/2, pady=self.widget_space_y/2)

		reboot_device_button_in_frame.grid(	row=self.Irysnc_Systemcoex_Root_module_layout['irysnc_root_button']['row'], 
											column=self.Irysnc_Systemcoex_Root_module_layout['irysnc_root_button']['column'],
											sticky='w')

		reboot_device_button['font'] = (self.coex_tk.font_type, self.coex_tk.font_size+10)
		reboot_device_button['command'] = lambda: self.__rsync_root_button_command(parent_frame, systemcoex_root_dir_path_StringVar.get()+'/')

		return reboot_device_button_in_frame, reboot_device_button

	def __rsync_root_button_command(self, parent_frame, systemcoex_root_dir_path):
		if self.device_information_module.SSHactive:
			self.hda.rsync_host_file_2_device(systemcoex_root_dir_path,'/',retries = 5)
		else:
			self.coex_tk.No_connection_window( 	parent_frame, 
												width=parent_frame['width'] - parent_frame['bd']*2 - self.coex_tk.widget_space_x, 
												height=parent_frame['height'] - parent_frame['bd']*2 - self.coex_tk.widget_space_y )
