import os
import tkinter as tk
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter
from scipy import ndimage
import numpy as np
import cv2
from tkinter import colorchooser
import tkinter.filedialog
import tkinter.messagebox


THEME_COLOR = "#FFFFFF"
undo_list = []
redo_list = []

class Editor(tk.Frame):

    def __init__(self,master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.configure(background=THEME_COLOR)
        self.image_reference = None
        self.theme_variable = tk.IntVar()
        self.theme_variable.set(1)
        buttonWidth=14
        buttonHeight=2
        backgroundColour="#cff055"

        self.toolKitFrame=tk.Frame(self.master)
        scaleButton=tk.Button(self.toolKitFrame, text="Scale Image",background=backgroundColour,\
                      width=buttonWidth, height=buttonHeight,command=self.scale_image_window)
        scaleButton.grid(row=0,column=0)


        mirrorButton=tk.Button(self.toolKitFrame, text="Mirror",background=backgroundColour, \
                           width=buttonWidth,height=buttonHeight,command=self.flip_vertically)
        mirrorButton.grid(row=1,column=0)

        flipButton=tk.Button(self.toolKitFrame, text="Flip",background=backgroundColour ,\
                      width=buttonWidth,height=buttonHeight,command=self.flip_horizontally)
        flipButton.grid(row=2,column=0)

        rotateButton=tk.Button(self.toolKitFrame, text="Rotate",background=backgroundColour, \
                        width=buttonWidth,height=buttonHeight,command=self.rotate_right)
        rotateButton.grid(row=3,column=0)

        blurButton=tk.Button(self.toolKitFrame, text="Blur",background=backgroundColour ,\
                            width=buttonWidth, height=buttonHeight,command=self.blur_image)
        blurButton.grid(row=4,column=0)

        gaussianButton=tk.Button(self.toolKitFrame, text="Gaussian Blur",background=backgroundColour ,\
                      width=buttonWidth,height=buttonHeight,command=self.gaussian_frame)
        gaussianButton.grid(row=5,column=0)

        smoothButton=tk.Button(self.toolKitFrame, text="Smooth",background=backgroundColour ,\
                      width=buttonWidth,height=buttonHeight,command=self.smooth_image)
        smoothButton.grid(row=6,column=0)

        invertButton=tk.Button(self.toolKitFrame, text="Invert",background=backgroundColour ,\
                      width=buttonWidth,height=buttonHeight,command=self.invert)
        invertButton.grid(row=7,column=0)

        contrastButton=tk.Button(self.toolKitFrame, text="Contrast",background=backgroundColour ,\
                      width=buttonWidth,height=buttonHeight,command=self.contrast)
        contrastButton.grid(row=8,column=0)

        grayButton=tk.Button(self.toolKitFrame, text="Grayscale",background=backgroundColour ,\
                      width=buttonWidth,height=buttonHeight,command=self.to_grayscale)
        grayButton.grid(row=9,column=0)

        edgeButton=tk.Button(self.toolKitFrame, text="Find Edges",background=backgroundColour, \
                           width=buttonWidth,height=buttonHeight,command=self.find_edges)
        edgeButton.grid(row=10,column=0)

        contourButton=tk.Button(self.toolKitFrame, text="Contour",background=backgroundColour ,\
                      width=buttonWidth,height=buttonHeight,command=self.image_contour)
        contourButton.grid(row=11,column=0)

        resetButton=tk.Button(self.toolKitFrame, text="Reset",background=backgroundColour ,\
                      width=buttonWidth,height=buttonHeight,command=self.reset)
        resetButton.grid(row=12,column=0)

        self.toolKitFrame.pack(side=tk.LEFT)

        # creates the frame which will hold the image
        self.image_holder_frame = tk.Frame(self.master)
        self.image_holder_frame.pack()
        self.image_holder_frame.configure(background=THEME_COLOR)

        self.image_label = tk.Label(self.image_holder_frame,text="Welcome to Longclaw",image=None)
        self.image_label.pack()
        self.image_label.configure(background=THEME_COLOR)

        # creates the top-level menu-bar which holds the drop-down buttons
        self.menubar = tk.Menu(self.master)
        self.master.config(menu=self.menubar)
        self.menubar.configure(background=THEME_COLOR)


        self.label_width = self.image_holder_frame.winfo_screenwidth()
        self.label_height = self.image_holder_frame.winfo_screenheight() - 150

        # imports the images which appear on every file-menu button
        #self.open_icon = tk.PhotoImage(file="Icons/open.png")
        #self.save_icon = tk.PhotoImage(file="Icons/save.png")
       # self.save_as_icon = tk.PhotoImage(file="Icons/save_as.png")
      #  self.settings_icon = tk.PhotoImage(file="Icons/settings.png")
      
      # creates the drop-down button 'File' and adds it to the menu-bar
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.configure(background=THEME_COLOR)
        self.file_menu.add_command(label=" Open", accelerator='Ctrl + O',
                                  # compound="left", image=self.open_icon,
                                   command=self.open_image)
        self.file_menu.add_command(label=" Capture Image",
                                #   ,compound="left", image=self.open_icon,
                                   command=self.camera)
        self.file_menu.add_command(label=" Save", accelerator='Ctrl + S',
                                #   compound="left", image=self.save_icon,
                                   command=self.save_image)
        self.file_menu.add_command(label=" Save As...",
                                   accelerator='Ctrl + Shift + S',
                                #  compound="left", image=self.save_as_icon,
                                   command=self.save_as)
        self.themes_menu = tk.Menu(self.file_menu, tearoff=0)
        self.themes_menu.configure(background=THEME_COLOR)
        self.themes_menu.add_radiobutton(label="Default White",
                                         variable=self.theme_variable,
                                         value=1, command=self.theme_color)
        self.themes_menu.add_radiobutton(label="Gray",
                                         variable=self.theme_variable,
                                         value=2, command=self.theme_color)
        self.themes_menu.add_radiobutton(label="Green",
                                         variable=self.theme_variable,
                                         value=3, command=self.theme_color)
        self.themes_menu.add_radiobutton(label="Blue",
                                         variable=self.theme_variable,
                                         value=4, command=self.theme_color)
        self.themes_menu.add_radiobutton(label="Pink",
                                         variable=self.theme_variable,
                                         value=5, command=self.theme_color)
        self.themes_menu.add_radiobutton(label="Custom theme",
                                         variable=self.theme_variable,
                                         value=6, command=self.custom_theme)

        self.file_menu.add_cascade(label=" Settings", 
                                  # compound="left",image=self.settings_icon,
                                   menu=self.themes_menu)

        self.file_menu.add_separator()
        self.file_menu.add_command(label=" Exit", command=self.exit_program)

        # constructing the 'Edit' drop-down menu
      #  self.undo_icon = tk.PhotoImage(file="Icons/undo.png")
     #   self.redo_icon = tk.PhotoImage(file="Icons/redo.png")
       # self.flip_horizontally_icon = tk.PhotoImage(file="Icons/flip_hor.png")
    #    self.flip_vertically_icon = tk.PhotoImage(file="Icons/flip_vert.png")
    #    self.turn_right_icon = tk.PhotoImage(file="Icons/turn_right.png")
    #    self.turn_left_icon = tk.PhotoImage(file="Icons/turn_left.png")
    #    self.turn_180_icon = tk.PhotoImage(file="Icons/turn_180.png")

        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.configure(background=THEME_COLOR)
        self.edit_menu.add_command(label=" Undo", accelerator='Ctrl + Z',
                                  # compound="left", image=self.undo_icon,
                                   command=self.undo)
        self.edit_menu.add_command(label=" Redo", 
                                   accelerator='Ctrl + Shift + Z',
                                  # compound="left",  image=self.redo_icon,
                                   command=self.redo)

        self.edit_menu.add_separator()

        self.edit_menu.add_command(label=" Flip Horizontally", 
                                 #  compound="left", image=self.flip_horizontally_icon,
                                   command=self.flip_horizontally)

        self.edit_menu.add_command(label=" Flip Vertically",
                                #   compound="left", image=self.flip_vertically_icon,
                                   command=self.flip_vertically)
        self.edit_menu.add_separator()

        self.edit_menu.add_command(label=" Rotate 90\u00b0 clockwise",
                                 #  compound="left", image=self.turn_right_icon,
                                   command=self.rotate_right)
        self.edit_menu.add_command(label=" Rotate 90\u00b0 counter-clockwise",
                                #   compound="left", image=self.turn_left_icon,
                                   command=self.rotate_left)

        self.edit_menu.add_command(label=" Rotate 180\u00b0",
                                #   compound="left", image=self.turn_180_icon,
                                   command=self.rotate_180)

        # constructing the 'Image' drop-down menu
   #     self.sclae_icon = tk.PhotoImage(file="Icons/scale_image.png")
   #     self.crop_icon = tk.PhotoImage(file="Icons/invert.png")
  #      self.contrast_icon = tk.PhotoImage(file="Icons/contrast.png")
  #      self.graysclae_icon = tk.PhotoImage(file="Icons/grayscale.png")
        self.image_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Image", menu=self.image_menu)
        self.image_menu.configure(background=THEME_COLOR)
        self.image_menu.add_command(label=" Scale Image", compound="left",
                                  #  image=self.sclae_icon,
                                    command=self.scale_image_window)
        self.image_menu.add_command(label=" Invert", compound="left",
                                  #  image=self.crop_icon, 
                                  command=self.invert)
        self.image_menu.add_command(label=" Contrast", compound="left",
                                  #  image=self.contrast_icon,
                                    command=self.contrast)
        self.image_menu.add_command(label=" Grayscale", compound="left",
                                  #  image=self.graysclae_icon,
                                    command=self.to_grayscale)
        self.image_menu.add_command(label=" Posterize", compound="left",
                                  #  image=self.graysclae_icon,
                                    command=self.Posterize)


        # constructing the 'Filters' drop-down menu
        self.filters_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Filters", menu=self.filters_menu)
        self.filters_menu.configure(background=THEME_COLOR)
        self.filters_menu.add_command(label="Blur", command=self.blur_image)
        self.filters_menu.add_command(label="Gaussian Blur",
                                      command=self.gaussian_frame)
        self.filters_menu.add_command(label="Smooth",
                                      command=self.smooth_image)
        self.filters_menu.add_separator()

        self.filters_menu.add_command(label="Find Edges",
                                      command=self.find_edges)
        self.filters_menu.add_command(label="Contour",
                                      command=self.image_contour)

        # constructing the 'Help' drop-down menu
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.configure(background=THEME_COLOR)
        self.help_menu.add_command(label="Help", accelerator='F1',
                                   command=self.help)
        self.help_menu.add_command(label="About", command=self.about)


        #creates a keyboard shortcut which calls the open_image() method
        self.master.bind('<Control-o>', lambda e: self.open_image())
        self.master.bind('<Control-O>', lambda e: self.open_image())
        #creates a keyboard shortcut which calls the save_image() method
        self.master.bind('<Control-s>', lambda e: self.save_image())
        self.master.bind('<Control-S>', lambda e: self.save_image())
        #creates a keyboard shortcut which calls the save_as() method
        self.master.bind('<Control-Shift-s>', lambda e: self.save_as())
        self.master.bind('<Control-Shift-S>', lambda e: self.save_as())
        #creates a keyboard shortcut which calls the undo() method
        self.master.bind('<Control-z>', lambda e: self.undo())
        self.master.bind('<Control-Z>', lambda e: self.undo())
        #creates a keyboard shortcut which calls the redo() method
        self.master.bind('<Control-Shift-z>', lambda e: self.redo())
        self.master.bind('<Control-Shift-Z>', lambda e: self.redo())
        #creates a keyboard shortcut which calls the help() method
        self.master.bind('<KeyPress-F1>', lambda e: self.help())






    def Posterize(self):
        self.im = self.image_reference

        self.n = 5    # Number of levels of quantization

        self.indices = np.arange(0,256)   # List of all colors

        self.divider = np.linspace(0,255,self.n+1)[1] # we get a divider

        self.quantiz = np.int0(np.linspace(0,255,self.n)) # we get quantization colors

        self.color_levels = np.clip(np.int0(self.indices/self.divider),0,self.n-1) # color levels 0,1,2..

        self.palette = self.quantiz[self.color_levels] # Creating the palette

        self.im2 = self.palette[self.im]  # Applying palette on image

        self.im2 = cv2.convertScaleAbs(self.im2) # Converting image back to uint8

        try:
            self.img = self.im2
            self.image = Image.fromarray(self.img)
            self.image_reference = self.image
            width, height = self.image.size
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            image_tk = ImageTk.PhotoImage(image=self.image_resized)
            self.image_label.image = image_tk
            self.image_label.configure(image=image_tk)
            undo_list.append(self.image_reference)
        except:
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')
    def open_image(self):
        self.file_types = [('All files', '*'), ('GIF Image', '*.gif'),
                           ('JPEG Image', '*.jpg *.jpeg *.jpe'),
                           ('PNG Image', '*.png'), ('BMP Image', '*.bmp'),
                           ('TIFF Image', '*.tiff *.tif')]
        self.file_name = tkinter.filedialog.askopenfilename(
            parent=self.master, title='Choose a file',filetypes=self.file_types)

        if self.file_name != "":
            try:
                self.img = ndimage.imread(self.file_name)
                self.image = Image.fromarray(self.img)
                self.image_reference = self.image
                width, height = self.image.size
                self.image_resized = self.resize_image(width, height,
                                                       self.label_width,
                                                       self.label_height,
                                                       self.image)
                image_tk = ImageTk.PhotoImage(image=self.image_resized)
                self.image_label.image = image_tk
                self.image_label.configure(image=image_tk)
                undo_list.append(self.image_reference)
            except:
                tkinter.messagebox.showwarning(title='Open file',
                                               message='Cannot open this file',
                                               icon='error')
        else:
            pass

        return self.file_name


    def camera(self):

        self.camera_port = 0
        self.ramp_frames = 30
        self.camera = cv2.VideoCapture(self.camera_port)
        def get_image():
            self.retval, self.im = self.camera.read()
            return self.im
        for i in range(self.ramp_frames):
            self.temp = get_image()
        self.camera_capture = get_image()
        try:
            self.camera_capture = self.camera_capture[:, :, ::-1] # or image = image[:, :, (2, 1, 0)]
            self.img = self.camera_capture
            self.image = Image.fromarray(self.img)
            self.image_reference = self.image
            width, height = self.image.size
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            image_tk = ImageTk.PhotoImage(image=self.image_resized)
            self.image_label.image = image_tk
            self.image_label.configure(image=image_tk)
            undo_list.append(self.image_reference)
            #cv2.imshow('img',camera_capture)
            #cv2.waitKey()
            del(camera)

        except:
            pass




    def resize_image(self, width, height, label_width, label_height, image):
        self.factor_one = 1.0 * label_width / width
        self.factor_two = 1.0 * label_height / height
        self.factor = min([self.factor_one, self.factor_two])
        # if the image resolution is smaller as the label resolution the function returns the original image
        # otherwise the function resize the image
        if self.factor_one > 1 and self.factor_two > 1:
            return image
        else:
            self.width_resized = int(width * self.factor)
            self.height_resized = int(height * self.factor)
            return image.resize((self.width_resized, self.height_resized),
                                 Image.ANTIALIAS)

    def save_image(self):
        try:
            image_name = self.file_name
            self.image.save(image_name)
        except:
            self.save_as()

    def save_as(self):
        try:
            self.file_types = [('All files', '*'), ('GIF Image', '*.gif'),
                               ('JPEG Image', '*.jpg *.jpeg *.jpe'),
                               ('PNG Image', '*.png'), ('BMP Image', '*.bmp'),
                               ('TIFF Image', '*.tiff *.tif')]
            self.save_img_as = tkinter.filedialog.asksaveasfilename\
                    (initialfile='editor.png', filetypes=self.file_types)
            self.image.save(self.save_img_as)
        except:
            pass

    def theme_color(self):
        self.variable = self.theme_variable.get()
        self.background_color = "#FFFFFF"

        if self.variable == 1:
            self.background_color = "#FFFFFF"  # white
        elif self.variable == 2:
            self.background_color = "#D1D1D1"  # Gray
        elif self.variable == 3:
            self.background_color = "#3afc46"  # Green
        elif self.variable == 4:
            self.background_color = "#BFD9F2"  # Blue
        elif self.variable == 5:
            self.background_color = "#F7DEFA"  # Pink
        else:
            pass

        # applies the made changes to the program
        self.master.configure(background=self.background_color)
        self.image_holder_frame.configure(background=self.background_color)
        self.menubar.configure(background=self.background_color)
        self.file_menu.configure(background=self.background_color)
        self.themes_menu.configure(background=self.background_color)
        self.edit_menu.configure(background=self.background_color)
        self.image_menu.configure(background=self.background_color)
        self.filters_menu.configure(background=self.background_color)
        self.help_menu.configure(background=self.background_color)
        self.image_label.configure(background=self.background_color)

    def custom_theme(self):
        self.color = colorchooser.askcolor()
        self.color_choice = self.color[1]
        # applies the made changes to the program
        self.master.configure(background=self.color_choice)
        self.image_holder_frame.configure(background=self.color_choice)
        self.menubar.configure(background=self.color_choice)
        self.file_menu.configure(background=self.color_choice)
        self.themes_menu.configure(background=self.color_choice)
        self.edit_menu.configure(background=self.color_choice)
        self.image_menu.configure(background=self.color_choice)
        self.filters_menu.configure(background=self.color_choice)
        self.help_menu.configure(background=self.color_choice)
        self.image_label.configure(background=self.color_choice)

    def exit_program(self):
        if tkinter.messagebox.askyesno(title="Quit", message="Are you " +
                                       "sure you want to quit?\n"
                                       "\nAll unsaved data will be lost."):
            self.master.destroy()  # exits the main program
            # if there is a temp image in the temp folder, deletes it
            try:
                os.remove('temp/temp.png')
            except:
                pass

    def undo(self):
        if len(undo_list) != 0:
            try:
                self.image = undo_list[-2]
                self.image_reference = self.image
                width, height = self.image.size
                self.image_resized = self.resize_image(width, height,
                                                       self.label_width,
                                                       self.label_height,
                                                       self.image)
                image_tk_undo = ImageTk.PhotoImage(image=self.image_resized)
                self.image_label.image = image_tk_undo
                self.image_label.configure(image=image_tk_undo)
                if undo_list[-1] not in redo_list:
                    redo_list.append(undo_list[-1])
                else:
                    pass
                redo_list.append(undo_list[-2])
                undo_list.pop()
            except:
                pass
        else:
            pass

    def redo(self):
        if len(redo_list) != 0:
            try:
                self.image = redo_list[-1]
                self.image_reference = self.image
                width, height = self.image.size
                self.image_resized = self.resize_image(width, height,
                                                       self.label_width,
                                                       self.label_height,
                                                       self.image)
                image_tk_redo = ImageTk.PhotoImage(image=self.image_resized)
                self.image_label.image = image_tk_redo
                self.image_label.configure(image=image_tk_redo)
                undo_list.append(redo_list[-1])
                redo_list.pop()
            except:
                pass
        else:
            pass

    def flip_horizontally(self):
        try:
            self.image = self.image_reference.transpose(Image.FLIP_TOP_BOTTOM)
            self.image_reference = self.image
            width, height = self.image.size
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            image_tk_flip_horiz = ImageTk.PhotoImage(image=self.image_resized)
            self.image_label.image = image_tk_flip_horiz
            self.image_label.configure(image=image_tk_flip_horiz)
            undo_list.append(self.image_reference)
        except:
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def flip_vertically(self):
        try:
            self.image = self.image_reference.transpose(Image.FLIP_LEFT_RIGHT)
            self.image_reference = self.image
            width, height = self.image.size
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            image_tk_flip_vert = ImageTk.PhotoImage(image=self.image_resized)
            self.image_label.image = image_tk_flip_vert
            self.image_label.configure(image=image_tk_flip_vert)
            undo_list.append(self.image_reference)
        except:
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def rotate_right(self):
        try:
            self.image = self.image_reference.rotate(-90)
            self.image_reference = self.image
            width, height = self.image.size
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            image_tk_rotate_right = ImageTk.PhotoImage(image=self.image_resized)
            self.image_label.image = image_tk_rotate_right
            self.image_label.configure(image=image_tk_rotate_right)
            undo_list.append(self.image_reference)
        except:
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def rotate_left(self):
        try:
            self.image = self.image_reference.rotate(90)
            self.image_reference = self.image
            width, height = self.image.size
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            image_tk_rotate_left = ImageTk.PhotoImage(image=self.image_resized)
            self.image_label.image = image_tk_rotate_left
            self.image_label.configure(image=image_tk_rotate_left)
            undo_list.append(self.image_reference)
        except:
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def rotate_180(self):
        try:
            self.image = self.image_reference.rotate(180)
            self.image_reference = self.image
            width, height = self.image.size
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            image_tk_rotate_180 = ImageTk.PhotoImage(image=self.image_resized)
            self.image_label.image = image_tk_rotate_180
            self.image_label.configure(image=image_tk_rotate_180)
            undo_list.append(self.image_reference)
        except:
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def scale_image_window(self):
        # crates the top-level frame
        self.scale_frame = tk.Toplevel()
        self.scale_frame.title("Scale Image")
        self.scale_frame.geometry('250x120')

        self.label = tk.Label(self.scale_frame, text='Image Size',
                              font="Helvetica 12 bold")
        self.label.grid(row=0, column=0, padx=20)

        self.width_label = tk.Label(self.scale_frame, text='Width:')
        self.width_label.grid(row=1, column=0)

        self.width_entry = tk.Entry(self.scale_frame, width='10',
                                    font="Helvetica 11", justify="right")
        self.width_entry.grid(row=1, column=1)

        self.height_label = tk.Label(self.scale_frame, text='Height:')
        self.height_label.grid(row=2, column=0)

        self.height_entry = tk.Entry(self.scale_frame, width='10',
                                     font="Helvetica 11", justify="right")
        self.height_entry.grid(row=2, column=1)

        self.button_frame = tk.Frame(self.scale_frame)
        self.button_frame.grid(row=3, column=0, columnspan=2)

        self.ok_button = tk.Button(self.button_frame, text='  OK  ',
                                   command=self.get_scale_size)
        self.ok_button.grid(row=0, column=1, sticky='e', pady=10, padx=20)

        self.cancel_button = tk.Button(self.button_frame, text='Cancel',
                                       command=lambda: self.scale_frame.destroy())
        self.cancel_button.grid(row=0, column=0, sticky='e', pady=10, padx=5)

    def get_scale_size(self):
        try:
            self.new_width = int(self.width_entry.get())
            self.new_height = int(self.height_entry.get())
            self.scale_frame.destroy()
            self.scale_image()
        except:
            tkinter.messagebox.showwarning(title='Contrast',
                                           message='Please enter a valid ' +
                                           'width and height value',
                                           icon='error')

    def scale_image(self):
        try:
            self.image = self.image_reference.resize((self.new_width,
                                                      self.new_height),
                                                      Image.ANTIALIAS)
            self.image_reference = self.image
            image_tk_scale = ImageTk.PhotoImage(image=self.image)
            self.image_label.image = image_tk_scale
            self.image_label.configure(image=image_tk_scale)
            undo_list.append(self.image_reference)
        except:
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def contrast(self):
        self.value = tk.DoubleVar()
        # creates a top-level frame
        self.contrast_frame = tk.Toplevel()
        self.contrast_frame.title("Contrast")
        self.contrast_frame.geometry('305x120')

        self.button_frame = tk.Frame(self.contrast_frame)
        self.button_frame.grid(row=1, column=0)

        self.ok_button = tk.Button(self.button_frame, text='  OK  ',
                                   command=self.get_contrast_value)
        self.ok_button.grid(row=0, column=1, sticky='e', pady=10)

        self.cancel_button = tk.Button(self.button_frame, text='Cancel',
                                       command=lambda: \
                                           self.contrast_frame.destroy())
        self.cancel_button.grid(row=0, column=0, sticky='e', pady=10)

        self.scale_bar = tk.Scale(self.contrast_frame, length=300,
                                  from_=-100, to=100, orient='horizontal',
                                  tickinterval=50, width=20, sliderlength=20,
                                  variable = self.value)
        self.scale_bar.grid(row=0, column=0)

        self.scale_bar.set(0)

    def get_contrast_value(self):
        try:
            self.contrast_value = self.value.get()
            self.contrast_frame.destroy()
            # transforms the values between -99 an 0 into values
            # between 0.01 and 0.99 and sets the contrast value accordingly
            if -99 < self.contrast_value < 0:
                self.new_contrast_value = 1 - self.contrast_value / -100
            # if the returned value is -100, sets the contrast value at 0
            elif self.contrast_value == -100:
                self.new_contrast_value = 0
            # transforms the values between 0 an 99 into values
            # between 1.01 and 0.99 and sets the contrast value accordingly
            elif 0 < self.contrast_value < 99:
                self.new_contrast_value = 1 + self.contrast_value / 100
            # if the returned value is 100, sets the contrast value at 2
            elif self.contrast_value == 100:
                self.new_contrast_value = 2
            elif self.contrast_value == 1:
                self.new_contrast_value = 0.01
            # if the returned value is 0, sets the contrast value at 1
            # no change is applied to the image
            elif self.contrast_value == 0:
                self.new_contrast_value = 1
            else:
                pass
            self.change_contrast()
        except:
            pass

    def change_contrast(self):
        try:
            self.enhancer = ImageEnhance.Contrast(self.image_reference)
            self.image = self.enhancer.enhance(self.new_contrast_value)
            self.image_reference = self.image

            width, height = self.image.size
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            image_tk_contrast = ImageTk.PhotoImage(image=self.image_resized)
            self.image_label.image = image_tk_contrast
            self.image_label.configure(image=image_tk_contrast)
            undo_list.append(self.image_reference)
        except:
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def invert(self):
        try:
            self.image = self.image_reference
            # verifies if the image is a gray-scale image or a rgb image
            # splits and merge the image, so that the alfa channel
            # can be removed
            if self.image.mode == 'RGBA':
                self.image.load()
                r, g, b, a = self.image.split()
                self.image = Image.merge('RGB', (r, g, b))
            self.image = ImageOps.invert(self.image)

            self.image_reference = self.image
            width, height = self.image.size
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            image_tk_invert = ImageTk.PhotoImage(image=self.image_resized)
            self.image_label.image = image_tk_invert
            self.image_label.configure(image=image_tk_invert)
            undo_list.append(self.image_reference)
        except:
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def to_grayscale(self):
        try:
            self.image = self.image_reference.convert('L')
            self.image_reference = self.image
            width, height = self.image.size
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            image_tk_gray = ImageTk.PhotoImage(image=self.image_resized)
            self.image_label.image = image_tk_gray
            self.image_label.configure(image=image_tk_gray)
            undo_list.append(self.image_reference)
        except:
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')


    def blur_image(self):
        """
        these function applies a blur filter to the image
        """
        try:
            # modifies the image stored in the instance variable
            # applies the blur filter to the image
            self.image = self.image_reference.filter(ImageFilter.BLUR)
            # saves the image in an instance variable
            self.image_reference = self.image
            # sets the height and width variables equal to the
            # height and width of the image
            width, height = self.image.size
            # runs the resize image() function and returns the new image
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            # puts the PIL image into a TK PhotoImage to display it
            image_tk_blur = ImageTk.PhotoImage(image=self.image_resized)
            # keeps a reference of the PhotoImage
            self.image_label.image = image_tk_blur
            self.image_label.configure(image=image_tk_blur)
            # adds the image into a list so that it can be later
            # by the undo function used
            undo_list.append(self.image_reference)
        except:
            # a warning message box appears when the user tries to
            # manipulate an image without opening it first
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')


    def gaussian_frame(self):
        self.gaussian_radius = tk.DoubleVar()
        # creates the top-level frame
        self.gaussian_frame = tk.Toplevel()
        self.gaussian_frame.title("Gaussian Blur")
        self.gaussian_frame.geometry('305x120')
        self.button_frame = tk.Frame(self.gaussian_frame)
        self.button_frame.grid(row=1, column=0)

        self.ok_button = tk.Button(self.button_frame, text='  OK  ',
                                   command=self.get_gaussian_value)
        self.ok_button.grid(row=0, column=1, sticky='e', pady=10)

        self.cancel_button = tk.Button(self.button_frame, text='Cancel',
                                       command=lambda: \
                                       self.gaussian_frame.destroy())
        self.cancel_button.grid(row=0, column=0, sticky='e', pady=10)

        self.gaussian_bar = tk.Scale(self.gaussian_frame, length=300,
                                     from_=0, to=100, orient='horizontal',
                                     tickinterval=25, width=20, sliderlength=20,
                                     variable = self.gaussian_radius)
        self.gaussian_bar.grid(row=0, column=0)
        self.gaussian_bar.set(0)

    def get_gaussian_value(self):
        try:
            self.radius = self.gaussian_radius.get()
            self.gaussian_frame.destroy()
            self.gaussian_blur()
        except:
            pass

    def gaussian_blur(self):
        try:
            self.image = self.image_reference.filter(ImageFilter.GaussianBlur
                                                     (radius=self.radius))
            self.image_reference = self.image
            width, height = self.image.size
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            image_tk_gaussian = ImageTk.PhotoImage(image=self.image_resized)
            self.image_label.image = image_tk_gaussian
            self.image_label.configure(image=image_tk_gaussian)
            undo_list.append(self.image_reference)
        except:
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def smooth_image(self):
        try:
            self.image = self.image_reference.filter(ImageFilter.SMOOTH)
            self.image_reference = self.image
            width, height = self.image.size
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            image_tk_smooth = ImageTk.PhotoImage(image=self.image_resized)
            self.image_label.image = image_tk_smooth
            self.image_label.configure(image=image_tk_smooth)
            undo_list.append(self.image_reference)
        except:
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def find_edges(self):
        """
        these function identify the points in a digital image where
        the image brightness changes sharply
        """
        try:
            self.image = self.image_reference.filter(ImageFilter.FIND_EDGES)
            self.image_reference = self.image
            width, height = self.image.size
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            image_tk_edge = ImageTk.PhotoImage(image=self.image_resized)
            self.image_label.image = image_tk_edge
            self.image_label.configure(image=image_tk_edge)
            undo_list.append(self.image_reference)
        except:
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def image_contour(self):
        try:
            self.image = self.image_reference.filter(ImageFilter.CONTOUR)
            self.image_reference = self.image
            width, height = self.image.size
            self.image_resized = self.resize_image(width, height,
                                                   self.label_width,
                                                   self.label_height,
                                                   self.image)
            image_tk_contur = ImageTk.PhotoImage(image=self.image_resized)
            self.image_label.image = image_tk_contur
            self.image_label.configure(image=image_tk_contur)
            undo_list.append(self.image_reference)
        except:
            tkinter.messagebox.showwarning(title='No image found',
                                           message='Please open an image first',
                                           icon='error')

    def reset(self):
        self.image_label.configure(image = '')


    def help(self):
        self.help_text = open('template\help.txt', 'r')
        text = self.help_text.read()
        tkinter.messagebox.showinfo(title="Help", message=text, icon="info")

    def about(self):
        self.about_text = open('template\we.txt', 'r')
        text = self.about_text.read()
        tkinter.messagebox.showinfo(title="About", message=text, icon='info')

    
