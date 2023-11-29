
from PIL import Image
import tkinter as tk
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox


class App(ctk.CTk):
    def __init__(self, app_version, sidebar_width):
        super().__init__()
        self.app_version = app_version
        self.sidebar_width = sidebar_width
        self.file_loaded = False
        self.file_extension = None

    def open_file(self):
        original_img = ctk.filedialog.askopenfile()
        try:
            self.RGB_file = Image.open(original_img.name)
            self.file_loaded = True
        except:
            CTkMessagebox(title='Error', message='The file was not loaded. You must choose graphical image.', icon='warning')
        if self.file_loaded:
            sf = 0.85 # scalling factor of image
            for widget in self.main_frame.winfo_children():
                widget.destroy()
            if self.RGB_file.size[0] >= self.RGB_file.size[1]:
                image_width = sf*(self.winfo_screenwidth() - self.sidebar_width)
                image_height = self.RGB_file.size[1]/self.RGB_file.size[0]*image_width
            else:
                image_height = sf*self.winfo_screenheight()
                image_width = self.RGB_file.size[0]/self.RGB_file.size[1]*image_height
            image = ctk.CTkImage(light_image=self.RGB_file, size=(image_width, image_height))
            self.label = ctk.CTkLabel(master=self.main_frame, image=image, text='')
            self.label.place(relx=0.5, rely=0.45, anchor=ctk.CENTER)

    def convert_and_save_file(self):
        if self.file_loaded:
            ff = self.file_extension.get()  # file format (filename extension)
            directory = ctk.filedialog.asksaveasfile(defaultextension='.'+ff)
            try:
                converted_img = self.RGB_file.convert('CMYK')
                converted_img.save(directory.name)
            except:
                CTkMessagebox(title='Error', message='Something went wrong. File was not converted and not saved.', icon='warning')
        else:
            CTkMessagebox(title='Error', message='File was not loaded. Please load file.', icon='warning')

    def exit(self):
        self.destroy()

    def create_window(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.title(f'RGB image to CMYK converter by Krystian Mistewicz ver. {app_version}')
        self.after(0, lambda: self.state('zoomed'))
        w_height = self.winfo_screenheight() # screen height
        w_width = self.winfo_screenwidth() # screen width
        self.sidebar_frame = ctk.CTkFrame(self, width=self.sidebar_width, height=w_height)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame = ctk.CTkFrame(self, width=w_width-self.sidebar_width, height=w_height, fg_color='gray90')
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.description_frame = ctk.CTkFrame(self.sidebar_frame, height=100, width=250)
        self.description_frame.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)
        description_text = 'This is app that allows to load\ngraphical RGB image, preview it,\nand convert to CMYK file'
        self.label_description = ctk.CTkLabel(master=self.description_frame, text=description_text)
        self.label_description.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.radiobutton_frame = ctk.CTkFrame(self.sidebar_frame, height=200, width=150)
        self.radiobutton_frame.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)
        self.file_extension = tk.StringVar(value='tiff')
        self.label_radio = ctk.CTkLabel(master=self.radiobutton_frame, text='Choose file format\nof new CMYK file:')
        self.label_radio.place(relx=0.5, rely=0.15, anchor=ctk.CENTER)
        self.radio_button_1 = ctk.CTkRadioButton(master=self.radiobutton_frame, text='TIFF', variable=self.file_extension, value='tiff')
        self.radio_button_1.place(relx=0.5, rely=0.35, anchor=ctk.CENTER)
        self.radio_button_2 = ctk.CTkRadioButton(master=self.radiobutton_frame, text='JPG', variable=self.file_extension, value='jpg')
        self.radio_button_2.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.radio_button_3 = ctk.CTkRadioButton(master=self.radiobutton_frame, text='PDF', variable=self.file_extension, value='pdf')
        self.radio_button_3.place(relx=0.5, rely=0.65, anchor=ctk.CENTER)
        self.radio_button_4 = ctk.CTkRadioButton(master=self.radiobutton_frame, text='EPS', variable=self.file_extension, value='eps')
        self.radio_button_4.place(relx=0.5, rely=0.8, anchor=ctk.CENTER)
        self.button_load = ctk.CTkButton(master=self.sidebar_frame, text="Load RGB image", command=lambda:self.open_file())
        self.button_load.place(relx=0.5, rely=0.25, anchor=ctk.CENTER)
        self.button_convert = ctk.CTkButton(master=self.sidebar_frame, text="Convert and save", command=lambda:self.convert_and_save_file())
        self.button_convert.place(relx=0.5, rely=0.325, anchor=ctk.CENTER)
        self.button_exit = ctk.CTkButton(master=self.sidebar_frame, text="Exit", command=lambda:self.exit())
        self.button_exit.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)
        self.mainloop()


if __name__ == '__main__':
    app_version = 1.6
    sidebar_width = 300
    app = App(app_version, sidebar_width)
    app.create_window()
