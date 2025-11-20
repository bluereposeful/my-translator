import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
import io
from streamlit_mic_recorder import mic_recorder

st.set_page_config(page_title="Gemini 手機口譯", page_icon="🌍")
st.title("🌍 Gemini 手機即時口譯")

# --- 設定區 ---
with st.expander("🛠️ 設定與 API Key (點擊展開)", expanded=True):
    api_key = st.text_input("Gemini API Key", type="password", placeholder="貼上你的 AIza...金鑰")
    target_lang = st.selectbox("目標語言", ["英文", "日文", "韓文", "繁體中文"])

lang_map = {
    "英文": {"code": "en", "prompt": "English"},
    "日文": {"code": "ja", "prompt": "Japanese"},
    "韓文": {"code": "ko", "prompt": "Korean"},
    "繁體中文": {"code": "zh-TW", "prompt": "Traditional Chinese"}
}

# --- 核心邏輯 ---
def translate_audio(audio_bytes, target_info):
    if not api_key:
        st.error("❌ 請先輸入 API Key")
        return

    # 1. 語音轉文字 (STT)
    r = sr.Recognizer()
    try:
        # 使用 io.BytesIO 處理音訊流
        audio_file = sr.AudioFile(io.BytesIO(audio_bytes))
        with audio_file as source:
            audio_data = r.record(source)
            # 預設聽中文
            text = r.recognize_google(audio_data, language="zh-TW")
            st.success(f"👂 聽到: {text}")
    except Exception as e:
        st.warning(f"無法辨識語音，可能太小聲或格式問題。({e})")
        return

    # 2. Gemini 翻譯 (LLM)
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"Translate '{text}' to {target_info['prompt']}. Output only translation.")
        translated_text = response.text.strip()
        st.markdown(f"### 🗣️ 翻譯: {translated_text}")
    except Exception as e:
        st.error(f"Gemini 翻譯失敗: {e}")
        return

    # 3. 文字轉語音 (TTS)
    try:
        tts = gTTS(text=translated_text, lang=target_info['code'])
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        st.audio(mp3_fp, format='audio/mp3', start_time=0)
    except Exception as e:
        st.warning(f"語音播放失敗: {e}")

# --- 主介面 ---
try:
    st.write("👇 點擊按鈕開始錄音：")
    # 網頁版錄音按鈕
    audio = mic_recorder(
        start_prompt="🔴 錄音 (點擊開始)",
        stop_prompt="⏹️ 停止 (點擊結束)",
        key='recorder'
    )

    if audio:
        target_info = lang_map[target_lang]
        translate_audio(audio['bytes'], target_info)

except Exception as e:
    st.error(f"發生未預期的錯誤: {e}")
