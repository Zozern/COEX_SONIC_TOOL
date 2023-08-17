import SystemCoex_Customized_Tkinter_Widgets 
import re

def Calculate_SubFrame_width_and_height(parent_frame, parent_frame_layout:dict, subframe_name, widget_space_x, widget_space_y):

    subfrmae_relative_width_string     = parent_frame_layout[subframe_name]['relative_width']
    subfrmae_relative_height_string    = parent_frame_layout[subframe_name]['relative_height']

    subfrmae_relative_width = int(re.search(r"(\d+)\/\d+",subfrmae_relative_width_string).group(1)) / int(re.search(r"\d+\/(\d+)",subfrmae_relative_width_string).group(1))
    subfrmae_relative_height = int(re.search(r"(\d+)\/\d+",subfrmae_relative_height_string).group(1)) / int(re.search(r"\d+\/(\d+)",subfrmae_relative_height_string).group(1))

    subframe_width  = int(  (parent_frame['width'] -  widget_space_x) * subfrmae_relative_width   - widget_space_x  )
    subframe_height = int(  (parent_frame['height'] - widget_space_y) * subfrmae_relative_height  - widget_space_y  )

    return subframe_width, subframe_height




def create_device_information_module(   window, device_information_module_layout, module_width, module_height, module_border_width, module_relief_style, font_type, font_size,  
                                        widget_space_x, widget_space_y):
    
    Coex_tk = SystemCoex_Customized_Tkinter_Widgets.systemcoex_customized_tkinter_widgets(font_type, font_size, widget_space_x, widget_space_y)
    device_information_dict = {}

    # create the ModuleFrame for device information module
    module_title_string = "Device Information"
    ModuleFrame, BodyFrame = Coex_tk.create_ModuleFrame_with_TitleLabel_and_BodyFrame(  parent_frame=window, width_in_pixel=module_width, height_in_pixel=module_height, border_width=module_border_width, relief_style=module_relief_style, 
                                                                                        module_title_name=module_title_string)
    
    key_name_label_width_in_text_letter = max(len(keyname_string) for keyname_string in device_information_module_layout)
    key_name_label_width_in_pixel = key_name_label_width_in_text_letter * font_size * 0.5

    for key_name_string in device_information_module_layout:
        
        KeyLabel_ValueLabel_frame_width, KeyLabel_ValueLabel_frame_height = Calculate_SubFrame_width_and_height(BodyFrame, device_information_module_layout, key_name_string, widget_space_x, widget_space_y)
        
        KeyLabel_ValueLabel_frame, value_StringVar = Coex_tk.create_KeyValueLabelPair_frame(    frame=BodyFrame, frame_width_in_pixel=KeyLabel_ValueLabel_frame_width, frame_height_in_pixel=KeyLabel_ValueLabel_frame_height, 
                                                                                                key_name=key_name_string, key_label_width_in_pixel=key_name_label_width_in_pixel,
                                                                                                copy_button_exist=device_information_module_layout[key_name_string]['copy_button'])

        KeyLabel_ValueLabel_frame.grid( row=device_information_module_layout[key_name_string]['row'], column=device_information_module_layout[key_name_string]['column'],
                                        padx=widget_space_x/2, pady=widget_space_y/2,
                                        columnspan=device_information_module_layout[key_name_string]['columnspan'], sticky='w'  )
        
        device_information_dict[key_name_string] = value_StringVar


    return ModuleFrame, device_information_dict


