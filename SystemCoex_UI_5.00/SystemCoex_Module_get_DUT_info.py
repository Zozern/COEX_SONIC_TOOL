import device_dependent_actions  
import SystemCoex_host_dependent_actions 
from SystemCoex_Customized_Tkinter_Widgets import systemcoex_customized_tkinter_widgets
import tkinter as tk
from time import sleep
from datetime import datetime

class systemcoex_get_DUT_attributes_module():
    def __init__(self, window:tk.Tk, device_information_module_layout:dict, device_default_cmd):

        self.window = window
        # self.device_default_cmd = device_default_cmd
        self.unit_info_dict = {}
        self.device_information_module_layout = device_information_module_layout

        
        self.SSHactive = False
        self.DEFAULT_SSHPORT = 18000
        self.reboot_flag = False

        self.host_action = SystemCoex_host_dependent_actions.host_dependent_actions()
        self.sshconnect = self.host_action.create_ssh_to_dut()

        self.Coex_DUT = device_dependent_actions.device_dependent_actions(self.sshconnect, device_default_cmd)
        # self.tcprelay_subprocess=self.host_action.enable_tcprelay(self.DEFAULT_SSHPORT, "873 22 23")

    def create_module_frame(self, parent_frame, font_type, font_size, widget_space_x, widget_space_y, width_in_pixel, height_in_pixel, border_width, relief_style ):
        coex_tk = systemcoex_customized_tkinter_widgets(font_type, font_size, widget_space_x, widget_space_y)
        # module_frame , body_frame = coex_tk.create_ModuleFrame_with_TitleLabel_and_BodyFrame(   parent_frame, width_in_pixel, height_in_pixel, border_width, relief_style, 
        #                                                                                         module_title_name="Device Information")
        
        module_frame , body_frame = coex_tk.create_ModuleLabelFrame(   parent_frame, width_in_pixel, height_in_pixel, border_width, relief_style, 
                                                                                                module_title_name="Device Information")


        max_keyname_string_length = max(len(keyname_string) for keyname_string in self.device_information_module_layout)
        key_name_label_width_in_pixel = max_keyname_string_length * font_size * 0.5

        for key_name_string in self.device_information_module_layout:
            
            KeyLabel_ValueLabel_frame_width, KeyLabel_ValueLabel_frame_height = coex_tk.Calculate_SubFrame_width_and_height(body_frame, self.device_information_module_layout, key_name_string, widget_space_x/2, widget_space_y/2)



            KeyLabel_ValueLabel_frame, value_StringVar = coex_tk.create_KeyValueLabelPair_frame(    frame=body_frame, 
                                                                                                    frame_width_in_pixel=KeyLabel_ValueLabel_frame_width, 
                                                                                                    frame_height_in_pixel=KeyLabel_ValueLabel_frame_height, 
                                                                                                    key_name=key_name_string, 
                                                                                                    key_label_width_in_pixel=key_name_label_width_in_pixel,
                                                                                                    copy_button_exist=self.device_information_module_layout[key_name_string]['copy_button']
                                                                                                )

            KeyLabel_ValueLabel_frame.grid( row=self.device_information_module_layout[key_name_string]['row'], 
                                            column=self.device_information_module_layout[key_name_string]['column'],
                                            columnspan=self.device_information_module_layout[key_name_string]['columnspan'], 
                                            padx=widget_space_x/2, pady=widget_space_y/2, sticky='w')
            
            self.unit_info_dict[key_name_string] = value_StringVar

        return module_frame



    def init_unit_info_dict(self):
        self.unit_info_dict["Connection Status"].set( 'disconnected' )
        for key in self.unit_info_dict.keys():
            if key != 'Connection Status':
                self.unit_info_dict[key].set('')
    

    def __wait_for_device_reboot(self):


        if self.reboot_flag:

            print('Rebooting device. Waiting for usbterm connection break.')
            
            sleeptime = 0
            timeout_time = 15
            while self.host_action.is_unit_connect():
                sleep(1)
                sleeptime += 1
                print(f'sleep {sleeptime} ...')
                
                if not self.host_action.is_unit_connect():
                    print('usbterm connection break!')
                    break
                elif sleeptime > timeout_time:
                    print('timeout')
                    break

            self.reboot_flag = False


    def __establish_ssh_connection_to_dut(self):
        try:
            print(f'start to establisth SSH connection, sshport={self.DEFAULT_SSHPORT}')
            # self.host_action.disable_tcprelay()
            self.tcprelay_subprocess = self.host_action.enable_tcprelay(self.DEFAULT_SSHPORT, "873 22 23")
            self.host_action.ssh_connect_to_dut(self.sshconnect, self.DEFAULT_SSHPORT)
            self.SSHactive = self.sshconnect.get_transport().is_active()
        except:
            print("Failed to establish SSH connection. Unit not connected yet!")

        if self.SSHactive == True:
            print('Success! SSH connection eastablished')

    def __read_constant_attributes(self):
        if self.SSHactive == True:
             
            self.unit_info_dict['SN'].set( self.Coex_DUT.get_device_sn()['SN'] )
            self.unit_info_dict['Bundle Overlay'].set( self.Coex_DUT.get_device_bundle_version()['BundleVersion'].rstrip('\n'))
            self.unit_info_dict['Product Code'].set( self.Coex_DUT.get_device_code()['Product_Code'] )
            self.unit_info_dict['Config'].set( self.Coex_DUT.get_device_cfg(self.unit_info_dict['Product Code'].get())['Config'] )
            self.unit_info_dict['BB Region'].set( self.Coex_DUT.get_device_region_according_to_cfg(self.unit_info_dict['Config'].get())['BB_Region'] )
            self.unit_info_dict['IMU Calibration'].set(self.Coex_DUT.get_IMU_calibration_info()["IMU_Calibration"])
            self.unit_info_dict['Alert Calibration'].set(self.Coex_DUT.get_Alert_calibration_info()["Alert_Calibration"])

        else:
            self.init_unit_info_dict()


    def __read_dynamic_attributes(self):
        if self.SSHactive == True:
            ggtool_info = self.Coex_DUT.get_ggtool_info()
            self.unit_info_dict['State Of Charge'].set( ggtool_info["StateOfCharge"] )
            self.unit_info_dict['AverageCurrent'].set( ggtool_info["AverageCurrent"] )
            self.unit_info_dict['AveragePower'].set( ggtool_info['AveragePower'] )
            self.unit_info_dict["Temperature"].set( ggtool_info["Temperature"] )
            self.unit_info_dict["Voltage"].set( ggtool_info["Voltage"] )

            self.unit_info_dict["Root version"].set( self.Coex_DUT.get_root_version()['RootVersion'])
            self.unit_info_dict["Boot-args"].set( self.Coex_DUT.get_boot_args_info()["Boot_args"] )
            self.unit_info_dict["Puck FwState"].set( self.Coex_DUT.get_c26tool_FwState()["FwState"] )

        else:
            self.init_unit_info_dict()

    def __is_SSHactive(self, sshconnect):
        if sshconnect.get_transport() == None:
            SSHactive = False
        else:
            if sshconnect.get_transport().is_active():
                SSHactive = True
            else:
                SSHactive = False         
        return SSHactive


    def update_DUT_attributes(self):

        self.__wait_for_device_reboot()

        self.SSHactive = self.__is_SSHactive(self.sshconnect)
        self.unit_info_dict["Connection Status"].set('connected' if self.SSHactive else 'disconnected')
        
        # print(f"{datetime.now()}: usbterm connection:{self.host_action.is_unit_connect()}\n SSHactive:{self.SSHactive}")

        if self.host_action.is_unit_connect()==True and self.SSHactive==False:
            self.__establish_ssh_connection_to_dut()
            self.__read_constant_attributes()
        elif self.host_action.is_unit_connect()==True and self.SSHactive==True:
            self.__read_dynamic_attributes()
        else:
            self.init_unit_info_dict()


        self.window.after(100, self.update_DUT_attributes)