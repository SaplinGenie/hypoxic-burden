import streamlit as st
import os
import tempfile
import numpy as np
import pandas as pd

from config import Action                # 資料庫操作模組
from calculate_v1 import Calculate       # 第一版演算法（保留）
from calculate_v2 import Calculate_v2    # 改用 mne 的演算法

# 初始化元件
action = Action()
calculate = Calculate()
calculate_v2 = Calculate_v2()

st.set_page_config(page_title="hypoxic-burden calculation", page_icon=":bar_chart:", layout="wide")

# UI 標題
st.title("Hypoxic Burden: Calculation and Analysis")

# Sidebar 操作說明
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

# Step 1-1: 選擇檔案
st.subheader("📂 Step 1: 請選擇文件")
uploaded_files = st.file_uploader(label="Choose files",
                                  type=["edf"],
                                  accept_multiple_files=True,
                                  label_visibility="hidden")

# Step 1-2: 檢視資料庫現有資料
if st.button("查看資料庫"):
    df = action.get_existed_data()
    st.write(df)

# Step 2: 開始計算
st.subheader("📂 Step 2: 開始計算 EDF")

if uploaded_files:
    st.write("🔽 **請選擇每個檔案是否參與多檔計算**")

if st.button("計算"):
    existed_files = set(action.get_existed_files())  # 資料庫中已有檔案名稱

    for uploaded_file in uploaded_files:
        st.write(f"📄 檔案名稱：{uploaded_file.name}")
        try:
            # 儲存至暫存路徑
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmpfile:
                tmpfile.write(uploaded_file.read())
                file_path = tmpfile.name

            # 執行第二種計算法（mne）
            matched_signals = calculate_v2.get_signal(file_path, ["Saturation", "Desaturation"])
            if matched_signals is None:
                st.warning(f"⚠️ 檔案 `{uploaded_file.name}` 中找不到 `Saturation` 或 `Desaturation` 通道，已跳過。")
                continue

            area, time127 = calculate_v2.get_area(matched_signals)
            time = calculate_v2.get_time(matched_signals, "Saturation", time127)
            result = calculate_v2.cal_result(time, area)

            # 顯示結果
            st.write("🕒 時間：", time)
            st.write("📐 區域：", area)
            st.write("📊 計算結果：", result)
            st.success(f"✅ {uploaded_file.name} 計算完成！")

            # 寫入資料庫（避免重複）
            if uploaded_file.name not in [item[0] for item in existed_files]:
                action.insert_files(uploaded_file.name, result, result)

        except Exception as e:
            st.error(f"❌ 解析 `{uploaded_file.name}` 時發生錯誤：{str(e)}")

# 勾選同意條款
agree = st.checkbox("我同意條款")
if agree:
    st.write("謝謝您的同意！")

# UI 裝飾用的 CSS
st.markdown(
    """
    <style>
    .element-container:has(style){
        display: none;
    }
    #button-after {
        display: none;
    }
    .element-container:has(#button-after) {
        display: none;
    }
    .element-container:has(#button-after) + div button {
        background-color: orange;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)
st.button("My Button")
