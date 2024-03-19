# Img2pdf converter
# Author of idea: @Hanashiko
import tkinter as tk
from tkinter import filedialog

import img2pdf


class FileSelectionWindow(tk.Tk):
    allowed_ext = ["*.jpg", "*.png", "*.tiff", "*.jpeg"]

    def __init__(self):
        super().__init__()
        self.title("img2pdf - File Selection")
        self.files = []  # List to store selected files
        self.selected_index = None  # Index of the currently selected item
        self.init_ui()

    def init_ui(self):
        # Create the Listbox for displaying selected files
        self.file_list = tk.Listbox(self)
        self.file_list.pack(fill="both", expand=True)

        # Create a frame to hold the buttons
        button_frame = tk.Frame(self)
        button_frame.pack()

        # Button to select multiple image files
        select_files_button = tk.Button(
            button_frame, text="Select Files", command=self.select_files
        )
        select_files_button.pack(side=tk.LEFT, padx=5)

        # Button to select a folder containing image files
        select_folder_button = tk.Button(
            button_frame, text="Select Folder", command=self.select_folder
        )
        select_folder_button.pack(side=tk.LEFT, padx=5)

        # Button to move a selected file up in the list
        up_button = tk.Button(button_frame, text="Up", command=self.move_up)
        up_button.pack(side=tk.LEFT, padx=5)

        # Button to move a selected file down in the list
        down_button = tk.Button(button_frame, text="Down", command=self.move_down)
        down_button.pack(side=tk.LEFT, padx=5)

        # Button to remove the selected file(s) from the list
        remove_button = tk.Button(button_frame, text="Remove", command=self.remove_selected)
        remove_button.pack(side=tk.LEFT, padx=5)

        sort_button = tk.Button(button_frame, text="Sort", command=self.sort_files)
        sort_button.pack(side=tk.LEFT, padx=5)

        to_pdf = tk.Button(button_frame, text="Save to pdf", command=self.save_to_pdf)
        to_pdf.pack(side=tk.LEFT, padx=5)

    def save_to_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        images = self.files
        pdf = img2pdf.convert(images)
        with open(file_path, "wb") as file:
            file.write(pdf)

    def sort_files(self):
        # Determine the sort order reverse/straight
        is_sorted = all(self.files[i] <= self.files[i + 1] for i in range(len(self.files) - 1))
        # Save the selected item name to restore selection
        selected_index = self.file_list.curselection()
        name = None
        if selected_index:
            name = self.files[int(selected_index[0])]
        # Sort list
        if is_sorted:
            self.files.sort(reverse=True)
        else:
            self.files.sort()
        self.update_list()
        # Restore selection
        if name:
            idx = self.files.index(name)
            self.file_list.select_set(idx)

    def remove_selected(self):
        # Get the currently selected index
        selected_index = self.file_list.curselection()
        if selected_index:
            index = int(selected_index[0])
            del self.files[index]
            self.update_list()
            if len(self.files) != 0:
                if len(self.files) - 1 < index:
                    self.file_list.select_set(len(self.files) - 1)
                else:
                    self.file_list.select_set(index)

    def select_files(self):
        # Open a file selection dialog allowing multiple image file selection (JPG and PNG)
        extensions = ";".join(self.allowed_ext)
        filenames = filedialog.askopenfilenames(title="Select Images", filetypes=[("Images", extensions)])
        self.add_files(filenames)

    def select_folder(self):
        # Open a folder selection dialog
        folder_path = filedialog.askdirectory(title="Select Folder")
        if folder_path:
            # Add all image files from the selected folder using a custom function
            for file in self.get_image_files(folder_path):
                self.files.append(file)
            self.update_list()

    def get_image_files(self, folder_path):
        # This function can be customized to filter based on specific image formats or extensions
        from glob import glob

        filtered_files = []
        for ext in self.allowed_ext:
            filtered_files.extend(glob(f"{folder_path}/{ext}"))

        return filtered_files

    def add_files(self, filenames):
        # Add unique files to the list to avoid duplicates
        for filename in filenames:
            if filename not in self.files:
                self.files.append(filename)
        self.update_list()

    def update_list(self):
        # Clear the Listbox and repopulate it with the updated list of files
        self.file_list.delete(0, tk.END)
        for file in self.files:
            self.file_list.insert(tk.END, file)
            # Reset selected index after update
            self.selected_index = None

    def move_up(self):
        # Get the currently selected index
        selected_index = self.file_list.curselection()
        if selected_index:
            index = int(selected_index[0])
            # Check if the selected item is not already at the top
            if index > 0:
                # Swap the positions of the selected item and the item above it
                self.files[index], self.files[index - 1] = self.files[index - 1], self.files[index]
                # Update the Listbox and maintain selection
                self.update_list()
                self.file_list.select_set(index - 1)

    def move_down(self):
        # Get the currently selected index
        selected_index = self.file_list.curselection()
        if selected_index:
            index = int(selected_index[0])
            print(index)
            # Check if the selected item is not already at the top
            if index < len(self.files) - 1:
                self.files[index], self.files[index + 1] = self.files[index + 1], self.files[index]
                # Update the Listbox and maintain selection
                self.update_list()
                self.file_list.select_set(index + 1)


if __name__ == "__main__":
    fd = FileSelectionWindow()
    fd.mainloop()
