from SystemCoex_Module_get_DUT_info import systemcoex_get_DUT_attributes_module
from SystemCoex_Module_head_GUI import systemcoex_head_GUI_module
from SystemCoex_Module_delete_systemcoex_log import systemcoex_delete_systemcoex_logs_module
from SystemCoex_Module_change_device_bootargs import systemcoex_change_device_bootargs_module
from SystemCoex_Module_check_device_logs import systemcoex_check_systemcoex_logs_module
from SystemCoex_Module_reboot_device import systemcoex_reboot_device_module
from SystemCoex_Module_irysnc_systemcoex_logs import systemcoex_irysnc_systemcoex_logs_module
from SystemCoex_Module_rsync_systemcoex_root import systemcoex_rsync_systemcoex_root_module

from SystemCoex_Module_HeadMenu import systemcoex_head_menu_module
from SystemCoex_host_dependent_actions import host_dependent_actions 


import tkinter as tk
from pathlib import Path
import os, re
from time import sleep


def Calculate_SubFrame_width_and_height(parent_frame, parent_frame_layout:dict, subframe_name, padx, pady):
	
	subfrmae_relative_width_string     = parent_frame_layout[subframe_name]['relative_width']
	subfrmae_relative_height_string    = parent_frame_layout[subframe_name]['relative_height']

	subfrmae_relative_width = int(re.search(r"(\d+)\/\d+",subfrmae_relative_width_string).group(1)) / int(re.search(r"\d+\/(\d+)",subfrmae_relative_width_string).group(1))
	subfrmae_relative_height = int(re.search(r"(\d+)\/\d+",subfrmae_relative_height_string).group(1)) / int(re.search(r"\d+\/(\d+)",subfrmae_relative_height_string).group(1))

	subframe_width  = int(  (parent_frame['width'] -  padx*2) * subfrmae_relative_width   - padx*2  )
	subframe_height = int(  (parent_frame['height'] - pady*2) * subfrmae_relative_height  - pady*2  )

	return subframe_width, subframe_height




sshconnect = None
hda = host_dependent_actions()


SCRIPT_DIR = Path(os.path.dirname(__file__))
device_default_cmd_dict = hda.load_json_file(f"{SCRIPT_DIR}/default_unit_command.json")
layout_settings = hda.load_json_file(f"{SCRIPT_DIR}/layout_settings.json")
other_settings = hda.load_json_file(f"{SCRIPT_DIR}/other_settings.json")


main_window_settings = layout_settings['main_window']

font_type = main_window_settings["font_type"]
font_size = main_window_settings["font_size"]
widget_space_x, widget_space_y = main_window_settings["widget_space_x"], main_window_settings["widget_space_y"]
module_border_width = main_window_settings['module_border_width']
module_relief_style = main_window_settings['module_relief_style']
modules_space_x, modules_space_y = main_window_settings["modules_space_x"], main_window_settings["modules_space_y"]


main_window = tk.Tk()
main_window.title(main_window_settings['title'])

window_frame  = tk.Frame(main_window, width=main_window_settings['width'], height=main_window_settings['height'])
window_frame.grid_propagate(0)
window_frame.grid()

CoexTool_window_layout = layout_settings["CoexTool_window_layout"]



# =============================================================================================================================================================================================================================
# create header GUI module

header_GUI_module_width, header_GUI_module_height = Calculate_SubFrame_width_and_height(window_frame, CoexTool_window_layout, "header GUI", modules_space_x/2, modules_space_y/2)

header_GUI_module = systemcoex_head_GUI_module(window=main_window, header_GUI_module_layout=layout_settings["header_GUI_module_layout"])

header_GUI_module_frame = header_GUI_module.create_module_frame(window_frame, font_type, font_size, widget_space_x, widget_space_y, 
																width_in_pixel=header_GUI_module_width, 
																height_in_pixel=header_GUI_module_height, 
																border_width=module_border_width, 
																relief_style=module_relief_style )

header_GUI_module_frame.grid(	row=CoexTool_window_layout["header GUI"]['row'],
								column=CoexTool_window_layout["header GUI"]['column'],
								columnspan=CoexTool_window_layout["header GUI"]['columnspan'],
								padx=modules_space_x/2, pady=modules_space_y/2, sticky='w'	)




# =============================================================================================================================================================================================================================
# create device information module

device_information_module_width, device_information_module_height = Calculate_SubFrame_width_and_height(window_frame, CoexTool_window_layout, "Device Information", modules_space_x/2, modules_space_y/2)

