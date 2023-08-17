import tkinter as tk
import os, re
from tkinter import XView, filedialog, ttk


class systemcoex_customized_tkinter_widgets():

    def __init__(self, font_type, font_size, widget_space_x, widget_space_y):
        self.font_type = font_type
        self.font_size = font_size
        self.widget_space_x = widget_space_x
        self.widget_space_y = widget_space_y


    def __create_frame_with_single_cell(self, parent_frame, width_in_pixel, height_in_pixel, border_width=False, relief_style=False) -> tk.Frame:
        # create a frame containing only one grid cell at row=0, column=0
        # resize this grid cell according to fit the frame width and frame hegiht
        # return this tkinter frame widget
        
        single_cell_frame = tk.Frame(parent_frame, width=width_in_pixel, height=height_in_pixel, padx=self.widget_space_x/2, pady=self.widget_space_y/2,)
        single_cell_frame.grid_propagate(0)
        
        if border_width:
            single_cell_frame['bd'] = border_width
        if relief_style:
            single_cell_frame['relief'] = relief_style

        single_cell_frame.rowconfigure(0, minsize=single_cell_frame['height'] - single_cell_frame['pady']*2 - single_cell_frame['bd']*2)


        single_cell_frame.columnconfigure(0, minsize=single_cell_frame['width'] - single_cell_frame['padx']*2 - single_cell_frame['bd']*2)
        
        return single_cell_frame


    def create_button_in_frame(self, parent_frame, button_name, width_in_pixel, height_in_pixel, padx=False, pady=False, font_type=False, font_size=False,  button_action=False) -> tk.Frame:
        # create a frame containing only a tkinter button widget
        # size of the button will be streched to fit the size of this frame created
        # return this tkinter frame widget
        button_frame = self.__create_frame_with_single_cell(parent_frame, width_in_pixel, height_in_pixel)

        button = tk.Button(button_frame, text=button_name, font=(self.font_type, self.font_size), padx=padx, pady=pady)
        button.grid(sticky=tk.W+tk.E+tk.N+tk.S)

        if button_action:
            button['command'] = button_action

        if padx:
            button['padx'] = padx
        if pady:
            button['pady'] = pady

        if font_type and not font_size:
            button['font'] = (font_type, self.font_size)
        elif not font_type and font_size:
            button['font'] = (self.font_type, font_size)
        elif font_type and font_size:
            button['font'] = (self.font_type, self.font_size)
            
        return button_frame, button

    def create_label_in_frame(self, parent_frame, textvariable, width_in_pixel, height_in_pixel, disable_wrap=False, padx=False, pady=False, font_type=False, font_size=False, border_width=False, relief_style=False) -> tk.Frame:
        # create a frame containing only a tkinter label widget
        # size of the label will be streched to fit the size of this frame created
        # return this tkinter frame widget and the label widget 
    

        label_frame = self.__create_frame_with_single_cell(parent_frame, width_in_pixel, height_in_pixel)

        label = tk.Label(   label_frame, textvariable=textvariable, font=(self.font_type, self.font_size), anchor='w', justify='left')
        label.grid(sticky=tk.W+tk.E+tk.N+tk.S)


        if disable_wrap:
            pass
        else:
            label['wraplength'] = (width_in_pixel-padx*2)

        if padx:
            label['padx'] = padx
        if pady:
            label['pady'] = pady

        label['font'] = (font_type if font_type else self.font_type, font_size if font_size else self.font_size)


        if border_width:
            label['bd'] = border_width
        if relief_style:
            label['relief'] = relief_style


        return label_frame, label



    def create_Entry_in_frame(self, parent_frame, width_in_pixel, height_in_pixel, font_type=False, font_size=False):
        # create a frame containing only a tkinter Entry widget
        # size of the Entry will be streched to fit the size of this frame created
        # return this entry_box_frame and the text entered in the entry box
        
        Entry_box_frame = self.__create_frame_with_single_cell(parent_frame, width_in_pixel, height_in_pixel)

        Entry_box_text = tk.Entry(Entry_box_frame, font=(self.font_type, self.font_size))
        Entry_box_text.grid(column=0, row=0, sticky=tk.W+tk.E+tk.N+tk.S)


        if font_type and not font_size:
            Entry_box_text['font'] = (font_type, self.font_size)
        elif not font_type and font_size:
            Entry_box_text['font'] = (self.font_type, font_size)
        elif font_type and font_size:
            Entry_box_text['font'] = (self.font_type, self.font_size)

        return Entry_box_frame, Entry_box_text


    def create_combobox_in_frame(self, parent_frame, width_in_pixel, height_in_pixel, combobox_value=False, font_type=False, font_size=False):
        # create a frame containing only a ttk combobox widget
        # return this combobox_frame and the combobox widget

        combobox_frame = self.__create_frame_with_single_cell(parent_frame, width_in_pixel, height_in_pixel)


        combobox = ttk.Combobox(combobox_frame, font=(self.font_type, self.font_size), justify=tk.LEFT)
        combobox.grid(sticky=tk.W+tk.E)
        combobox['width']=int(width_in_pixel/self.font_size*1.2)


        if font_type and not font_size:
            combobox['font'] = (font_type, self.font_size)
        elif not font_type and font_size:
            combobox['font'] = (self.font_type, font_size)
        elif font_type and font_size:
            combobox['font'] = (self.font_type, self.font_size)
        if combobox_value:
            combobox['value'] = combobox_value

        return combobox_frame, combobox




    def create_text_box_in_frame(self, parent_frame, width_in_pixel, height_in_pixel, padx=False, pady=False, font_type=False, font_size=False, border_width=False, relief_sytle=False):
        # create a frame containing only a tkinter textbox widget
        # size of the textbox will be streched to fit the size of this frame created
        # return this text_box_frame and the textbox widget
        text_box_frame = tk.Frame(parent_frame, width=width_in_pixel, height=height_in_pixel)
        text_box_frame.grid_propagate(0)
        if border_width:
            text_box_frame['bd'] = border_width
            if relief_sytle:
                text_box_frame['relief'] = relief_sytle

        sbar_frame_width = width_in_pixel*(0.03) - text_box_frame['bd']*2 
        sbar_frame_height = height_in_pixel - text_box_frame['bd']*2
        sbar_frame = self.__create_frame_with_single_cell(text_box_frame, sbar_frame_width, sbar_frame_height)
        sbar_frame.grid(row=0, column=1)

        sbar1= tk.Scrollbar(sbar_frame)
        sbar1.grid(sticky=tk.W+tk.E+tk.N+tk.S)

        text_frame_width = width_in_pixel*(0.97) - text_box_frame['bd']*2
        text_frame_height = height_in_pixel - text_box_frame['bd']*2
        text_frame = self.__create_frame_with_single_cell(text_box_frame, text_frame_width, text_frame_height)
        text_frame.grid(row=0, column=0)

        text_box = tk.Text(text_frame, font=(self.font_type, self.font_size), yscrollcommand=sbar1.set, padx=padx, pady=pady )
        
        if padx:
            text_box['padx'] = padx
        if pady:
            text_box['pady'] = pady
        
        if font_type and not font_size:
            text_box['font'] = (font_type, self.font_size)
        elif not font_type and font_size:
            text_box['font'] = (self.font_type, font_size)
        elif font_type and font_size:
            text_box['font'] = (self.font_type, self.font_size)

        text_box['height'] = int((text_frame_height - padx*2) / (font_size * 1.1)) if font_size else int((text_frame_height - padx*2) / (self.font_size * 1.1))
        text_box.insert('insert','hello world\n'*100)
        text_box.grid(sticky=tk.W+tk.E+tk.N+tk.S)

        sbar1.config(command=text_box.yview)



        return text_box_frame, text_box
        




    def Calculate_SubFrame_width_and_height(self, parent_frame, parent_frame_layout:dict, subframe_name, padx, pady):

        subfrmae_relative_width_string     = parent_frame_layout[subframe_name]['relative_width']
        subfrmae_relative_height_string    = parent_frame_layout[subframe_name]['relative_height']

        subfrmae_relative_width = int(re.search(r"(\d+)\/\d+",subfrmae_relative_width_string).group(1)) / int(re.search(r"\d+\/(\d+)",subfrmae_relative_width_string).group(1))
        subfrmae_relative_height = int(re.search(r"(\d+)\/\d+",subfrmae_relative_height_string).group(1)) / int(re.search(r"\d+\/(\d+)",subfrmae_relative_height_string).group(1))

        subframe_width  = int(  (parent_frame['width'] - parent_frame['bd']*2 - padx*2) * subfrmae_relative_width   - padx*2  )
        subframe_height = int(  (parent_frame['height'] - parent_frame['bd']*2 - pady*2) * subfrmae_relative_height  - pady*2  )
    

        return subframe_width, subframe_height






    # ==================================================================================================================================================================
    def create_ModuleFrame_with_TitleLabel_and_BodyFrame(   self, parent_frame, width_in_pixel, height_in_pixel, border_width, relief_style, 
                                                            module_title_name=False, module_title_font_size=False, module_title_height_in_pixel=False) -> tk.Frame:
        # create a frame that consists of    (1) an optional module_title frame containing a label widget stating the systemcoex module title 
        #                                    (2) an empty module_body frame which is to be filled with customized tkinter widget
        # return the ModuleFrame and the BodyFrame

        #  ---- ModuleFrame ----------------------------------------------------------------------------------------------
        # |  ----------------------                                                                                       |
        # | | optional Title Label |                                                                                      |
        # |  ----------------------                                                                                       |
        # |  ---- BodyFrame --------------------------------------------------------------------------------------------  |
        # | |                                                                                                           | |
        # | |                                                                                                           | | 
        # | |                                                                                                           | | 
        # | |                                                                                                           | | 
        # | |                                                                                                           | | 
        # | |                                                                                                           | | 
        # | |                                                                                                           | | 
        # |  -----------------------------------------------------------------------------------------------------------  | 
        #  ---------------------------------------------------------------------------------------------------------------



        ModuleFrame = tk.Frame( parent_frame, width=width_in_pixel, height=height_in_pixel, bd=border_width, relief=relief_style, padx=self.widget_space_x/2, pady=self.widget_space_y/2    )
        ModuleFrame.grid_propagate(0)

        # a coex module may or maynot have a title, 
        # create a frame containing the title label only if a "title" string is passed to "module_title_name" parameter.
        if module_title_name:
            module_title_text = tk.StringVar(value=module_title_name)

            title_label_font_size = module_title_font_size if module_title_font_size else (self.font_size + 3)

            module_title_label_height_in_pixel = module_title_height_in_pixel if module_title_height_in_pixel else (title_label_font_size * 1.8)
           
            module_title_width_in_pixel = len(module_title_name) * title_label_font_size * 0.55

            module_title_label_in_frame, _ = self.create_label_in_frame(parent_frame=ModuleFrame, textvariable=module_title_text, font_size=title_label_font_size, 
                                                                        width_in_pixel=module_title_width_in_pixel, height_in_pixel=module_title_label_height_in_pixel, 
                                                                        padx=self.widget_space_x/2, pady=self.widget_space_y/2)

            module_title_label_in_frame.grid(row=0, column=0, padx=self.widget_space_x/2, pady=self.widget_space_y/2, sticky='w')

        else:
            module_title_label_height_in_pixel = 0
        

        BodyFrame = tk.Frame(ModuleFrame)
        BodyFrame.grid_propagate(0)
        BodyFrame.grid(row=1, column=0, padx=self.widget_space_x/2, pady=self.widget_space_y/2, sticky='w')
        BodyFrame['width'] = width_in_pixel - border_width - self.widget_space_x - self.widget_space_x - border_width
        BodyFrame['height'] = height_in_pixel - border_width - self.widget_space_y - module_title_label_height_in_pixel - self.widget_space_y - self.widget_space_y - border_width


        return ModuleFrame, BodyFrame



    # ==================================================================================================================================================================
    def create_ModuleLabelFrame(self, parent_frame, width_in_pixel, height_in_pixel, border_width, relief_style, 
                                module_title_name=False, module_title_font_size=False, module_title_height_in_pixel=False) -> tk.LabelFrame:
        """
        Function:   create a LabelFrame consisting of -- a text label displaying the module name if given
                                                        
        Usage:      self.send_command_to_device(command)
        Return:     the output of command
        """
        #  ---- ModuleFrame ----------------------------------------------------------------------------------------------
        # |  ---- BodyFrame --------------------------------------------------------------------------------------------  |
        # | |                                                                                                           | |
        # | |                                                                                                           | |
        # | |                                                                                                           | | 
        # | |                                                                                                           | | 
        # |  -----------------------------------------------------------------------------------------------------------  | 
        # ---------------------------------------------------------------------------------------------------------------

        ModuleLabelFrame = tk.LabelFrame( parent_frame, width=width_in_pixel, bd=border_width, relief=relief_style, padx=self.widget_space_x/2, pady=self.widget_space_y/2    )
        ModuleLabelFrame.grid_propagate(0)

        # a coex module may or maynot have a title, 
        if module_title_name:
            
            title_font_type = self.font_type
            title_font_size = module_title_font_size if module_title_font_size else self.font_size + 5
            ModuleLabelFrame['font'] = (title_font_type, title_font_size)
            
            ModuleLabelFrame['text'] = module_title_name

            ModuleLabelFrame['height'] = height_in_pixel - title_font_size/2

        else:
            title_font_size = 0

            ModuleLabelFrame['height'] = height_in_pixel - title_font_size/2


        ModuleBodyFrame = tk.Frame(ModuleLabelFrame)
        ModuleBodyFrame.grid_propagate(0)
        ModuleBodyFrame['width'] = ModuleLabelFrame['width'] - ModuleLabelFrame['padx']*2 - ModuleLabelFrame['bd']*2
        ModuleBodyFrame['height'] = ModuleLabelFrame['height'] - ModuleLabelFrame['pady']*2 - ModuleLabelFrame['bd']*2 - title_font_size
        ModuleBodyFrame.grid()

        return ModuleLabelFrame, ModuleBodyFrame








    # ==================================================================================================================================================================
    def __select_dir(self, window, directory_path_stringvar):
        directory_path = filedialog.askdirectory(   parent=window,  
                                                    initialdir = self.file_browse_initial_dir_path   )
        directory_path_stringvar.set(directory_path)
        self.file_browse_initial_dir_path = directory_path_stringvar.get()
        return directory_path


    def __convert_width_in_textletter_to_width_in_pixel(self, width_in_textletter, font_size):
        pixel_to_textletter_coefficient = 0.6
        width_in_pixel = width_in_textletter * font_size * pixel_to_textletter_coefficient

        return width_in_pixel


    # ==================================================================================================================================================================
    def create_directory_browse_frame(  self, parent_frame, frame_width_in_pixel, frame_height_in_pixel, directory_browse_button_width_in_pixel=False, 
                                        frame_border_width=False, frame_relief_style=False, key_name=False, key_label_in_same_row=False, default_dir_path=False):
        # create frame containing an optional label displaying key_name, a label displaying directory_path selected, and a button that browser directory
        # return the directory_browse_frame and the directory_path_stringvar
        
        # if key_name and key_label_in_same_row == False
        #  ---- directory_browse_frame -----------------------------------------------------------------------------------
        # |  -----------                                                                                                  |
        # | | key Label |                                                                                                 |
        # |  -----------                                                                                                  |
        # |  ------------------------------------------------------------------------      --------------------           |
        # | |                      directory_path_label                              |    | file-browse button |          |              
        # |  ------------------------------------------------------------------------      --------------------           | 
        #  ---------------------------------------------------------------------------------------------------------------


        # if key_name and key_label_in_same_row == True
        #  ---- directory_browse_frame -----------------------------------------------------------------------------------
        # |  -----------    ----------------------------------------------------------     --------------------           |
        # | | key Label |  |           directory_path_label                           |   | file-browse button |          |              
        # |  -----------    ----------------------------------------------------------     --------------------           | 
        #  ---------------------------------------------------------------------------------------------------------------

        # if key_name == False 
        # #  ---- directory_browse_frame -----------------------------------------------------------------------------------
        # # |     ----------------------------------------------------------------------     --------------------           |
        # # |   |           directory_path_label                                        |   | file-browse button |          |              
        # # |     ----------------------------------------------------------------------     --------------------           | 
        # #  ---------------------------------------------------------------------------------------------------------------
        self.file_browse_initial_dir_path = default_dir_path if default_dir_path else '~/'

        number_of_rows_in_directory_browse_frame = 2 if key_name and key_label_in_same_row==False else 1


        directory_browse_frame = tk.Frame(  parent_frame, width=frame_width_in_pixel, height=frame_height_in_pixel, padx=self.widget_space_x/2, pady=self.widget_space_y/2,
                                            bd=frame_border_width if frame_border_width else 0,
                                            relief=frame_relief_style if frame_relief_style else 'flat')

        directory_browse_frame.grid_propagate(0)


     
        if key_name:
        # ********************************************************************************************************************************
        # create the key_label widget displaying the key name 
            padx=self.widget_space_x/2
            pady=self.widget_space_y/2   
            key_label_width_in_pixel = self.__convert_width_in_textletter_to_width_in_pixel(len(key_name), self.font_size)
            key_label_height_in_pixel = int((frame_height_in_pixel - directory_browse_frame['bd']*2 - self.widget_space_y)/number_of_rows_in_directory_browse_frame) - self.widget_space_y


            key_label_in_frame, _ = self.create_label_in_frame( parent_frame=directory_browse_frame, 
                                                                textvariable=tk.StringVar(value=key_name),
                                                                width_in_pixel=key_label_width_in_pixel, 
                                                                height_in_pixel=key_label_height_in_pixel, 
                                                                padx=self.widget_space_x/2, pady=self.widget_space_y/2)

            key_label_in_frame.grid(row     =   1 if key_label_in_same_row else 0, 
                                    column  =   0 if key_label_in_same_row else 1, 
                                    padx=self.widget_space_x/2, pady=self.widget_space_y/2, sticky='w')


        # ********************************************************************************************************************************
        # create the directory-browse button that create a topwindow to browse directory
        directory_path_StringVar = tk.StringVar(value=default_dir_path) if default_dir_path else tk.StringVar()
        button_name = 'browse dir'
        directory_browse_button_width_in_pixel = self.__convert_width_in_textletter_to_width_in_pixel(len('browse dir'), self.font_size)
        directory_browse_button_height_in_pixel  = key_label_height_in_pixel
        directory_browser_button_in_frame, _ = self.create_button_in_frame( parent_frame=directory_browse_frame, 
                                                                            button_name=button_name, 
                                                                            width_in_pixel=directory_browse_button_width_in_pixel, 
                                                                            height_in_pixel=directory_browse_button_height_in_pixel, 
                                                                            button_action =lambda: self.__select_dir(window=directory_browse_frame, directory_path_stringvar=directory_path_StringVar), 
                                                                            padx=self.widget_space_x/2, pady=self.widget_space_y/2)
        directory_browser_button_in_frame.grid(row=1, column=2, padx=self.widget_space_x/2, pady=self.widget_space_y/2, sticky='w')


        # ********************************************************************************************************************************
        # create the directory_path_label that displays the selected direcotry path
        directory_path_label_height = key_label_height_in_pixel
        directory_path_label_width =(   frame_width_in_pixel - directory_browse_frame['bd']*2 - padx*2*3 - directory_browse_button_width_in_pixel
                                        if key_name and key_label_in_same_row==False else
                                        frame_width_in_pixel - directory_browse_frame['bd']*2 - padx*2*4 - key_label_width_in_pixel - directory_browse_button_width_in_pixel    )       
        
        # directory_path_label_in_frame, directory_path_label = self.create_label_in_frame(   parent_frame=directory_browse_frame, 
        #                                                                                     textvariable=directory_path_StringVar, 
        #                                                                                     width_in_pixel=directory_path_label_width, 
        #                                                                                     height_in_pixel=directory_path_label_height, 
        #                                                                                     padx=self.widget_space_x/2, pady=self.widget_space_y/2, 
        #                                                                                     disable_wrap=True, border_width=1, relief_style='solid')
        # directory_path_label['anchor'] = 'e'
        # directory_path_label_in_frame.grid(row=1, column=1, padx=self.widget_space_x/2, pady=self.widget_space_y/2, sticky='w')



        directory_path_label = tk.Label(    directory_browse_frame, font=(self.font_type, self.font_size), 
                                            width=int(directory_path_label_width/self.font_size*1.57),
                                            height=1,
                                            bd=1, relief='solid',
                                            textvariable=directory_path_StringVar, 
                                            padx=self.widget_space_x/2, pady=self.widget_space_y/2, anchor='e')

        directory_path_label.grid(row=1, column=1, padx=self.widget_space_x/2, pady=self.widget_space_y/2, sticky='w')



        return directory_browse_frame, directory_path_StringVar


    # ==================================================================================================================================================================
    def create_Entry_box_frame(self, parent_frame, frame_width_in_pixel, frame_height_in_pixel, key_name, key_label_in_same_row=False, frame_border_width=False, frame_relief_style=False):
        # create a frame conatining a label widget displaying key name, and an entry box widget
        # return this entry_box_frame and the text entered in entry box.
        
        # if key_label_in_same_row == False:
        #  ---- Entry_box_frame ------------------------------------------------------------------------------------------
        # |  -----------                                                                                                  |
        # | | key Label |                                                                                                 |
        # |  -----------                                                                                                  |
        # |  -----------------------------------------------------------------------------------------------------------  |
        # | |                      entry widget                                                                         | |              
        # |  -----------------------------------------------------------------------------------------------------------  | 
        #  ---------------------------------------------------------------------------------------------------------------

        # if key_label_in_same_row:
        #  ---- Entry_box_frame ------------------------------------------------------------------------------------------
        # |  -----------    --------------------------------------------------------------------------------------------  |
        # | | key Label |  |           entry widget                                                                     | |              
        # |  -----------    --------------------------------------------------------------------------------------------  | 
        #  ---------------------------------------------------------------------------------------------------------------


        padx = self.widget_space_x/2
        pady = self.widget_space_y/2

        number_of_rows_in_entry_box_frame = 1 if key_label_in_same_row==True else 2

        entry_box_frame = tk.Frame( parent_frame, width=frame_width_in_pixel, height=frame_height_in_pixel, padx=padx, pady=pady,
                                    bd=frame_border_width if frame_border_width else 0,
                                    relief=frame_relief_style if frame_relief_style else 'flat')
        entry_box_frame.grid_propagate(0)


        # ********************************************************************************************************************************
        # create a label displaying the key_name
        key_label_width_in_pixel = self.__convert_width_in_textletter_to_width_in_pixel(len(key_name), self.font_size)
        key_label_height_in_pixel = int((frame_height_in_pixel - entry_box_frame['bd']*2 - self.widget_space_y)/number_of_rows_in_entry_box_frame) - self.widget_space_y

        key_label_in_frame, _ = self.create_label_in_frame( parent_frame=entry_box_frame, 
                                                            textvariable=tk.StringVar(value=key_name),  
                                                            width_in_pixel=key_label_width_in_pixel, 
                                                            height_in_pixel=key_label_height_in_pixel, 
                                                            padx=padx, pady=pady )
        key_label_in_frame.grid( row=1 if key_label_in_same_row else 0,
                                 column=0 if key_label_in_same_row else 1, 
                                 padx=padx, pady=pady, sticky='w')


        # ********************************************************************************************************************************
        # create the entry widget
        entry_box_width_in_pixel = ( frame_width_in_pixel - padx*2*3 - key_label_width_in_pixel) if key_label_in_same_row else (frame_width_in_pixel - padx*2*2)
        entry_box_height_in_pixel = key_label_height_in_pixel

        entry_frame, entry_box_text = self.create_Entry_in_frame(   parent_frame=entry_box_frame,
                                                                    width_in_pixel=entry_box_width_in_pixel, 
                                                                    height_in_pixel=entry_box_height_in_pixel)
        entry_frame.grid(row=1, column=1, padx=self.widget_space_x/2, pady=self.widget_space_y/2, sticky='w')


        return entry_box_frame, entry_box_text


    # ======================================================================================================
    # Function: copy the text to clipboard 
    def __copy_to_clipboard(self, text):
        os.system(f'echo {text}|pbcopy')


    # ==================================================================================================================================================================
    def create_KeyValueLabelPair_frame(self, frame, frame_width_in_pixel, frame_height_in_pixel, key_name, key_label_width_in_pixel, copy_button_exist=False, frame_border_width=False, frame_relief_style=False):
        # create a tkinter frame containing:    (1) a key label displaying the key name string
        #                                       (2) a value label displaying the value corresponds to the key name
        #                                       (3) an optional button copy the text in the value label
        # return this KeyValueLabelPair frame and the tk.StringVar in the value label widget


        # if copy_button_exist == True 
        #  ---- KeyLabel_ValueLabel_frame --------------------------------
        # |  -----------    --------------------------     -------------  |
        # | | key Label |  |        value_label       |   | copy button | |              
        # |  -----------    --------------------------     -------------  | 
        #  ---------------------------------------------------------------


        # if copy_button_exist == False
        #  ---- KeyLabel_ValueLabel_frame --------------------------------
        # |  -----------    --------------------------------------------  |
        # | | key Label |  |        value_label                         | |              
        # |  -----------    --------------------------------------------  | 
        #  ---------------------------------------------------------------
        padx = self.widget_space_x/2
        pady = self.widget_space_y/2

        KeyLabel_ValueLabel_frame = tk.Frame(   frame, width=frame_width_in_pixel, height=frame_height_in_pixel,
                                                bd=frame_border_width if frame_border_width else 0,
                                                relief=frame_relief_style if frame_relief_style else 'flat' )
        KeyLabel_ValueLabel_frame.grid_propagate(0)

        # ********************************************************************************************************************************   
        # create a tkinter copy button that copy the text string in the value label to clipboard 
        if copy_button_exist == 'True':
            copy_button_width_in_pixel = int(len('copy') * self.font_size * 0.80)
            copy_button_height_in_pixel = (frame_height_in_pixel - self.widget_space_y)
            copy_button_frame, _ = self.create_button_in_frame( parent_frame=KeyLabel_ValueLabel_frame, button_name='copy',
                                                                button_action=lambda:self.__copy_to_clipboard(value_StringVar.get()), 
                                                                width_in_pixel=copy_button_width_in_pixel, height_in_pixel=copy_button_height_in_pixel, 
                                                                padx=self.widget_space_x/2, pady=self.widget_space_y/2)
            copy_button_frame.grid( row=0, column=2, padx=self.widget_space_x/2, pady=self.widget_space_y/2, sticky='w' )


        # ********************************************************************************************************************************
        # create a tkinter label widget displaying the key_name
        key_label_height_in_pixel = (frame_height_in_pixel - self.widget_space_y)
        key_label_in_frame, _ = self.create_label_in_frame( parent_frame=KeyLabel_ValueLabel_frame, textvariable=tk.StringVar(value=key_name),
                                                            width_in_pixel=key_label_width_in_pixel, height_in_pixel=key_label_height_in_pixel, 
                                                            padx=self.widget_space_x/2, pady=self.widget_space_y/2  )
        key_label_in_frame.grid( row=0, column=0, padx=self.widget_space_x/2, pady=self.widget_space_y/2, sticky='w')


        # ********************************************************************************************************************************
        # calculate the width of the label widget displaying the value corresponding to the key name        
        # create a tkinter label widget displaying the value content
        if copy_button_exist == 'True':
            value_label_width_in_pixel = (frame_width_in_pixel - KeyLabel_ValueLabel_frame['bd'] - self.widget_space_x - key_label_width_in_pixel - self.widget_space_x - self.widget_space_x - copy_button_width_in_pixel - self.widget_space_x - KeyLabel_ValueLabel_frame['bd'])
        else:
            value_label_width_in_pixel = (frame_width_in_pixel - KeyLabel_ValueLabel_frame['bd'] - self.widget_space_x - key_label_width_in_pixel - self.widget_space_x - self.widget_space_x - KeyLabel_ValueLabel_frame['bd'])
        
        value_StringVar = tk.StringVar()
        value_label_height_in_pixel = (frame_height_in_pixel - self.widget_space_y)
        value_label_in_frame, value_label = self.create_label_in_frame(   parent_frame=KeyLabel_ValueLabel_frame, textvariable=value_StringVar,
                                                                width_in_pixel=value_label_width_in_pixel, height_in_pixel=value_label_height_in_pixel, 
                                                                padx=self.widget_space_x/2, pady=self.widget_space_y/2, border_width=1, relief_style='solid')
        value_label_in_frame.grid( row=0, column=1, padx=self.widget_space_x/2, pady=self.widget_space_y/2, sticky='w'   )



        return KeyLabel_ValueLabel_frame, value_StringVar

    # ======================================================================================================
    # Function: create a popu-up window displaying given text 
    def No_connection_window(self, parent_frame, width, height):
        self.message_window(parent_frame, width, height, 'No connected unit !', font_size=self.font_size + 10)

    def message_window(self, parent_frame, width, height, message_text:str, message_color=False, font_type=False, font_size=False, ):
        note_window = tk.Frame( parent_frame, bd=1, relief='solid',
                                height=parent_frame['height'] - self.widget_space_y - parent_frame['bd']*2, 
                                width=parent_frame['width'] - self.widget_space_x - parent_frame['bd']*2 )
        note_window.grid_propagate(0)
        note_window.grid( row=0, column=0)


        note_info_label_frame, note_info_label = self.create_label_in_frame(parent_frame=note_window, textvariable=tk.StringVar(value=message_text), 
                                                                            width_in_pixel=note_window['width'] - note_window['bd']*2 - self.widget_space_x, 
                                                                            height_in_pixel=(note_window['height'] - note_window['bd']*2 - self.widget_space_y)*2/3 - self.widget_space_y,
                                                                            font_size = font_size if font_size else self.font_size,
                                                                            font_type = font_type if font_type else self.font_type)


        note_info_label['anchor'] = 'center'
        note_info_label['fg'] = message_color if message_color else 'black'
        exit_button_frame, exit_button = self.create_button_in_frame(   parent_frame=note_window, button_name='OK', 
                                                                        width_in_pixel=note_window['width']/5, 
                                                                        height_in_pixel=(note_window['height'] - note_window['bd']*2 - self.widget_space_y)/3 - self.widget_space_y, 
                                                                        button_action=note_window.destroy)

        note_info_label_frame.grid(row=0, column=0, columnspan=2)
        exit_button_frame.grid(row=1, column=0, columnspan=1)

        return note_window