import device_dependent_actions  
import SystemCoex_host_dependent_actions 
from SystemCoex_Customized_Tkinter_Widgets import systemcoex_customized_tkinter_widgets
import tkinter as tk

class systemcoex_delete_systemcoex_logs_module():
	def __init__(self, station_list, delete_systemcoex_data_module_layout, device_default_cmd, device_information_module):
		self.device_information_module = device_information_module
		



		self.dda = device_dependent_actions.device_dependent_actions(device_information_module.sshconnect, device_default_cmd)
		
		self.station_list = station_list.copy()
		self.station_list.append('all')
		self.number_of_columns = delete_systemcoex_data_module_layout["max_column_number"]
		self.number_of_rows = int(len(self.station_list)/self.number_of_columns) + 1
		self.confirm_delete_topwindow_width=250,
		self.confirm_delete_topwindow_height=80,


	def create_module_frame(self, parent_frame, font_type, font_size, widget_space_x, widget_space_y, width_in_pixel, height_in_pixel, border_width, relief_style ):
		self.font_type=font_type
		self.font_size=font_size
		self.widget_space_x = widget_space_x
		self.widget_space_y = widget_space_y

		self.coex_tk = systemcoex_customized_tkinter_widgets(self.font_type, self.font_size, self.widget_space_x, self.widget_space_y)
		module_frame , body_frame = self.coex_tk.create_ModuleLabelFrame(	parent_frame, width_in_pixel, height_in_pixel, border_width, relief_style, 
																								module_title_name="Delete Systemcoex data")


		self.delete_systemcoex_data_module_layout = {}

		for i, station in enumerate(self.station_list):
			self.delete_systemcoex_data_module_layout[station] = {}
			self.delete_systemcoex_data_module_layout[station]['button_name'] = station
			self.delete_systemcoex_data_module_layout[station]['row'] = int(i / self.number_of_columns)
			self.delete_systemcoex_data_module_layout[station]['column'] = i % self.number_of_columns
			self.delete_systemcoex_data_module_layout[station]['columnspan'] = 1
			self.delete_systemcoex_data_module_layout[station]['relative_width'] = f"1/{self.number_of_columns}" 
			self.delete_systemcoex_data_module_layout[station]['relative_height'] = f"1/{self.number_of_rows}"

			button_width_in_pixel, button_height_in_pixel = self.coex_tk.Calculate_SubFrame_width_and_height(body_frame, self.delete_systemcoex_data_module_layout, station, widget_space_x/2, widget_space_y/2)
			button_in_frame, button = self.coex_tk.create_button_in_frame(  parent_frame=body_frame, 
																			button_name=self.delete_systemcoex_data_module_layout[station]["button_name"],
																			width_in_pixel=button_width_in_pixel, 
																			height_in_pixel=button_height_in_pixel, 
																			padx=widget_space_x/2, pady=widget_space_y/2)

			button_in_frame.grid(	row=self.delete_systemcoex_data_module_layout[station]['row'], 
									column=self.delete_systemcoex_data_module_layout[station]['column'], 
									padx=widget_space_x/2, pady=widget_space_y/2, sticky='w'	)


			button['command'] = lambda arg=button['text']: self.__delete_button_function(	parent_frame=body_frame, 
																							station=arg)

		return module_frame


	def __delete_button_function(self, parent_frame, station):
		if self.device_information_module.SSHactive:


			self.create_confirm_delete_toplevel_window(	parent_frame, 
														station=station,
														width=parent_frame['width'] - parent_frame['bd']*2 - self.widget_space_x, 
														height=parent_frame['height'] - parent_frame['bd']*2 - self.widget_space_y)
		else:

			self.coex_tk.No_connection_window(	parent_frame, 
												width=parent_frame['width'] - parent_frame['bd']*2 - self.widget_space_x, 
												height=parent_frame['height'] - parent_frame['bd']*2 - self.widget_space_y 	)


	def create_confirm_delete_toplevel_window(self, parent_frame, width, height, station):

		confirm_delete_window_frame = tk.Frame(parent_frame, width=width, height=height, bd=1, relief='solid')
		confirm_delete_window_frame.grid_propagate(0)
		confirm_delete_window_frame.grid(row=0, column=0)

		text_frame = tk.Frame(confirm_delete_window_frame, padx=10)
		text_frame.grid(row=0, column=0, columnspan=2, sticky='w'+'e', pady=10)

		text_1 = tk.Label(text_frame, text ='Do you comfirm to delete ', font=(self.font_type, self.font_size))
		text_2 = tk.Label(text_frame, text = station, font=(self.font_type, self.font_size, 'bold'), fg='red')
		text_3 = tk.Label(text_frame, text = " logs ?", font=(self.font_type, self.font_size))
        
		text_1.grid(row=0, column=0)
		text_2.grid(row=0, column=1)
		text_3.grid(row=0, column=2)


		yes_button = tk.Button(confirm_delete_window_frame, text='yes', font=(self.font_type, self.font_size))
		yes_button['command'] = lambda: self.__confirm_delete_yes_button_action(station, confirm_delete_window_frame)
		yes_button.grid(row=1, column=0)

		no_button = tk.Button(confirm_delete_window_frame, text='no', font=(self.font_type, self.font_size), command=confirm_delete_window_frame.destroy)
		no_button.grid(row=1, column=1)


	def __confirm_delete_yes_button_action(self, station, confirm_delete_window_frame):

		self.dda.delete_systemcoex_log_by_station(station, self.device_information_module.sshconnect)

		confirm_delete_window_frame.destroy()


