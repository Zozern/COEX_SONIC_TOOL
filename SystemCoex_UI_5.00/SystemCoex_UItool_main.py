import SystemCoex_Customized_modules as Coex_modules
import SystemCoex_host_functions as host_functions
import tkinter as tk    
import os
from pathlib import Path
import tkinter as tk

SCRIPT_DIR = Path(os.path.dirname(__file__))
layout_settings_json_file_name = 'layout_settings.json'
other_settings_json_file_name = 'other_settings.json'


layout_settings = host_functions.load_json_file(f"{SCRIPT_DIR}/{layout_settings_json_file_name}")
other_settings = host_functions.load_json_file(f"{SCRIPT_DIR}/{other_settings_json_file_name}")

font_type = layout_settings['main_window']["font_type"]
font_size = layout_settings['main_window']["font_size"]

window_title = layout_settings['main_window']['title']
window_width = layout_settings['main_window']['width']
window_height = layout_settings['main_window']['height']

main_window = tk.Tk()
main_window.title(window_title)
window_frame  = tk.Frame(main_window, width=window_width, height=window_height)
window_frame.grid_propagate(0)
window_frame.grid()


CoexTool_window_layout = layout_settings["CoexTool_window_layout"]
modules_space_x, modules_space_y = layout_settings['main_window']["modules_space_x"], layout_settings['main_window']["modules_space_y"]
widget_space_x, widget_space_y = layout_settings['main_window']["widget_space_x"], layout_settings['main_window']["widget_space_y"]




# =============================================================================================================================================================================================================================
# create header GUI module

header_GUI_module_layout = layout_settings["header_GUI_module_layout"]
header_GUI_module_width, header_GUI_module_height = Coex_modules.Calculate_SubFrame_width_and_height(window_frame, CoexTool_window_layout, "header GUI", modules_space_x, modules_space_x)

header_GUI_module = Coex_modules.create_header_GUI_module(  window_frame, header_GUI_module_layout, header_GUI_module_width, header_GUI_module_height, 
															module_border_width=3, module_relief_style='ridge', font_type=font_type, font_size=font_size, 
                                    						main_window=main_window, widget_space_x=widget_space_x, widget_space_y=widget_space_y	)

header_GUI_module.grid(row=0, column=0, columnspan=3, padx=modules_space_x/2, pady=modules_space_y/2, sticky='w')






# =============================================================================================================================================================================================================================
# create device information module

device_information_module_width, device_information_module_height = Coex_modules.Calculate_SubFrame_width_and_height(window_frame, CoexTool_window_layout, "Device Information", modules_space_x, modules_space_x)

device_information_module_layout = layout_settings["device_information_module_layout"]

Device_information_module, device_information_dict = Coex_modules.create_device_information_module( window_frame, device_information_module_layout, device_information_module_width, device_information_module_height, 
                                                                                                    module_border_width=3, module_relief_style='ridge', font_type=font_type, font_size=font_size, 
                                                                                                    widget_space_x=widget_space_x, widget_space_y=widget_space_y)
Device_information_module.grid( row=1, column=0, columnspan=3, padx=modules_space_x/2, pady=modules_space_y/2, sticky='w')


# =============================================================================================================================================================================================================================
# create Delete Systemcoex data module

delete_systemcoex_data_module_width, delete_systemcoex_data_module_height = Coex_modules.Calculate_SubFrame_width_and_height(window_frame, CoexTool_window_layout, "Delete Systemcoex data", modules_space_x, modules_space_x)
delete_systemcoex_data_module_layout = layout_settings["Delete_Systemcoex_data_module_layout"]
systemcoex_stations_list = host_functions.load_json_file(f"{SCRIPT_DIR}/{other_settings_json_file_name}")['systemcoex_stations_list']
delete_systemcoex_data_module, delete_buttons_dict = Coex_modules.create_delete_systemcoex_data_module( window_frame, delete_systemcoex_data_module_layout, systemcoex_stations_list, delete_systemcoex_data_module_width, delete_systemcoex_data_module_height, 
																										module_border_width=3, module_relief_style='ridge', font_type=font_type, font_size=font_size, 
																										widget_space_x=widget_space_x, widget_space_y=widget_space_y  )

delete_systemcoex_data_module.grid(row=2, column=0, columnspan=1, padx=modules_space_x/2, pady=modules_space_y/2, sticky='w')

