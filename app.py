import streamlit as st

st.set_page_config(page_title="測試中")
st.title("✅ 網站復活了！")
st.write("如果你看得到這行字，代表雲端環境是正常的，是原本的程式碼某個套件衝到了。")

try:
    import google.generativeai
    st.success("1. Google AI 套件：正常")
except Exception as e:
    st.error(f"1. Google AI 套件：失敗 ({e})")

try:
    import speech_recognition
    st.success("2. 語音辨識套件：正常")
except Exception as e:
    st.error(f"2. 語音辨識套件：失敗 ({e})")

try:
    from gtts import gTTS
    st.success("3. 文字轉語音套件：正常")
except Exception as e:
    st.error(f"3. 文字轉語音套件：失敗 ({e})")

try:
    from streamlit_mic_recorder import mic_recorder
    st.success("4. 錄音套件：正常")
except Exception as e:
    st.error(f"4. 錄音套件：失敗 ({e})")
