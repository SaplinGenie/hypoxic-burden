from pyedflib import highlevel
import pyedflib
import streamlit as st
from config import Action 
import os
import io
import tempfile
import numpy as np
import pandas as pd
from process import Calculate

# Initialize database connection
action = Action()
calculate = Calculate()

# Streamlit UI
st.title("HB-sys")

# Sidebar
st.sidebar.header("操作說明")
st.sidebar.write("This is a sidebar example.")
st.sidebar.image("example.png", use_container_width=True, caption="Example Image") 
st.sidebar.markdown("""
    ## 📌 EDF 檔案管理系統  
    - 上傳 **EDF (European Data Format) 檔案**
    - 儲存 **EDF 檔案** 於 SQLite
    - 下載 **已上傳的 EDF 檔案**
""")

# Step 1-1: Browse Files
st.subheader("📂 Step 1: 請選擇文件")
uploaded_files = st.file_uploader(label="Choose files",
                                  type=["edf"],
                                  accept_multiple_files=True,
                                  label_visibility="hidden"
                    )

# Step 1-2: insert file
if st.button("查看資料庫"):
    df = action.get_existed_data()
    st.write(df)



# Step 2: Process EDF Files
st.subheader("🔮 Step 2: 開始計算 EDF")

# Step 2-1: Process EDF Files
if st.button("計算"):
    existed_files = set(action.get_existed_files())  # 從資料庫取得已存在的檔案名稱

    if uploaded_files:

        for uploaded_file in uploaded_files:
            st.write(uploaded_file.name)
            try:
                # 建立一個臨時檔案，並寫入上傳的內容
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmpfile:
                    tmpfile.write(uploaded_file.read())
                    file_path = tmpfile.name  # 取得檔案路徑

                # 顯示檔案儲存位置
                result = calculate.convert_signal(file_path)
                st.write(result)
                st.success(f"✅ 計算完成！")


                # 比對準備上傳和資料庫的檔案是否已存在
                if any(uploaded_file.name == item[0] for item in existed_files):
                    pass
                else:
                    action.insert_files(uploaded_file.name, result[2], result[2])

            except Exception as e:
                st.error(f"❌ 解析 {uploaded_file.name} 時發生錯誤: {str(e)}")








#     if db_files.empty:
#         st.warning("資料庫中沒有檔案，請先上傳！")
#     else:
#         results = []
#         for index, row in db_files.iterrows():
#             file_id, filename = row["id"], row["filename"]
            
#             # Retrieve binary file from database
#             cursor = action.conn.cursor()
#             cursor.execute("SELECT filedata FROM temp_files WHERE id=?", (file_id,))
#             file_data = cursor.fetchone()[0]

#             # Write file to temporary directory
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".edf") as temp_file:
#                 temp_file.write(file_data)
#                 temp_file_path = temp_file.name

#             # # Process the EDF file
#             # try:
#             #     result = calculate.convert_signal(temp_file_path)
#             #     results.append(result)
#             # except Exception as e:
#             #     st.error(f"處理檔案 {filename} 時發生錯誤: {e}")

#         # Display results
#         if results:
#             df_results = pd.DataFrame(results, columns=["File Name", "Res", "Total Duration", "Processed Value"])
#             st.write(df_results)