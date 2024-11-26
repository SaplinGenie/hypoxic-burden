import tkinter as tk
from tkinter import filedialog, messagebox
from pyedflib import highlevel
import pandas as pd
import ttkbootstrap as ttkb

from process import convert_signal





# Define the main application
window = ttkb.Window(themename = 'litera')
window.geometry("1000x1000")
My_Label = ttkb.Label(text = "This is an application agent which can help user to calculate xxxxx.")
My_Label.pack()
window.title("EDF File Viewer and Processor")

uploaded_files = []  # A global list to keep track of uploaded file names

result_labels = {
    "file_name": ttkb.Label(window, text="File Name: ", font=("Helvetica", 12)),
    "raw_data": ttkb.Label(window, text="Raw Data (Area): ", font=("Helvetica", 12)),
    "total_duration": ttkb.Label(window, text="Total Duration (s): ", font=("Helvetica", 12)),
    "processed_value": ttkb.Label(window, text="Processed Value: ", font=("Helvetica", 12))
}



def upload_files():
    """
    Upload EDF files and list them without processing.
    """
    global uploaded_files
    file_names = filedialog.askopenfilenames(filetypes=[("EDF files", "*.edf")])
    if not file_names:
        return
    try:
        # Filter out duplicates
        new_files = [file for file in file_names if file not in uploaded_files]
        if not new_files:
            messagebox.showinfo("Info", "No new files to upload. All selected files are already uploaded.")
            return
        
        # Add only new files to the list
        uploaded_files.extend(new_files)

         # Update the Listbox with the new files
        update_file_list()
        messagebox.showinfo("Info", "Files uploaded successfully! Confirm and calculate when ready.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to upload files: {e}")



def update_file_list():
    """
    Refresh the Listbox with the current list of uploaded files.
    """
    file_listbox.delete(0, "end")  # Clear the Listbox
    for file_name in uploaded_files:
        file_listbox.insert("end", file_name)  # Add each file name to the Listbox



def remove_selected_file():
    """
    Remove the selected file from the list.
    """
    global uploaded_files
    selected_index = file_listbox.curselection()  # Get the index of the selected file
    if not selected_index:
        messagebox.showwarning("Warning", "No file selected for removal!")
        return
    
    # Remove the selected file from the list and refresh the Listbox
    file_to_remove = file_listbox.get(selected_index)
    uploaded_files.remove(file_to_remove)
    update_file_list()



def calculate_all_files():
    """
    Process all confirmed uploaded files and display the results.
    """
    global uploaded_files
    if not uploaded_files:
        messagebox.showwarning("Warning", "No files uploaded to calculate!")
        return
    try:
        results = []
        for file in uploaded_files:
            result = convert_signal(file)
    
            results.append(f"File: {file}\n"
                           f"依面積大小: {result[0]}\n"
                           f"Total Duration (s): {result[1]}\n"
                           f"Processed Value: {result[2]}\n")
        
        print(results)
        # Display results for all processed files
        results_text.delete("1.0", tk.END)
        results_text.insert("1.0", "\n".join(results))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to calculate results: {e}")





# widgets
# File list section
file_list_label = ttkb.Label(window, text="Uploaded Files:")
file_list_label.pack(pady=5)

file_listbox = tk.Listbox(window, height=10, width=80, selectmode="single")
file_listbox.pack(padx=10, pady=5)

# Buttons
upload_button = ttkb.Button(window, text="Upload EDF Files", command=upload_files, style='Outline.TButton')
upload_button.pack(pady=5)

remove_button = ttkb.Button(window, text="Remove Selected File", command=remove_selected_file, style='Outline.TButton')
remove_button.pack(pady=5)

confirm_button = ttkb.Button(window, text="Confirm and Calculate", command=calculate_all_files, style='Primary.TButton')
confirm_button.pack(pady=5)

# Results display
results_label = tk.Label(window, text="Processing Results:")
results_label.pack(pady=5)

results_text = tk.Text(window, wrap="word", height=10, width=80)
results_text.pack(padx=10, pady=5, fill="both", expand=True)

# for label in result_labels.values():
#     label.pack(pady=5)

# Run the GUI event loop
window.mainloop()


    # f"Raw Data (原始數據計算後的面積): {res}\n" \
    #          f"Total Duration(s) (需要計算的秒數): {total_duration}\n" \
    #          f"Processed Value (最終計算結果): {processed_value}\n" \
    #          f"Filename (上傳的檔案名稱): {file}"