device_information_module = systemcoex_get_DUT_attributes_module(	window=main_window, device_information_module_layout=layout_settings["device_information_module_layout"],
																	device_default_cmd=device_default_cmd_dict	)

device_information_module_frame = device_information_module.create_module_frame(	window_frame, font_type, font_size, widget_space_x, widget_space_y, 
																					width_in_pixel=device_information_module_width, 
																					height_in_pixel=device_information_module_height, 
																					border_width=module_border_width, 
																					relief_style=module_relief_style )

device_information_module_frame.grid(	row=CoexTool_window_layout["Device Information"]['row'],
										column=CoexTool_window_layout["Device Information"]['column'],
										columnspan=CoexTool_window_layout["Device Information"]['columnspan'],
										padx=modules_space_x/2, pady=modules_space_y/2, sticky='w'	)

device_information_module.update_DUT_attributes()


# =============================================================================================================================================================================================================================
# create delete systemcoex logs module

delete_systemcoex_logs_module_width, delete_systemcoex_logs_module_hegiht = Calculate_SubFrame_width_and_height(window_frame, CoexTool_window_layout, "Delete Systemcoex data", modules_space_x/2, modules_space_y/2)
delete_systemcoex_logs_module = systemcoex_delete_systemcoex_logs_module(	station_list=other_settings["systemcoex_stations_list"], 
																			delete_systemcoex_data_module_layout=layout_settings["Delete_Systemcoex_data_module_layout"],
																			device_default_cmd=device_default_cmd_dict,
																			device_information_module = device_information_module	)

delete_systemcoex_logs_module_frame = delete_systemcoex_logs_module.create_module_frame(	window_frame, font_type, font_size, widget_space_x, widget_space_y, 
																							width_in_pixel=delete_systemcoex_logs_module_width, 
																							height_in_pixel=delete_systemcoex_logs_module_hegiht, 
																							border_width=module_border_width, 
																							relief_style=module_relief_style)

delete_systemcoex_logs_module_frame.grid(	row=CoexTool_window_layout["Delete Systemcoex data"]['row'],
											column=CoexTool_window_layout["Delete Systemcoex data"]['column'],
											columnspan=CoexTool_window_layout["Delete Systemcoex data"]['columnspan'],
											padx=modules_space_x/2, pady=modules_space_y/2, sticky='w'	)



# =============================================================================================================================================================================================================================
# create change device boot-args module
change_device_bootargs_module_width, change_device_bootargs_module_hegiht = Calculate_SubFrame_width_and_height(window_frame, CoexTool_window_layout, "Change Device Boot-args", modules_space_x/2, modules_space_y/2)
change_device_bootargs_module = systemcoex_change_device_bootargs_module (	station_list=other_settings["systemcoex_stations_list"], 
																			change_device_bootargs_module_layout=layout_settings['Change_Device_Boot-args_module_layout'], 
																			device_information_module=device_information_module, 
																			device_default_cmd=device_default_cmd_dict)

change_device_bootargs_module_frame = change_device_bootargs_module.create_module_frame(	window_frame, font_type, font_size, widget_space_x, widget_space_y, 
																							width_in_pixel=change_device_bootargs_module_width, 
																							height_in_pixel=change_device_bootargs_module_hegiht, 
																							border_width=module_border_width, 
																							relief_style=module_relief_style)

change_device_bootargs_module_frame.grid(	row=CoexTool_window_layout["Change Device Boot-args"]['row'],
											column=CoexTool_window_layout["Change Device Boot-args"]['column'],
											columnspan=CoexTool_window_layout["Change Device Boot-args"]['columnspan'],
											padx=modules_space_x/2, pady=modules_space_y/2, sticky='w'	)



# =============================================================================================================================================================================================================================
# create check systemcoex logs module
check_systemcoex_logs_module_width, check_systemcoex_logs_module_height = Calculate_SubFrame_width_and_height(window_frame, CoexTool_window_layout, "Check Systemcoex Logs", modules_space_x/2, modules_space_y/2)
check_systemcoex_logs_module = systemcoex_check_systemcoex_logs_module( check_systemcoex_logs_module_layout=layout_settings['Check_Systemcoex_Logs_module_layout'],
																		device_information_module=device_information_module,
																		device_default_cmd=device_default_cmd_dict,
																		font_type=font_type, font_size=font_size, 
																		widget_space_x=widget_space_x, widget_space_y=widget_space_y )

check_systemcoex_logs_module_frame = check_systemcoex_logs_module.create_module_frame(	window_frame,  
																						width_in_pixel=check_systemcoex_logs_module_width, 
																						height_in_pixel=check_systemcoex_logs_module_height, 
																						border_width=module_border_width, 
																						relief_style=module_relief_style)