def create_header_GUI_module(   parent_frame, header_GUI_module_layout, module_width, module_height, module_border_width, module_relief_style, font_type, font_size,  
                                main_window, widget_space_x, widget_space_y):
    Coex_tk = SystemCoex_Customized_Tkinter_Widgets.systemcoex_customized_tkinter_widgets(font_type, font_size, widget_space_x, widget_space_y)

    # create the ModuleFrame for device information module
    ModuleFrame, BodyFrame = Coex_tk.create_ModuleFrame_with_TitleLabel_and_BodyFrame(  parent_frame=parent_frame, width_in_pixel=module_width, height_in_pixel=module_height, border_width=module_border_width, relief_style=module_relief_style)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    quit_button_width_in_pixel, quit_button_height_in_pixel = Calculate_SubFrame_width_and_height(BodyFrame, header_GUI_module_layout, "Quit_button", widget_space_x, widget_space_y)
    Quit_button_in_frame, Quit_button = Coex_tk.create_button_in_frame( BodyFrame, button_name=header_GUI_module_layout["Quit_button"]["button_name"], 
                                                                        width_in_pixel=quit_button_width_in_pixel, height_in_pixel=quit_button_height_in_pixel, padx=widget_space_x, pady=widget_space_y, 
                                                                        button_action=main_window.quit)
    Quit_button_in_frame.grid(row=header_GUI_module_layout["Quit_button"]["row"], column=header_GUI_module_layout["Quit_button"]["column"], sticky='w')


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    Setting_button_width_in_pixel, Setting_button_height_in_pixel = Calculate_SubFrame_width_and_height(BodyFrame, header_GUI_module_layout, "Setting_button", widget_space_x, widget_space_y)
    Setting_button_in_frame, Setting_button = Coex_tk.create_button_in_frame(   BodyFrame, button_name=header_GUI_module_layout["Setting_button"]["button_name"], 
                                                                                width_in_pixel=Setting_button_width_in_pixel, height_in_pixel=Setting_button_height_in_pixel, padx=widget_space_x, pady=widget_space_y)

    Setting_button_in_frame.grid(row=header_GUI_module_layout["Setting_button"]["row"], column=header_GUI_module_layout["Setting_button"]["column"], sticky='w')


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    Switch_debugpowr_button_width_in_pixel, Switch_debugpowr_button_height_in_pixel = Calculate_SubFrame_width_and_height(BodyFrame, header_GUI_module_layout, "Switch_debugpowr_button", widget_space_x, widget_space_y)
    Switch_debugpowr_button_in_frame, Switch_debugpowr_button = Coex_tk.create_button_in_frame(  BodyFrame, button_name=header_GUI_module_layout["Switch_debugpowr_button"]["button_name"], 
                                                                                                width_in_pixel=Setting_button_width_in_pixel, height_in_pixel=Setting_button_height_in_pixel, padx=widget_space_x, pady=widget_space_y)
    
    Switch_debugpowr_button_in_frame.grid(row=header_GUI_module_layout["Switch_debugpowr_button"]["row"], column=header_GUI_module_layout["Switch_debugpowr_button"]["column"], sticky='w')

    return ModuleFrame


def create_delete_systemcoex_data_module(   parent_frame, delete_systemcoex_data_module_layout, station_list, module_width, module_height, module_border_width, module_relief_style, font_type, font_size,
                                            widget_space_x, widget_space_y  ):
    
    module_title_string = "Delete Systemcoex data"
    Coex_tk = SystemCoex_Customized_Tkinter_Widgets.systemcoex_customized_tkinter_widgets(font_type, font_size, widget_space_x, widget_space_y)
    ModuleFrame, BodyFrame = Coex_tk.create_ModuleFrame_with_TitleLabel_and_BodyFrame(  parent_frame=parent_frame, width_in_pixel=module_width, height_in_pixel=module_height, border_width=module_border_width, relief_style=module_relief_style,
                                                                                        module_title_name=module_title_string)

    station_list.append('all')
    max_column_number = delete_systemcoex_data_module_layout["max_column_number"]
    max_row_number = int(len(station_list)/max_column_number) + 1
    layout = {}
    buttons_dict = {}
    for i, station in enumerate(station_list):
        layout[station] = {}
        layout[station]['button_name'] = station
        layout[station]['row'] = int(i / max_column_number)
        layout[station]['column'] = i % max_column_number
        layout[station]['columnspan'] = 1
        layout[station]['relative_width'] = f"1/{max_column_number}" 
        layout[station]['relative_height'] = f"1/{max_row_number}"

        button_width_in_pixel, button_height_in_pixel = Calculate_SubFrame_width_and_height(BodyFrame, layout, station, widget_space_x, widget_space_y)
        button_in_frame, button = Coex_tk.create_button_in_frame(   BodyFrame, button_name=layout[station]["button_name"],
                                                                    width_in_pixel=button_width_in_pixel, height_in_pixel=button_height_in_pixel, padx=widget_space_x, pady=widget_space_y)
        button['command'] = lambda arg=f"delete {button['text']}": print(arg)
        button_in_frame.grid(row=layout[station]['row'], column=layout[station]['column'], padx=widget_space_x/2, pady=widget_space_y/2, sticky='w')

        buttons_dict[station] = button


    for _ , delete_button in buttons_dict.items():
        delete_button['command'] = lambda arg=delete_button['text']: Coex_tk.create_confirm_delete_toplevel_window(arg, toplevel_window_width=250, toplevel_window_height=80)

    return ModuleFrame, buttons_dict




