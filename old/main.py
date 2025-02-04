import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttkb
from process import convert_signal


# Define the main application
window = ttkb.Window(themename='litera')
window.geometry("800x600")
window.title("EDF File Viewer and Processor")

uploaded_files = []  # A global list to keep track of uploaded file names


def upload_files():
    """
    Upload EDF files and list them without processing.
    """
    global uploaded_files
    file_names = filedialog.askopenfilenames(filetypes=[("EDF files", "*.edf")])
    if not file_names:
        return
    try:
        new_files = [file for file in file_names if file not in uploaded_files]
        if not new_files:
            messagebox.showinfo("Info", "已有重複文件上傳！")
            return
        
        uploaded_files.extend(new_files)
        update_file_list()
        messagebox.showinfo("Info", "文件上傳成功！")
    except Exception as e:
        messagebox.showerror("Error", f"文件上傳失敗，原因： {e}")


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
        messagebox.showwarning("Warning", "請選取要刪除的文件！")
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
        messagebox.showwarning("Warning", "請上傳文件！")
        return
    try:
        # Clear previous results
        for widget in results_scrollable_frame.winfo_children():
            widget.destroy()

        for file in uploaded_files:
            result = convert_signal(file)

            file_label = ttkb.Label(results_scrollable_frame, text=f"檔案名稱: {result[3]}", style='Secondary.TLabel')
            file_label.pack(anchor="w", pady=2)

            area_label = ttkb.Label(results_scrollable_frame, text=f"面積大小: {result[0]}")
            area_label.pack(anchor="w", pady=2)

            duration_label = ttkb.Label(results_scrollable_frame, text=f"持續秒數(s): {result[1]}")
            duration_label.pack(anchor="w", pady=2)

            value_label = ttkb.Label(results_scrollable_frame, text=f"數值結果: {result[2]}")
            value_label.pack(anchor="w", pady=2)

            separator = ttkb.Separator(results_scrollable_frame, orient="horizontal")
            separator.pack(fill="x", pady=5)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to calculate results: {e}")


# Widgets
file_listbox = tk.Listbox(window, height=8, width=80, selectmode="single")

upload_button = ttkb.Button(text="選擇上傳文件", command=upload_files, style='Outline.TButton')
remove_button = ttkb.Button(text="刪除文件", command=remove_selected_file, style='Outline.TButton')
confirm_button = ttkb.Button(window, text="開始計算", command=calculate_all_files, style='Primary.TButton')

topic_label = ttkb.Label(text="This is an application agent which can help user to calculate Hypoxic burden.", style='Secondary.TLabel')
file_list_label = ttkb.Label(window, text="請選擇上傳文件 (限EDF格式)")

results_label = ttkb.Label(window, text="計算結果")

# Scrollable frame for results
results_canvas = tk.Canvas(window)
results_scrollbar = ttkb.Scrollbar(window, orient="vertical", command=results_canvas.yview)
results_scrollable_frame = ttkb.Frame(results_canvas)

results_scrollable_frame.bind(
    "<Configure>",
    lambda e: results_canvas.configure(scrollregion=results_canvas.bbox("all"))
)

results_canvas.create_window((0, 0), window=results_scrollable_frame, anchor="nw")
results_canvas.configure(yscrollcommand=results_scrollbar.set)

# Grid layout
topic_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")
file_list_label.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")
file_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

upload_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
remove_button.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
confirm_button.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")

results_label.grid(row=5, column=0, columnspan=2, pady=5, sticky="w")
results_canvas.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
results_scrollbar.grid(row=6, column=2, sticky="ns")

# Configure row/column weights for resizing
window.grid_rowconfigure(6, weight=1)  # Allow results to expand vertically
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

window.mainloop()
