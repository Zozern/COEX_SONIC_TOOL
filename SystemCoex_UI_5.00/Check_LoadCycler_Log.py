import re, os
import matplotlib.pyplot as plt
import device_dependent_actions

class systemcoex_loadcycler_log():
	def __init__(self, sshconnect, device_default_cmd):
		pass
		self.dda = device_dependent_actions.device_dependent_actions(sshconnect, device_default_cmd)

	def __find_index_in_comma_separated_TextLine(self,comma_separated_TestLine):

		index_dict = {}
		comma_splited_list = comma_separated_TestLine.split(',')
		for i in range(len(comma_splited_list)):
			index_dict[comma_splited_list[i]] = i
		return index_dict

	def __plot_loadCycler_result(self,loadcycler_key_dict,key_list):

		
		fig = plt.figure()
		plt.suptitle('Loadcycler')
		axes_list =[]
		x_index = []

		for i in range(len(key_list)):
			index = int(f'{len(key_list)}1{i+1}')
			temp_ax = fig.add_subplot(index)
			temp_ax.plot(loadcycler_key_dict['DeltaTime'], loadcycler_key_dict[key_list[i]])
			temp_ax.set(xlabel = 'DeltaTime', ylabel = key_list[i])
			axes_list.append(temp_ax)

		for i in range(len(loadcycler_key_dict['GG_StateOfCharge'])-4):
			if loadcycler_key_dict['GG_StateOfCharge'][i+4] > loadcycler_key_dict['GG_StateOfCharge'][i] and loadcycler_key_dict['Mode'][i] == 'Discharge':
				if len(x_index) ==0:
					x_index.append(loadcycler_key_dict['DeltaTime'][i])
				else:
					if int(loadcycler_key_dict['DeltaTime'][i]) > int(x_index[len(x_index)-1])+300:
						x_index.append(loadcycler_key_dict['DeltaTime'][i])

		for ax in axes_list:
			for i in x_index:
				ax.axvline(x=i,color = 'red')

		fig.subplots_adjust(hspace=0)
		plt.show()


	def find_loadCycle_csv_file_in_device(self):

		try:
			coal_station_file_list = self.dda.split_station_file_list()["coal"]
			for file in coal_station_file_list:
				if "loadCycler_" in file and ".csv" in file:
					loadcycler_csv_file = file
					return loadcycler_csv_file
		except:
			# print('failed to find coal_loadCycler.csv log in conencted device')
			return None
			

	def parse_loadCycle_csv_file(self, loadcycler_csv_file):
		loadcycler_csv_dict = {}
		loadCycle_csv_content = self.dda.send_command_to_device(f"cat {loadcycler_csv_file}")
		for i in range(len(loadCycle_csv_content)):
			line_comma_splited_list = loadCycle_csv_content[i].split(',')
			title_match = re.search('Mode', loadCycle_csv_content[i])
			if title_match:
				index_dict = self.__find_index_in_comma_separated_TextLine(loadCycle_csv_content[i])
				for key in index_dict.keys():
					loadcycler_csv_dict[key]=[]
			else:
				for key in index_dict.keys():
					try:                
						line_comma_splited_list[index_dict[key]] = float(line_comma_splited_list[index_dict[key]])
					except:
						pass
					loadcycler_csv_dict[key].append(line_comma_splited_list[index_dict[key]])

		self.__plot_loadCycler_result(loadcycler_csv_dict,loadcycler_select_key_list)