def create_change_device_boot_args_module(  parent_frame, change_device_boot_args_layout, station_list, module_width, module_height, module_border_width, module_relief_style, font_type, font_size,
                                            widget_space_x, widget_space_y  ):
    
    module_title_string = "Change Device Boot-args"
    Coex_tk = SystemCoex_Customized_Tkinter_Widgets.systemcoex_customized_tkinter_widgets(font_type, font_size, widget_space_x, widget_space_y)
    ModuleFrame, BodyFrame = Coex_tk.create_ModuleFrame_with_TitleLabel_and_BodyFrame(  parent_frame=parent_frame, width_in_pixel=module_width, height_in_pixel=module_height, border_width=module_border_width, relief_style=module_relief_style,
                                                                                        module_title_name=module_title_string)

    station_list.append('none')
    max_column_number = change_device_boot_args_layout["max_column_number"]
    max_row_number = int(len(station_list)/max_column_number) + 1
    layout = {}
    buttons_dict = {}
    for i, station in enumerate(station_list):
        layout[station] = {}
        layout[station]['button_name'] = station
        layout[station]['row'] = int(i / max_column_number)
        layout[station]['column'] = i % max_column_number
        layout[station]['columnspan'] = 1
        layout[station]['relative_width'] = f"1/{max_column_number}" 
        layout[station]['relative_height'] = f"1/{max_row_number}"

        button_width_in_pixel, button_height_in_pixel = Calculate_SubFrame_width_and_height(BodyFrame, layout, station, widget_space_x, widget_space_y)
        button_in_frame, button = Coex_tk.create_button_in_frame(BodyFrame, button_name=layout[station]["button_name"],
                                                width_in_pixel=button_width_in_pixel, height_in_pixel=button_height_in_pixel, padx=widget_space_x, pady=widget_space_y)
        button['command'] = lambda arg=f"astro={button['text']}": print(arg)
        button_in_frame.grid(row=layout[station]['row'], column=layout[station]['column'], padx=widget_space_x/2, pady=widget_space_y/2, sticky='w')

        buttons_dict[station] = button

    return ModuleFrame, buttons_dict

















