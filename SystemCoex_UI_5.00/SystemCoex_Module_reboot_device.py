from SystemCoex_Customized_Tkinter_Widgets import systemcoex_customized_tkinter_widgets
import device_dependent_actions  

class systemcoex_reboot_device_module():
	def __init__(self, device_default_cmd, device_information_module):
		self.device_default_cmd = device_default_cmd
		self.device_default_cmd['reboot_device_cmd'] =  'reboot'
		self.device_information_module = device_information_module

	def create_module_frame(self, parent_frame, font_type, font_size, widget_space_x, widget_space_y, width_in_pixel, height_in_pixel, border_width, relief_style):
		self.dda = device_dependent_actions.device_dependent_actions(self.device_information_module.sshconnect, self.device_default_cmd)
		self.coex_tk = systemcoex_customized_tkinter_widgets(font_type, font_size, widget_space_x, widget_space_y)
		module_frame , body_frame = self.coex_tk.create_ModuleLabelFrame(	parent_frame, width_in_pixel, height_in_pixel, border_width, relief_style, 
																			module_title_name="Reboot Device")


		reboot_device_button_in_frame, reboot_device_button = self.coex_tk.create_button_in_frame(	body_frame, 
																									button_name="Reboot Device", 
																									width_in_pixel=body_frame['width'] - body_frame['bd']*2 - widget_space_x , 
																									height_in_pixel=body_frame['height'] - body_frame['bd']*2 - widget_space_y , 
																									padx=widget_space_x/2, pady=widget_space_y/2)

		reboot_device_button_in_frame.grid(row=0, column=0)

		reboot_device_button['font'] = (font_type, font_size+10)
		reboot_device_button['command'] = lambda: self.__reboot_device_button_command(body_frame)



		return module_frame

	def __reboot_device_button_command(self, parent_frame):
		if self.device_information_module.SSHactive:
			self.dda.send_command_to_device(self.device_default_cmd['reboot_device_cmd'], self.device_information_module.sshconnect)
			# self.device_information_module.init_unit_info_dict()
			self.device_information_module.reboot_flag = True
		else:
			self.coex_tk.No_connection_window( 	parent_frame, 
												width=parent_frame['width'] - parent_frame['bd']*2 - self.coex_tk.widget_space_x, 
												height=parent_frame['height'] - parent_frame['bd']*2 - self.coex_tk.widget_space_y )
