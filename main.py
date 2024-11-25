import tkinter as tk
from tkinter import filedialog, messagebox
from pyedflib import highlevel
import pandas as pd
import ttkbootstrap as ttkb

from process import convert_signal



# Define the main application
window = ttkb.Window(themename = 'litera')
window.geometry("800x600")
My_Label = ttkb.Label(text = "This is an application agent which can help user to calculate xxxxx.")
My_Label.pack()
window.title("EDF File Viewer and Processor")



# define functions
def upload_file():
    file_name = filedialog.askopenfilename(filetypes=[("EDF files", "*.edf")])
    if not file_name:
        return
    try:
        # Process the file
        result = convert_signal(file_name)
        text_area.delete("1.0", tk.END)
        text_area.insert(tk.END, result)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process file: {e}")




# widgets
upload_button = ttkb.Button(window, text="Upload EDF File", command=upload_file, style='Outline.TButton')
upload_button.pack(pady=20)


text_area = tk.Text(window, wrap=ttkb.WORD, height=20, width=100)
text_area.pack(padx=20, pady=20, fill=ttkb.BOTH, expand=True)

check_button = ttkb.Button(window, text="enter", command="test", style='Outline.TButton')
check_button.pack(pady=20)


# text_area = ttkb.Label(window, text=ttkb.WORD, style='Inverse.TLabel')
# text_area.pack(padx=20, pady=20, fill=ttkb.BOTH, expand=True)

window.mainloop()



    # f"Raw Data (原始數據計算後的面積): {res}\n" \
    #          f"Total Duration(s) (需要計算的秒數): {total_duration}\n" \
    #          f"Processed Value (最終計算結果): {processed_value}\n" \
    #          f"Filename (上傳的檔案名稱): {file}"