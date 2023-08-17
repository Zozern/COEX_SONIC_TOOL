import os
import re
import json

# ======================================================================================================
# Function: copy the text to clipboard 
def copy_to_clipboard(text):
	os.system(f'echo {text}|pbcopy')
	pass

def load_json_file(json_file_path):
	with open (json_file_path) as f:
		json_data_dict = json.load(f)
	return json_data_dict


def Calculate_SubFrame_width_and_height(parent_frame, parent_frame_layout:dict, subframe_name, padx, pady):

    subfrmae_relative_width_string     = parent_frame_layout[subframe_name]['relative_width']
    subfrmae_relative_height_string    = parent_frame_layout[subframe_name]['relative_height']

    subfrmae_relative_width = int(re.search(r"(\d+)\/\d+",subfrmae_relative_width_string).group(1)) / int(re.search(r"\d+\/(\d+)",subfrmae_relative_width_string).group(1))
    subfrmae_relative_height = int(re.search(r"(\d+)\/\d+",subfrmae_relative_height_string).group(1)) / int(re.search(r"\d+\/(\d+)",subfrmae_relative_height_string).group(1))

    subframe_width  = int(  (parent_frame['width'] -  padx*2) * subfrmae_relative_width   - padx*2  )
    subframe_height = int(  (parent_frame['height'] - pady*2) * subfrmae_relative_height  - pady*2  )

    return subframe_width, subframe_height