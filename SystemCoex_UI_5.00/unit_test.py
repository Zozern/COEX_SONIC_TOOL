# from SystemCoex_Customized_Tkinter_Widgets import systemcoex_customized_tkinter_widgets
import tkinter as tk
import re

main_window = tk.Tk()
main_window.title('title')
main_window.geometry("200x200")


# coex_tk = systemcoex_customized_tkinter_widgets('Arial', 12, 2, 2)

# label_1_frame, label_1 = coex_tk.create_label_in_frame_test(main_window, tk.StringVar(value='hello world'), 30, 10, border_width=1, relief_style='solid')
# label_1_frame.grid(row=0, column=0)

# label_2_frame, label_2 = coex_tk.create_label_in_frame(main_window, tk.StringVar(value='hello world'), 30, 10, border_width=1, relief_style='solid')
# label_2_frame.grid(row=1, column=0)





    # subframe_width  = int(  (parent_frame['width'] - parent_frame['bd']*2 - padx*2) * subfrmae_relative_width   - padx*2  )
    # subframe_height = int(  (parent_frame['height'] - parent_frame['bd']*2 - pady*2) * subfrmae_relative_height  - pady*2  )


    # return subframe_width, subframe_height





# layout = {
#     0: {    'row': 0, 'column':0, 'rowspan': 1, 'columnspan':1, 'height': 10, 'width': 20, 'bd': 1, 'relief': 'solid'   },
#     # 1: {    'row': 1, 'column':0, 'rowspan': 1, 'columnspan':1, 'height': 10, 'width': 20, 'bd': 1, 'relief': 'solid'    },
#     2: {    'row': 2, 'column':0, 'rowspan': 2, 'columnspan':1, 'height': 20, 'width': 20, 'bd': 1, 'relief': 'solid'   },
    
#     3: {    'row': 0, 'column':1, 'rowspan': 1, 'columnspan':1, 'height': 10, 'width': 20, 'bd': 1, 'relief': 'solid'   },
#     4: {    'row': 1, 'column':1, 'rowspan': 2, 'columnspan':1, 'height': 20, 'width': 20, 'bd': 1, 'relief': 'solid'   },
# }


# Calculate_SubFrame_width_and_height(main_window, layout, 2)



# for key, value in layout.items():
#     frame = tk.Frame(main_window, width=value['width'], height=value['height'], bd=1, relief='solid')
#     frame.grid_propagate(0)
#     frame.grid(row=value['row'], column=value['column'], rowspan=value['rowspan'], columnspan=value['columnspan'], sticky='w')
    







main_window.mainloop()