def create_irysnc_systemcoex_logs_module(   parent_frame, irysnc_systemcoex_logs_module_layout, module_width, module_height, module_border_width, module_relief_style, font_type, font_size, 
                                            widget_space_x, widget_space_y  ):
    module_title_string = "Irysnc Systemcoex Logs"

    Coex_tk = SystemCoex_Customized_Tkinter_Widgets.systemcoex_customized_tkinter_widgets(font_type, font_size, widget_space_x, widget_space_y)
    ModuleFrame, BodyFrame = Coex_tk.create_ModuleFrame_with_TitleLabel_and_BodyFrame(  parent_frame=parent_frame, width_in_pixel=module_width, height_in_pixel=module_height, border_width=module_border_width, relief_style=module_relief_style,
                                                                                        module_title_name=module_title_string)

    target_dir_browse_frame_row, target_dir_browse_frame_column = irysnc_systemcoex_logs_module_layout["browse_host_path_frame"]['row'], irysnc_systemcoex_logs_module_layout["browse_host_path_frame"]['column']
    target_dir_browse_frame_columnspan = irysnc_systemcoex_logs_module_layout["browse_host_path_frame"]['columnspan']
    target_dir_browse_frame_width, target_dir_browse_frame_height = Calculate_SubFrame_width_and_height(BodyFrame, irysnc_systemcoex_logs_module_layout, "browse_host_path_frame", widget_space_x, widget_space_y)
    target_dir_browse_frame_keyname = "Target Directory"
    # target_dir_browse_frame_keylabel_width = len(target_dir_browse_frame_keyname) * font_size * 0.6
    
    target_dir_browse_frame = Coex_tk.create_directory_browse_frame(BodyFrame, target_dir_browse_frame_width, target_dir_browse_frame_height,  
                                                                    key_name=target_dir_browse_frame_keyname)
    target_dir_browse_frame.grid(row=target_dir_browse_frame_row, column=target_dir_browse_frame_column, columnspan=target_dir_browse_frame_columnspan, sticky='w')


    prefix_entrybox_frame_row, prefix_entrybox_frame_column = irysnc_systemcoex_logs_module_layout["prefix_setup_frame"]['row'], irysnc_systemcoex_logs_module_layout["prefix_setup_frame"]['column']
    prefix_entrybox_frame_columnspan = irysnc_systemcoex_logs_module_layout["prefix_setup_frame"]['columnspan']
    prefix_entrybox_frame_width, prefix_entrybox_frame_height = Calculate_SubFrame_width_and_height(BodyFrame, irysnc_systemcoex_logs_module_layout, "prefix_setup_frame", widget_space_x, widget_space_y)
    prefix_entrybox_frame_keyname = irysnc_systemcoex_logs_module_layout["prefix_setup_frame"]["key_name_string"]
    prefix_entrybox_frame_keylabel_width = len(prefix_entrybox_frame_keyname) * font_size * 0.6
    
    prefix_entrybox_frame, prefix_entrybox_text = Coex_tk.create_Entry_box_frame(   BodyFrame, prefix_entrybox_frame_width, prefix_entrybox_frame_height, 
                                                                                    prefix_entrybox_frame_keyname)
    prefix_entrybox_frame.grid(row=prefix_entrybox_frame_row, column=prefix_entrybox_frame_column, columnspan=prefix_entrybox_frame_columnspan, sticky='w')
    

    irysnc_astro_logs_button_width, irysnc_astro_logs_button_height = Calculate_SubFrame_width_and_height(BodyFrame, irysnc_systemcoex_logs_module_layout, "irysnc_astro_logs_button", widget_space_x, widget_space_y)
    irysnc_astro_logs_button_row, irysnc_astro_logs_button_column = irysnc_systemcoex_logs_module_layout["irysnc_astro_logs_button"]['row'], irysnc_systemcoex_logs_module_layout["irysnc_astro_logs_button"]['column']
    irysnc_astro_logs_button_text = irysnc_systemcoex_logs_module_layout["irysnc_astro_logs_button"]['button_name_string']
    
    irysnc_astro_logs_button_in_frame, irysnc_astro_logs_button = Coex_tk.create_button_in_frame(BodyFrame, irysnc_astro_logs_button_text, irysnc_astro_logs_button_width, irysnc_astro_logs_button_height, padx=widget_space_x/2, pady=widget_space_y/2)
    irysnc_astro_logs_button_in_frame.grid(row=irysnc_astro_logs_button_row, column=irysnc_astro_logs_button_column, padx=widget_space_x*2, pady=widget_space_y*2)


    irysnc_smokey_logs_button_width, irysnc_smokey_logs_button_height = Calculate_SubFrame_width_and_height(BodyFrame, irysnc_systemcoex_logs_module_layout, "irysnc_smokey_logs_button", widget_space_x, widget_space_y)
    irysnc_smokey_logs_button_row, irysnc_smokey_logs_button_column = irysnc_systemcoex_logs_module_layout["irysnc_smokey_logs_button"]['row'], irysnc_systemcoex_logs_module_layout["irysnc_smokey_logs_button"]['column']
    irysnc_smokey_logs_button_text = irysnc_systemcoex_logs_module_layout["irysnc_smokey_logs_button"]['button_name_string']
    
    irysnc_smokey_logs_button_in_frame, irysnc_smokey_logs_button = Coex_tk.create_button_in_frame(BodyFrame, irysnc_smokey_logs_button_text, irysnc_smokey_logs_button_width, irysnc_smokey_logs_button_height, padx=widget_space_x/2, pady=widget_space_y/2)
    irysnc_smokey_logs_button_in_frame.grid(row=irysnc_smokey_logs_button_row, column=irysnc_smokey_logs_button_column, padx=widget_space_x*2, pady=widget_space_y*2)


    return ModuleFrame





