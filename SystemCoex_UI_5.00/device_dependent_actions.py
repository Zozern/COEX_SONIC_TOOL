import paramiko
import re
import json
import subprocess,shlex,sys,os
from pathlib import Path

# with open()



class device_dependent_actions():
    def __init__(self,sconn, device_default_cmd:dict):
        
        self.sconn = sconn 
        self.device_default_cmd = device_default_cmd


    def send_command_to_device(self,cmd,sconn=False):
        """
        Function:   send command to device and return the output of this command
        Usage:      self.send_command_to_device(command)
        Return:     the output of command
        """
        if sconn:            
            self.sconn = sconn

        if not self.sconn.get_transport().is_active():
            return False
        try:
            stdin_, stdout_, stderr_ = self.sconn.exec_command(cmd)
            exitcode = stdout_.channel.recv_exit_status()
        except:
            exitcode = 1
        if exitcode != 0:
            return False
        result = stdout_.readlines()
        return result

    def __is_config_josn_exist(self) -> bool:
        """
        Function:   judge if config.json file is exist
        Usage:      self.__is_config_josn_exist()
        Return:     True or False
        """

        cat_config_json_cmd =  self.device_default_cmd["cat_config_json_defalut_cmd"]
        stdin_, stdout_, stderr_ = self.sconn.exec_command(cat_config_json_cmd)
        exitcode = stdout_.channel.recv_exit_status()
        if exitcode != 0:
            return False
        else:
            return True

    def get_ggtool_info(self) -> dict:
        """
        Function:   (1).send default command to read the gasgauge info
                    (2).store all of gasgauge key and value into a dictionary
        Usage:      self.get_ggtool_info()
        Return:     a dictionary inclue all of gasgauge key and corresponding value
        """

        cmd_result_dict = {}
        ggtool_cmd = self.device_default_cmd["ggtool_default_cmd"]
        for key in self.device_default_cmd["ggtool_keylist"]:
            cmd_result_dict[key] = ''
        ggtool_info = self.send_command_to_device(ggtool_cmd)
        if not ggtool_info:
            return cmd_result_dict
        for line in ggtool_info:
            key_match = re.search(r"\S{4}:\s+\S+,\s+\S+\s+(\S+)",line)
            value_match = re.search(r"\S{4}:\s+\S+,\s+(\S+)\s+\S+",line)
            if key_match and value_match:
                key = key_match.group(1)
                value = int(value_match.group(1))
                cmd_result_dict[key] = value
        return cmd_result_dict

    def get_c26tool_FwState(self) -> dict:
        """
        Function:   (1).send default command to read the c26tool FwState
                    (2).store FwState into dictionary
        Usage:      self.get_c26tool_FwState()
        Return:     a dictionary contains "FwState" key and value : cmd_result_dict["FwState"]
        """

        cmd_result_dict = {}
        cmd_result_dict["FwState"] = ""
        c26tool_command = self.device_default_cmd["c26tool_default_cmd"]
        c26tool_Fwstate = self.send_command_to_device(c26tool_command)
        if not c26tool_Fwstate:
            return cmd_result_dict
        for line in c26tool_Fwstate:
            cmd_result_dict["FwState"] = re.search(r'FwState\s+:\s+(.*)',line).group(1)
        return cmd_result_dict

    def get_boot_args_info(self) -> dict:
        """
        Function:   (1).send default command to read device boot-args
                    (2).store Boot_args into dictionary
        Usage:      self.get_boot_args_info()
        Return:     a dictionary contains "Boot_args" key and value : cmd_result_dict["Boot_args"]
        """

        cmd_result_dict = {}
        cmd_result_dict["Boot_args"] = ""
        boot_args_command = self.device_default_cmd["boot_args_default_cmd"]
        boot_args_info = self.send_command_to_device(boot_args_command)
        if not boot_args_info:
            return cmd_result_dict
        for line in boot_args_info:
            cmd_result_dict["Boot_args"] = re.search(r'boot-args\s+(.*)',line).group(1)
        return cmd_result_dict

    def get_IMU_calibration_info(self) -> dict:
        """
        Function:   (1).send default command to read device IMU calibration
                    (2).store IMU calibration into dictionary
        Usage:      self.get_IMU_calibration_info()
        Return:     a dictionary contains "IMU_Calibration" key and value : cmd_result_dict["IMU_Calibration"]
        """

        cmd_result_dict = {}
        cmd_result_dict["IMU_Calibration"] = ""
        IMU_cal_info_command = self.device_default_cmd["IMU_Calibration_info_default_cmd"]
        IMU_cal_info = self.send_command_to_device(IMU_cal_info_command)
        if not IMU_cal_info:
            return cmd_result_dict
        for line in IMU_cal_info:
            IMU_Calibration_data = line.split(" ")
        for axis_data in IMU_Calibration_data:
            if float(axis_data) !=  1:
                IMU_calibrated = "Yes"
            else:
                IMU_calibrated = "No"
                break
        cmd_result_dict["IMU_Calibration"] = IMU_calibrated
        return cmd_result_dict

    def get_Alert_calibration_info(self) -> dict:
        """
        Function:   (1).send default command to read device Alert calibration
                    (2).store Alert calibration into dictionary
        Usage:      self.get_Alert_calibration_info()
        Return:     a dictionary contains "Alert_Calibration" key and value : cmd_result_dict["Alert_Calibration"]
        """

        cmd_result_dict = {}
        cmd_result_dict["Alert_Calibration"] = ""
        Alert_cal_info_command = self.device_default_cmd["Alert_Calibration_info_default_cmd"]
        Alert_cal_info = self.send_command_to_device(Alert_cal_info_command)
        if not Alert_cal_info:
            return cmd_result_dict
        for alert_data in Alert_cal_info:
            if float(alert_data) != 0:
                Alert_calibrated = 'Yes'
            else:
                Alert_calibrated = 'No'
        cmd_result_dict["Alert_Calibration"] = Alert_calibrated
        return cmd_result_dict

    def get_device_code(self) -> dict:
        """
        Function:   (1).send default command to read device Code
                    (2).store device Code into dictionary
        Usage:      self.get_device_Code()
        Return:     a dictionary contains "Product_Code" key and value : cmd_result_dict["Product_Code"]
        """

        cmd_result_dict = {}
        cmd_result_dict["Product_Code"]= ""
        get_device_code_cmd = self.device_default_cmd["get_device_code_default_cmd"]
        device_code_info = self.send_command_to_device(get_device_code_cmd)
        if not device_code_info:
            return  cmd_result_dict
        for line in device_code_info:
            device_code  = line.rstrip('\n')
        cmd_result_dict["Product_Code"]= device_code

        return cmd_result_dict

    def get_device_sn(self) -> dict:
        """
        Function:   (1).send default command to read device sn
                    (2).store device sn into dictionary
        Usage:      self.get_device_sn()
        Return:     a dictionary contains "SN" key and value : cmd_result_dict["SN"]
        """

        cmd_result_dict = {}
        cmd_result_dict["SN"] = ""
        get_device_sn_cmd = self.device_default_cmd["get_device_sn_default_cmd"]
        device_sn_info = self.send_command_to_device(get_device_sn_cmd)
        if not device_sn_info:
            return  cmd_result_dict
        for line in device_sn_info:
            device_sn  = line.rstrip('\n')
        cmd_result_dict["SN"]= device_sn
        return cmd_result_dict

    def get_root_version(self) -> dict:
        """
        Function:   (1).send default command to read device root version
                    (2).store RootVersion into dictionary
        Usage:      self.get_root_version()
        Return:     a dictionary contains "RootVersion" key and value : cmd_result_dict["RootVersion"]
        """

        cmd_result_dict = {}
        cmd_result_dict["RootVersion"] = ""
        cat_root_version_command = self.device_default_cmd["cat_root_version_txt"]
        RootVersion_result = self.send_command_to_device(cat_root_version_command)
        if not RootVersion_result:
            return cmd_result_dict
        for line in RootVersion_result:
            root_version = re.search(rf",(root\S+?),", line).group(1)
        cmd_result_dict["RootVersion"] = root_version
        return cmd_result_dict

    def get_device_bundle_version(self) -> dict:
        """
        Function:   (1).send default command to read device bundle version
                    (2).store BundleVersion into dictionary
        Usage:      self.get_device_bundle_version()
        Return:     a dictionary contains "BundleVersion" key and value : cmd_result_dict["BundleVersion"]
        """

        cmd_result_dict = {}
        cmd_result_dict["BundleVersion"] = ""
        get_bundle_info_command = self.device_default_cmd["bundle_info_default_default_cmd"]
        BundleVersion_result = self.send_command_to_device(get_bundle_info_command)
        
        if not BundleVersion_result:
            return cmd_result_dict
        for line in BundleVersion_result:
            bundle_version = line

        cmd_result_dict["BundleVersion"] = bundle_version
        return cmd_result_dict


    def get_device_cfg(self,device_code) -> dict:
        """
        Function:   (1).send default command to read device CFG
                    (2).store device CFG into dictionary
        Usage:      self.get_device_CFG(device_code)
        Return:     a dictionary contains "Config" key and value : cmd_result_dict["Config"]
        """

        cmd_result_dict = {}
        cmd_result_dict["Config"] = ""
        self.config_json = self.__is_config_josn_exist()
        if self.config_json:
            cat_config_json_cmd =  self.device_default_cmd["cat_config_json_defalut_cmd"]
            config_json_content = self.send_command_to_device(cat_config_json_cmd)
            if not config_json_content:
                return cmd_result_dict
            for line in config_json_content:
                device_cfg_match = re.search(rf"FATP_CFG\":\"(.*)\"", line)
                if device_cfg_match:
                    device_cfg = device_cfg_match.group(1)
        elif self.device_default_cmd["ProductCodeType"][device_code] == "N14z":
            device_cfg = "confid.json absent"
        elif self.device_default_cmd["ProductCodeType"][device_code] == "N14y":
            N14y_get_cfg_cmd =  self.device_default_cmd["N14y_get_cfg_default_cmd"]
            get_n14y_cfg_info = self.send_command_to_device(N14y_get_cfg_cmd)
            if not get_n14y_cfg_info:
                return cmd_result_dict
            for line in get_n14y_cfg_info:
                device_cfg_match = re.match(rf"CFG#,STR,(.+)\s*", line)
                if device_cfg_match:
                    device_cfg = device_cfg_match.group(1)
        cmd_result_dict["Config"] = device_cfg
        return cmd_result_dict

    def get_device_region_according_to_cfg(self,device_cfg):
        """
        Function:   (1).send default command to read device CFG
                    (2).store device CFG into dictionary
        Usage:      self.get_device_CFG()
        Return:     a dictionary contains "Config" key and value : cmd_result_dict["Config"]
        """

        cmd_result_dict = {}
        cmd_result_dict["Config"] = ""
        CFG_match = re.search('\S+-\S+-\S+', device_cfg)
        if CFG_match:
            bb_region = re.search(rf"^\S\S(\S).*", device_cfg).group(1)
            if bb_region == "W":
                bb_region = "ROW"
            elif bb_region == "X":
                bb_region = "X"
            elif bb_region == "N":
                bb_region = "NA"
        else:
            bb_region = device_cfg
        cmd_result_dict["BB_Region"] = bb_region
        return cmd_result_dict
    


    def change_boot_args(self,station,device_code,device_cfg,sconn=False):
        """
        Function:   (1) According to device product code, change corresponding boot-args
                    (2) read boot-args to judge if boot-args correct
        Usage:      self.change_boot_args(device_code,device_cfg)
        Return:     the command and result for change boot-args
        """

        is_pf_device_match = False
        pf_device_match = re.search(r"\S{3}-\S{4}(\S)-.*",device_cfg)
        if pf_device_match:
            if pf_device_match.group(1) == "f":
                is_pf_device_match = True
        if not is_pf_device_match:
            boot_args_none = self.device_default_cmd["boot_args_none_command"][device_code]
        else:
            boot_args_none = self.device_default_cmd["boot_args_none_command"][device_code].replace(self.device_default_cmd["pf_unit_delete_parameter"],'')
        
        if station != "none":
            change_boot_args_command = "nvram boot-args='%s astro=%s'"%(boot_args_none,station)
        else:
            change_boot_args_command = "nvram boot-args='%s'"%boot_args_none
        
        print(change_boot_args_command)

        self.send_command_to_device(change_boot_args_command, sconn)
        boot_args_info = self.get_boot_args_info()
        change_boot_args_result = change_boot_args_command+'\n'
        if boot_args_info["Boot_args"] == re.search(r"=\'(.*)\'",change_boot_args_command).group(1):
            change_boot_args_result += change_boot_args_result + "Change boot-args success"
        else:
            change_boot_args_result += change_boot_args_result + "Change boot-args Fail"
        return change_boot_args_result

    def __delete_coex_log(self,delete_file_path, sconn=False):
        """
        Function:   delete coex log according to the input file path
        Usage:      self.__delete_coex_log(delete_file_path)
        Return:     the command to delete 
        """

        delete_cmd = "rm -rf %s"%delete_file_path
        self.send_command_to_device(delete_cmd, sconn)
        print(delete_cmd)
        return delete_cmd

    def delete_systemcoex_log_by_station(self,delete_station, sconn=False):
        """
        Function:   (1) Judge if the file need to be deleted depend on the delete station
                    (2) delete the file and return the command of delete file
        Usage:      self.delete_station_systemcoex_log(delete_station)
        Return:     the command of deleting file
        """

        astro_files = self.send_command_to_device(f"ls {self.device_default_cmd['Astro_default_path']}", sconn)
        if not astro_files:
                return False
        delete_command = ""
        for file in astro_files:
            for delete_key in self.device_default_cmd["systemcoex_astro_log_structure"][delete_station]:
                if delete_key in file and "config.json" not in file:
                    delete_command += self.__delete_coex_log(self.device_default_cmd["Astro_default_path"]+file, sconn)
        
        if delete_station == "darkarm" or delete_station=="all":
            for smokey_delete_path in self.device_default_cmd["systemcoex_smokey_log_structure"]:
                delete_command += self.__delete_coex_log(smokey_delete_path, sconn)
        elif delete_station == 'coal':
            delete_command += self.__delete_coex_log(self.device_default_cmd["Astro_default_path"]+"coal_Dali_*", sconn)

        return delete_command

    def split_station_file_list(self):
        cmd_result_dict = {}
        astro_file_list = self.send_command_to_device(f"ls -t {self.device_default_cmd['Astro_default_path']}")

        station_start_flag = 0
        station = "None"

        for file in astro_file_list:
            if ".astro" in file:
                if station_start_flag == 0:
                    station = re.search('(.*).astro',file).group(1)
                    station_start_flag = 1
                    cmd_result_dict[station] = []
                else:
                    print(f"{station} systemcoex log error , please check!")
                    del cmd_result_dict[station]
                    station = re.search('(.*).astro',file).group(1)
                    cmd_result_dict[station] = []
                    print(f"{station} start collect")
            elif f"{station}_start.txt" in file:
                cmd_result_dict[station].append(self.device_default_cmd['Astro_default_path']+file.rstrip('\n'))
                station_start_flag = 0
            elif "grapenfcsota" in file:
                cmd_result_dict[station] = [f"{self.device_default_cmd['Astro_default_path']}/grapenfcsota"]
            if station_start_flag == 1:
                cmd_result_dict[station].append(self.device_default_cmd['Astro_default_path']+file.rstrip('\n'))

        # print(cmd_result_dict)
        return cmd_result_dict