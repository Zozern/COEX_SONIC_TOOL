import sys,subprocess,warnings,paramiko,shlex,os
import json
from time import sleep
class host_dependent_actions():
    def __init__(self) -> None:
        pass

    def enable_tcprelay(self, offset, port):
        """
        Basically run this!:  /usr/local/bin/tcprelay --portoffset 10000 873 22 23 2>/dev/null &
        """
        cmd = shlex.split(r"/usr/local/bin/tcprelay --portoffset %s %s" % (offset, port))
        print(cmd)
        with open(os.devnull, "w") as fnull:
            tcprelay_subprocess = subprocess.Popen(cmd, stdout=fnull, stderr=fnull)

        # log.info("TCPRELAYPid: %s" % tcprelay_subprocess.pid)
        return tcprelay_subprocess

    def disable_tcprelay(self):
        cmd = 'killall -9 tcprelay'
        os.system(cmd)


    def create_ssh_to_dut(self):
        with warnings.catch_warnings():
            # ignore ElipticCurve warining
            warnings.simplefilter("ignore")
            sshconnect = paramiko.SSHClient()
            sshconnect.load_system_host_keys()
            sshconnect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        return sshconnect

    def ssh_connect_to_dut(self, sshconnect, tcprelay_port):
        sleep(0.5)
        if self.is_unit_connect():
            ssh_port = tcprelay_port + 22
            sshconnect.connect("localhost", ssh_port, username="root", password="alpine")
        else:
            print('usbterm detect no connected device')


    def is_unit_connect(self) -> bool:
        """
        Function:   Check if device connect
        Usage:      
        Return:     the result of command "usbterm -list" 
        """
        usbterm_check_cmd = "/usr/local/bin/usbterm -list"
        sys.stdout.flush()
        p = subprocess.Popen(   usbterm_check_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT   )
        if not p.stdout.readlines():
            return False
        else:
            return True

    def rsync_device_file_2_host(self,src_path,tar_path,retries = 5):
        """
        Function:   (1) open tcprelay 
                    (2) rsync log from device (src_path) to host (tar_path)
        Usage:      self.rsync_device_file_2_host(src_path,tar_path,retries)
        """

        portoffset = 10873
        rsync_result = []
        remote_src_item = "rsync://root@localhost:%s/root/%s" % (str(portoffset + 873), src_path)
        rsync_command = "RSYNC_PASSWORD=alpine rsync -av %s %s" % (remote_src_item,tar_path)
        tcprelay_cmd = "/usr/local/bin/tcprelay --portoffset %s ssh rsync" % portoffset
        os.system(f'mkdir -p {tar_path}')
        tcprelay_process  =  subprocess.Popen(shlex.split(tcprelay_cmd),stdout=False)
        for i in range(retries):
            print("Retry:",retries)
            # rsync_process = subprocess.run(shlex.split(rsync_command),capture_output=True)
            # rsync_process = os.system(rsync_command)
            rsync_process = os.popen(rsync_command)
            rsync_result += rsync_process.readlines()
            if rsync_process == 0:
                break
            else:
                continue
        tcprelay_process.terminate()
        return rsync_result

    def rsync_host_file_2_device(self,src_path,tar_path,retries = 5):
        """
        Function:   (1) open tcprelay 
                    (2) rsync log from host (src_path) to device (tar_path)
        Usage:      self.rsync_host_file_2_device(src_path,tar_path,retries)
        """

        portoffset = 10873
        remote_tar_item = "rsync://root@localhost:%s/root/%s" % (str(portoffset + 873), tar_path)
        rsync_command = "RSYNC_PASSWORD=alpine rsync -av %s %s" % (src_path,remote_tar_item)
        tcprelay_cmd = "/usr/local/bin/tcprelay --portoffset %s ssh rsync" % portoffset
        tcprelay_process  =  subprocess.Popen(shlex.split(tcprelay_cmd),stdout=False)
        rsync_result = []
        for i in range(retries):
            print("Retry:",retries)
            # rsync_process = subprocess.run(shlex.split(rsync_command),capture_output=True)
            # rsync_process = os.system(rsync_command)
            rsync_process = os.popen(rsync_command)
            rsync_result += rsync_process.readlines()
            # print("Rsync_result:",rsync_result)
            if rsync_process == 0:
                break
            else:
                continue
        tcprelay_process.terminate()
        
        return rsync_result

    def load_json_file(self, json_file_path):
        with open (json_file_path) as f:
            json_data_dict = json.load(f)
        return json_data_dict