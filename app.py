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
st.sidebar.image("./img/亞東醫院logo.png", use_container_width=True) 
st.sidebar.header("操作說明")

st.sidebar.markdown("""
    ## 📌 EDF 檔案管理系統  
    - 選擇您要計算的 **EDF (European Data Format) 檔案**
    - 確認上傳文件後，按下 **計算**
    - 一次上傳 同位病患、同一天的資料可以選擇 **多檔** 合併計算
""")
if st.sidebar.button(label="設定", icon="🔥", type="secondary"):
    st.sidebar.write("設定")


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
if uploaded_files:
    # 創建選擇計算方式的選單
    st.write("🔽 **請選擇每個檔案是否參與多檔計算**")

    # 生成選擇框
    file_selection = {}
    for uploaded_file in uploaded_files:
        file_selection[uploaded_file.name] = st.selectbox(
            f"是否計算 {uploaded_file.name}？",
            ["否", "是"]
        )
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


agree = st.checkbox("我同意條款")
if agree:
    st.write("謝謝您的同意！")
