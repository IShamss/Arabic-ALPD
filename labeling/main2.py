import tkinter

window = tkinter.Tk()

window.title("Automatic Labeling Tool")
window.minsize(width=500,height=300)

input_folder_label = tkinter.Label(text="Images Folder",font=("Arial",15,"italic"))
input_folder_label.pack(side="left")
output_folder_label = tkinter.Label(text="Output Folder")
output_folder_label.pack(side="left")





window.mainloop()