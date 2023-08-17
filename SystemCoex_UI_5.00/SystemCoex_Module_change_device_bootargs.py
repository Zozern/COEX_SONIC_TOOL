import device_dependent_actions  
from SystemCoex_Customized_Tkinter_Widgets import systemcoex_customized_tkinter_widgets
import tkinter as tk

class systemcoex_change_device_bootargs_module():
	def __init__(self, station_list, change_device_bootargs_module_layout, device_information_module, device_default_cmd):

		self.station_list = station_list.copy()
		self.station_list.append('none')
		self.station_list.remove('merlot')
		self.number_of_columns = change_device_bootargs_module_layout["max_column_number"]
		self.number_of_rows = len(self.station_list)//self.number_of_columns + 1 if len(self.station_list)%self.number_of_columns > 0 else len(self.station_list)//self.number_of_columns 
		self.device_information_module = device_information_module
		self.device_default_cmd = device_default_cmd

	def __create_change_device_bootargs_module_layout(self) -> dict:
		change_device_bootargs_module_layout = {}

		for i, station in enumerate(self.station_list):
			change_device_bootargs_module_layout[station] = {}
			change_device_bootargs_module_layout[station]['button_name'] = station
			change_device_bootargs_module_layout[station]['row'] = int(i / self.number_of_columns)
			change_device_bootargs_module_layout[station]['column'] = i % self.number_of_columns
			change_device_bootargs_module_layout[station]['columnspan'] = 1
			change_device_bootargs_module_layout[station]['relative_width'] = f"1/{self.number_of_columns}" 
			change_device_bootargs_module_layout[station]['relative_height'] = f"1/{self.number_of_rows}"

		return change_device_bootargs_module_layout

	def create_module_frame(self, parent_frame, font_type, font_size, widget_space_x, widget_space_y, width_in_pixel, height_in_pixel, border_width, relief_style ):

		self.widget_space_x = widget_space_x
		self.widget_space_y = widget_space_y
		self.Coex_DUT = device_dependent_actions.device_dependent_actions(self.device_information_module.sshconnect, self.device_default_cmd)

		self.coex_tk = systemcoex_customized_tkinter_widgets(font_type, font_size, widget_space_x, widget_space_y)
		module_frame , body_frame = self.coex_tk.create_ModuleLabelFrame(   parent_frame, width_in_pixel, height_in_pixel, border_width, relief_style, 
																								module_title_name="Change Device Boot-args")
        
		change_device_bootargs_module_layout = self.__create_change_device_bootargs_module_layout()

		for station in change_device_bootargs_module_layout:
			button_width_in_pixel, button_height_in_pixel = self.coex_tk.Calculate_SubFrame_width_and_height(body_frame, change_device_bootargs_module_layout, station, widget_space_x/2, widget_space_y/2)
			button_in_frame, button = self.coex_tk.create_button_in_frame(  		parent_frame=body_frame, 
																			button_name=change_device_bootargs_module_layout[station]["button_name"],
																			width_in_pixel=button_width_in_pixel, 
																			height_in_pixel=button_height_in_pixel, 
																			padx=widget_space_x/2, pady=widget_space_y/2)
			button_in_frame.grid(	row=change_device_bootargs_module_layout[station]['row'], 
									column=change_device_bootargs_module_layout[station]['column'], 
									padx=widget_space_x/2, pady=widget_space_y/2, sticky='w'	)


			button['command'] = lambda arg=button['text']: self.__change_bootargs_button_command(body_frame, station=arg)


		return module_frame

	def __change_bootargs_button_command(self, parent_frame, station):
		if self.device_information_module.SSHactive:
			self.Coex_DUT.change_boot_args(	station=station, 
											device_code=self.device_information_module.unit_info_dict['Product Code'].get(),
											device_cfg=self.device_information_module.unit_info_dict['Config'].get(),
											sconn=self.device_information_module.sshconnect	)
		else:
			self.coex_tk.No_connection_window(	parent_frame, 
												width=parent_frame['width'] - parent_frame['bd']*2 - self.widget_space_x, 
												height=parent_frame['height'] - parent_frame['bd']*2 - self.widget_space_y)
		