# # =============================================================================================================================================================================================================================
# # create Change Boot-args module
change_device_boot_args_module_width, change_device_boot_args_module_height = Coex_modules.Calculate_SubFrame_width_and_height(window_frame, CoexTool_window_layout, "Change Device Boot-args", modules_space_x, modules_space_x)
change_device_boot_args_module_layout = layout_settings["Change_Device_Boot-args_module_layout"]
systemcoex_stations_list = host_functions.load_json_file(f"{SCRIPT_DIR}/{other_settings_json_file_name}")['systemcoex_stations_list']
change_device_boot_args_module, change_bootargs_dict = Coex_modules.create_change_device_boot_args_module(	window_frame, change_device_boot_args_module_layout, systemcoex_stations_list, change_device_boot_args_module_width, change_device_boot_args_module_height, 
																											module_border_width=3, module_relief_style='ridge', font_type=font_type, font_size=font_size, 
																											widget_space_x=widget_space_x, widget_space_y=widget_space_y  )

change_device_boot_args_module.grid(row=3, column=0, columnspan=1, padx=modules_space_x/2, pady=modules_space_y/2, sticky='w')




# # =============================================================================================================================================================================================================================
# # create Check Systemcoex Logs module
check_systemcoex_logs_module_width, check_systemcoex_logs_module_height = Coex_modules.Calculate_SubFrame_width_and_height(window_frame, CoexTool_window_layout, "Check Systemcoex Logs", modules_space_x, modules_space_x)
check_systemcoex_logs_module_layout = layout_settings["Check_Systemcoex_Logs_module_layout"]
check_systemcoex_logs_module = Coex_modules.create_check_systemcoex_logs_module(  window_frame, check_systemcoex_logs_module_layout, check_systemcoex_logs_module_width, check_systemcoex_logs_module_height, 
                                                                                    module_border_width=3, module_relief_style='ridge', font_type=font_type, font_size=font_size, 
																					widget_space_x=widget_space_x, widget_space_y=widget_space_y  )

check_systemcoex_logs_module.grid(row=2, column=1, columnspan=1, padx=modules_space_x/2, pady=modules_space_y/2, sticky='w')


# # =============================================================================================================================================================================================================================
# # create Reboot Button

reboot_device_module_layout = layout_settings["Reboot_Device_module_layout"]
reboot_device_module_width, reboot_device_module_height = Coex_modules.Calculate_SubFrame_width_and_height(window_frame, CoexTool_window_layout, "Reboot Device", modules_space_x, modules_space_x)
reboot_device_module = Coex_modules.create_reboot_device_module(  	window_frame, reboot_device_module_layout, reboot_device_module_width, reboot_device_module_height, 
																	module_border_width=3, module_relief_style='ridge', font_type=font_type, font_size=30, 
                                    								widget_space_x=widget_space_x, widget_space_y=widget_space_y)

reboot_device_module.grid(row=2, column=2, columnspan=1, padx=modules_space_x/2, pady=modules_space_y/2, sticky='w')




# # =============================================================================================================================================================================================================================
# # create irysnc Systemcoex Logs module
irysnc_systemcoex_logs_module_width, irysnc_systemcoex_logs_module_height = Coex_modules.Calculate_SubFrame_width_and_height(window_frame, CoexTool_window_layout, "Irysnc Systemcoex Logs", modules_space_x, modules_space_x)
irysnc_systemcoex_logs_module_layout = layout_settings["Irysnc_Systemcoex_Logs_module_layout"]
irysnc_systemcoex_logs_module = Coex_modules.create_irysnc_systemcoex_logs_module(  window_frame, irysnc_systemcoex_logs_module_layout, irysnc_systemcoex_logs_module_width, irysnc_systemcoex_logs_module_height, 
                                                                                    module_border_width=3, module_relief_style='ridge', font_type=font_type, font_size=font_size, 
																					widget_space_x=widget_space_x, widget_space_y=widget_space_y  )




irysnc_systemcoex_logs_module.grid(row=3, column=1, columnspan=2, padx=modules_space_x/2, pady=modules_space_y/2, sticky='w')


# # =============================================================================================================================================================================================================================
# # create result output module
result_output_module_width, result_output_module_height = Coex_modules.Calculate_SubFrame_width_and_height(window_frame, CoexTool_window_layout, "Result Output", modules_space_x, modules_space_x)
result_output_module = Coex_modules.create_result_output_module(window_frame, result_output_module_width, result_output_module_height, module_border_width=3, module_relief_style='ridge', 
																font_type=font_type, font_size=font_size, widget_space_x=widget_space_x, widget_space_y=widget_space_y)


result_output_module.grid(row=4, column=0, columnspan=3, padx=modules_space_x/2, pady=modules_space_y/2, sticky='w')

main_window.mainloop() 