def create_check_systemcoex_logs_module(   parent_frame, check_systemcoex_logs_layout, module_width, module_height, module_border_width, module_relief_style, font_type, font_size, 
                                            widget_space_x, widget_space_y  ):
    module_title_string = "Check Systemcoex Logs"

    Coex_tk = SystemCoex_Customized_Tkinter_Widgets.systemcoex_customized_tkinter_widgets(font_type, font_size, widget_space_x, widget_space_y)
    ModuleFrame, BodyFrame = Coex_tk.create_ModuleFrame_with_TitleLabel_and_BodyFrame(  parent_frame=parent_frame, width_in_pixel=module_width, height_in_pixel=module_height, border_width=module_border_width, relief_style=module_relief_style,
                                                                                        module_title_name=module_title_string)

    find_error_button_width, find_error_button_height = Calculate_SubFrame_width_and_height(BodyFrame, check_systemcoex_logs_layout, "find_errors_button", widget_space_x, widget_space_y)
    find_error_button_row, find_error_button_column = check_systemcoex_logs_layout["find_errors_button"]['row'], check_systemcoex_logs_layout["find_errors_button"]['column']
    find_error_button_text = check_systemcoex_logs_layout["find_errors_button"]['button_name_string']
    
    find_error_button_in_frame, find_error_button = Coex_tk.create_button_in_frame(BodyFrame, find_error_button_text, find_error_button_width, find_error_button_height, padx=widget_space_x/2, pady=widget_space_y/2)
    find_error_button_in_frame.grid(row=find_error_button_row, column=find_error_button_column, padx=widget_space_x/2, pady=widget_space_y/2)



    check_loadcycler_button_width, check_loadcycler_button_height = Calculate_SubFrame_width_and_height(BodyFrame, check_systemcoex_logs_layout, "check_loadcycler_button", widget_space_x, widget_space_y)
    check_loadcycler_button_row, check_loadcycler_button_column = check_systemcoex_logs_layout["check_loadcycler_button"]['row'], check_systemcoex_logs_layout["check_loadcycler_button"]['column']
    check_loadcycler_button_text = check_systemcoex_logs_layout["check_loadcycler_button"]['button_name_string']
    
    check_loadcycler_button_in_frame, check_loadcycler_button = Coex_tk.create_button_in_frame(BodyFrame, check_loadcycler_button_text, check_loadcycler_button_width, check_loadcycler_button_height, padx=widget_space_x/2, pady=widget_space_y/2)
    check_loadcycler_button_in_frame.grid(row=check_loadcycler_button_row, column=check_loadcycler_button_column, padx=widget_space_x/2, pady=widget_space_y/2)



    check_brownout_button_width, check_brownout_button_height = Calculate_SubFrame_width_and_height(BodyFrame, check_systemcoex_logs_layout, "check_brownout_button", widget_space_x, widget_space_y)
    check_brownout_button_row, check_brownout_button_column = check_systemcoex_logs_layout["check_brownout_button"]['row'], check_systemcoex_logs_layout["check_brownout_button"]['column']
    check_brownout_button_text = check_systemcoex_logs_layout["check_brownout_button"]['button_name_string']
    
    check_brownout_button_in_frame, check_brownout_button = Coex_tk.create_button_in_frame(BodyFrame, check_brownout_button_text, check_brownout_button_width, check_brownout_button_height, padx=widget_space_x/2, pady=widget_space_y/2)
    check_brownout_button_in_frame.grid(row=check_brownout_button_row, column=check_brownout_button_column, padx=widget_space_x/2, pady=widget_space_y/2)

    return ModuleFrame







def create_reboot_device_module(    parent_frame, reboot_device_module_layout, module_width, module_height, module_border_width, module_relief_style, font_type, font_size, 
                                    widget_space_x, widget_space_y):
    
    Coex_tk = SystemCoex_Customized_Tkinter_Widgets.systemcoex_customized_tkinter_widgets(font_type, font_size, widget_space_x, widget_space_y)
    ModuleFrame, BodyFrame = Coex_tk.create_ModuleFrame_with_TitleLabel_and_BodyFrame(  parent_frame=parent_frame, width_in_pixel=module_width, height_in_pixel=module_height, border_width=module_border_width, relief_style=module_relief_style)


    reboot_button_width, reboot_button_height = Calculate_SubFrame_width_and_height(BodyFrame, reboot_device_module_layout, "reboot_button", widget_space_x, widget_space_y)
    reboot_button_row, reboot_button_column = reboot_device_module_layout["reboot_button"]['row'], reboot_device_module_layout["reboot_button"]['column']
    reboot_button_text = reboot_device_module_layout["reboot_button"]['button_name_string']
    
    reboot_button_in_frame, reboot_button = Coex_tk.create_button_in_frame(BodyFrame, reboot_button_text, reboot_button_width, reboot_button_height, padx=widget_space_x/2, pady=widget_space_y/2)
    reboot_button_in_frame.grid(row=reboot_button_row, column=reboot_button_column, padx=widget_space_x/2, pady=widget_space_y/2)

    return ModuleFrame










def create_result_output_module(   parent_frame, module_width, module_height, module_border_width, module_relief_style, font_type, font_size, 
                            widget_space_x, widget_space_y):
    Coex_tk = SystemCoex_Customized_Tkinter_Widgets.systemcoex_customized_tkinter_widgets(font_type, font_size, widget_space_x, widget_space_y)
    ModuleFrame, BodyFrame = Coex_tk.create_ModuleFrame_with_TitleLabel_and_BodyFrame(  parent_frame=parent_frame, width_in_pixel=module_width, height_in_pixel=module_height, border_width=module_border_width, relief_style=module_relief_style)

    result_output_textbox_width = module_width - 2*module_border_width
    result_output_textbox_height = module_height - 2*module_border_width
    result_output_textbox_in_frame, result_output_textbox = Coex_tk.create_text_box_in_frame(BodyFrame, result_output_textbox_width, result_output_textbox_height, 
                                                                                             padx=widget_space_x/2, pady=widget_space_y/2)
    result_output_textbox_in_frame.grid()

    return ModuleFrame