check_systemcoex_logs_module_frame.grid(row=CoexTool_window_layout["Check Systemcoex Logs"]['row'],
										column=CoexTool_window_layout["Check Systemcoex Logs"]['column'],
										columnspan=CoexTool_window_layout["Check Systemcoex Logs"]['columnspan'],
										padx=modules_space_x/2, pady=modules_space_y/2, sticky='w'	)


# =============================================================================================================================================================================================================================
# create reboot device module
reboot_device_module_width, reboot_device_module_height = Calculate_SubFrame_width_and_height(window_frame, CoexTool_window_layout, "Reboot Device", modules_space_x/2, modules_space_y/2)
reboot_device_module = systemcoex_reboot_device_module( device_default_cmd=device_default_cmd_dict, 
														device_information_module=device_information_module)

reboot_device_module_frame = reboot_device_module.create_module_frame(	window_frame, font_type, font_size, widget_space_x, widget_space_y, 
																		width_in_pixel=reboot_device_module_width, 
																		height_in_pixel=reboot_device_module_height, 
																		border_width=module_border_width, 
																		relief_style=module_relief_style)

reboot_device_module_frame.grid(row=CoexTool_window_layout["Reboot Device"]['row'],
								column=CoexTool_window_layout["Reboot Device"]['column'],
								columnspan=CoexTool_window_layout["Reboot Device"]['columnspan'],
								padx=modules_space_x/2, pady=modules_space_y/2, sticky='w'	)


# =============================================================================================================================================================================================================================
# create irysnc systemcoex logs module
irysnc_systemcoex_logs_module_width, irysnc_systemcoex_logs_module_height = Calculate_SubFrame_width_and_height(window_frame, CoexTool_window_layout, "Irysnc Systemcoex Logs", modules_space_x/2, modules_space_y/2)
irysnc_systemcoex_logs_module = systemcoex_irysnc_systemcoex_logs_module(	station_list=other_settings["systemcoex_stations_list"], 
																			irysnc_systemcoex_logs_module_layout=layout_settings['Irysnc_Systemcoex_Logs_module_layout'],
																			device_information_module = device_information_module,
																			device_default_cmd=device_default_cmd_dict)

irysnc_systemcoex_logs_module_frame = irysnc_systemcoex_logs_module.create_module_frame(window_frame, font_type, font_size, widget_space_x, widget_space_y, 
																						width_in_pixel=irysnc_systemcoex_logs_module_width, 
																						height_in_pixel=irysnc_systemcoex_logs_module_height, 
																						border_width=module_border_width, 
																						relief_style=module_relief_style )

irysnc_systemcoex_logs_module_frame.grid(	row=CoexTool_window_layout["Irysnc Systemcoex Logs"]['row'],
											column=CoexTool_window_layout["Irysnc Systemcoex Logs"]['column'],
											columnspan=CoexTool_window_layout["Irysnc Systemcoex Logs"]['columnspan'],
											padx=modules_space_x/2, pady=modules_space_y/2, sticky='w'	)

# =============================================================================================================================================================================================================================
# create irysnc systemcoex root module
irysnc_systemcoex_root_module_width, irysnc_systemcoex_root_module_height = Calculate_SubFrame_width_and_height(window_frame, CoexTool_window_layout, "Irysnc Systemcoex Root", modules_space_x/2, modules_space_y/2)
irysnc_systemcoex_root_module = systemcoex_rsync_systemcoex_root_module(	Irysnc_Systemcoex_Root_module_layout=layout_settings['Irysnc_Systemcoex_Root_module_layout'], 
																			device_information_module=device_information_module, 
																			font_type=font_type, font_size=font_size, widget_space_x=widget_space_x, widget_space_y=widget_space_y)

irysnc_systemcoex_root_module_frame = irysnc_systemcoex_root_module.create_module_frame(window_frame, 
																						width_in_pixel=irysnc_systemcoex_root_module_width, 
																						height_in_pixel=irysnc_systemcoex_root_module_height, 
																						border_width=module_border_width, 
																						relief_style=module_relief_style )

irysnc_systemcoex_root_module_frame.grid(	row=CoexTool_window_layout["Irysnc Systemcoex Root"]['row'],
											column=CoexTool_window_layout["Irysnc Systemcoex Root"]['column'],
											columnspan=CoexTool_window_layout["Irysnc Systemcoex Root"]['columnspan'],
											padx=modules_space_x/2, pady=modules_space_y/2, sticky='w'	)




main_window.mainloop()








