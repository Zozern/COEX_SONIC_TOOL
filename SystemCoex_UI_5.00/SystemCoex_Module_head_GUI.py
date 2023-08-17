from SystemCoex_Customized_Tkinter_Widgets import systemcoex_customized_tkinter_widgets


class systemcoex_head_GUI_module():
	def __init__(self, window, header_GUI_module_layout):
		self.main_window = window
		self.header_GUI_module_layout = header_GUI_module_layout




	def create_module_frame(self, parent_frame, font_type, font_size, widget_space_x, widget_space_y, width_in_pixel, height_in_pixel, border_width, relief_style ):
		self.coex_tk = systemcoex_customized_tkinter_widgets(font_type, font_size, widget_space_x, widget_space_y)
		module_frame , body_frame = self.coex_tk.create_ModuleLabelFrame(  parent_frame, width_in_pixel, height_in_pixel, border_width, relief_style)

		Quit_button_in_frame, Quit_button = self.create_quit_button(body_frame, self.header_GUI_module_layout, widget_space_x, widget_space_y)
		Quit_button_in_frame.grid(	row=self.header_GUI_module_layout["Quit_button"]["row"], 
									column=self.header_GUI_module_layout["Quit_button"]["column"], 
									padx=widget_space_x/2, pady=widget_space_y/2, sticky='w')

		Setting_button_in_frame, Setting_button = self.create_setting_button(body_frame, self.header_GUI_module_layout, widget_space_x, widget_space_y)
		Setting_button_in_frame.grid(	row=self.header_GUI_module_layout["Setting_button"]["row"], 
										column=self.header_GUI_module_layout["Setting_button"]["column"], 
										padx=widget_space_x/2, pady=widget_space_y/2, sticky='w')

		Switch_debugpowr_button_in_frame, Switch_debugpowr_button = self.create_switch_debugpower_button(body_frame, self.header_GUI_module_layout, widget_space_x, widget_space_y)
		Switch_debugpowr_button_in_frame.grid(	row=self.header_GUI_module_layout["Switch_debugpowr_button"]["row"], 
												column=self.header_GUI_module_layout["Switch_debugpowr_button"]["column"], 
												padx=widget_space_x/2, pady=widget_space_y/2, sticky='w')

		return module_frame

	def create_quit_button(self, parent_frame, header_GUI_module_layout, widget_space_x, widget_space_y):
		quit_button_width_in_pixel, quit_button_height_in_pixel = self.coex_tk.Calculate_SubFrame_width_and_height(parent_frame, header_GUI_module_layout, "Quit_button", widget_space_x/2, widget_space_y/2)
		Quit_button_in_frame, Quit_button = self.coex_tk.create_button_in_frame(parent_frame, button_name=header_GUI_module_layout["Quit_button"]["button_name"], 
																				width_in_pixel=quit_button_width_in_pixel, 
																				height_in_pixel=quit_button_height_in_pixel, 
																				padx=widget_space_x/2, pady=widget_space_y/2, 
																				button_action=self.main_window.quit)
		return Quit_button_in_frame, Quit_button


	def create_setting_button(self, parent_frame, header_GUI_module_layout, widget_space_x, widget_space_y):
		Setting_button_width_in_pixel, Setting_button_height_in_pixel = self.coex_tk.Calculate_SubFrame_width_and_height(parent_frame, header_GUI_module_layout, "Setting_button", widget_space_x/2, widget_space_y/2)
		Setting_button_in_frame, Setting_button = self.coex_tk.create_button_in_frame(  parent_frame, button_name=header_GUI_module_layout["Setting_button"]["button_name"], 
																						width_in_pixel=Setting_button_width_in_pixel, 
																						height_in_pixel=Setting_button_height_in_pixel, 
																						padx=widget_space_x/2, pady=widget_space_y/2)
		return Setting_button_in_frame, Setting_button

	def create_switch_debugpower_button(self, parent_frame, header_GUI_module_layout, widget_space_x, widget_space_y):
		Switch_debugpowr_button_width_in_pixel, Switch_debugpowr_button_height_in_pixel = self.coex_tk.Calculate_SubFrame_width_and_height(parent_frame, header_GUI_module_layout, "Switch_debugpowr_button", widget_space_x/2, widget_space_y/2)
		Switch_debugpowr_button_in_frame, Switch_debugpowr_button = self.coex_tk.create_button_in_frame(	parent_frame, button_name=header_GUI_module_layout["Switch_debugpowr_button"]["button_name"], 
																											width_in_pixel=Switch_debugpowr_button_width_in_pixel, 
																											height_in_pixel=Switch_debugpowr_button_height_in_pixel, 
																											padx=widget_space_x/2, pady=widget_space_y/2)
		return Switch_debugpowr_button_in_frame, Switch_debugpowr_button
		