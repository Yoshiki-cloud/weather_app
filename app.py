import streamlit as st
import requests

# 画面の設定
st.set_page_config(page_title="朝の1秒チェックボード", page_icon="☀️")
st.title("☀️ 朝の1秒チェックボード")

# 1. お天気データの取得（東京エリアの座標をより精密に設定）
LATITUDE = 35.6762
LONGITUDE = 139.6503
url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&daily=weather_code,temperature_2m_max,precipitation_probability_max&timezone=Asia%2FTokyo&forecast_days=2"

try:
    # タイムアウト（5秒待ってもダメなら諦める設定）を追加して接続を安定させる
    response = requests.get(url, timeout=5).json()
    
    if "daily" in response:
        tomorrow_temp = response["daily"]["temperature_2m_max"][1]
        tomorrow_rain_prob = response["daily"]["precipitation_probability_max"][1]
        tomorrow_code = response["daily"]["weather_code"][1]
        
        if tomorrow_code in [0, 1]: weather_text = "晴れ ☀️"
        elif tomorrow_code in [2, 3]: weather_text = "曇り ☁️"
        else: weather_text = "雨・雪 ☔"

        # 2. 画面へ表示
        st.subheader("🌈 明日の天気予報")
        col1, col2, col3 = st.columns(3)
        col1.metric("天気", weather_text)
        col2.metric("最高気温", f"{tomorrow_temp} ℃")
        col3.metric("降水確率", f"{tomorrow_rain_prob} %")

        st.markdown("---")

        # 3. 自動持ち物アドバイス
        st.markdown("### 🎒 明日のマスト持ち物")
        if tomorrow_rain_prob >= 40:
            st.error("☔ 降水確率が高めです！折りたたみ傘をカバンに入れましたか？")
        else:
            st.success("✨ 傘は持って行かなくても大丈夫そうです！")
            
        if tomorrow_temp <= 20:
            st.warning("🧥 最高気温が20度以下です。薄手の上着を忘れずに！")
    else:
        st.error(f"APIからの応答が不正です: {response}")

except Exception as e:
    # エラーの具体的な理由を画面に出すようにして原因を特定しやすくします
    st.error(f"お天気データの取得に失敗しました。理由: {e}")

# 4. 定番チェックリスト
st.markdown("---")
st.markdown("### ✅ お出かけ前最終チェック")
st.checkbox("スマホの充電はバッチリ？")
st.checkbox("財布と家の鍵は持った？")

if st.button("準備完了！いってきます 🚀"):
    st.balloons()