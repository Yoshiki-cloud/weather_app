import streamlit as st
import requests

# 画面の設定
st.set_page_config(page_title="朝の1秒チェックボード", page_icon="☀️")
st.title("☀️ 朝の1秒チェックボード")

# 1. 気象庁のAPIから東京（130000）のデータを取得
# 完全無料で制限が非常に緩い安定したデータソースです
url = "https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json"

try:
    response = requests.get(url, timeout=5).json()
    
    # 東京地方（伊豆諸島などを除く本州側）の予報をピックアップ
    area_data = response[0]["timeSeries"][0]["areas"][0]
    
    # 「明日」のデータを取得
    tomorrow_weather = response[0]["timeSeries"][0]["areas"][0]["weathers"][1]
    
    # 降水確率のデータ（明日の午前・午後で一番高い値を採用）
    # ※気象庁のデータ構造に合わせて調整しています
    rain_pops = response[0]["timeSeries"][1]["areas"][0]["pops"]
    # 明日の時間帯（通常インデックス3〜5あたり）の最大値を取得
    tomorrow_rain_prob = max([int(p) for p in rain_pops[2:6]]) if len(rain_pops) >= 6 else 30
    
    # 気温データ（明日の最高気温）
    # ※予報タイミングによってデータ位置が変わるため、安全に取得
    temp_url = "https://www.jma.go.jp/bosai/forecast/data/overview_forecast/130000.json"
    temp_text = tomorrow_weather  # 天気文字列

    # 2. 画面へ表示
    st.subheader("🌈 明日の天気予報（気象庁データ）")
    col1, col2 = st.columns(2)
    col1.metric("天気", tomorrow_weather)
    col2.metric("降水確率 (最大)", f"{tomorrow_rain_prob} %")

    st.markdown("---")

    # 3. 自動持ち物アドバイス
    st.markdown("### 🎒 明日のマスト持ち物")
    if tomorrow_rain_prob >= 40 or "雨" in tomorrow_weather:
        st.error("☔ 傘マークが入っているか、降水確率が高めです！折りたたみ傘をカバンにどうぞ。")
    else:
        st.success("✨ 傘は持って行かなくても大丈夫そうです！")
        
except Exception as e:
    st.error(f"お天気データの取得に失敗しました。理由: {e}")

# 4. 定番チェックリスト
st.markdown("---")
st.markdown("### ✅ お出かけ前最終チェック")
st.checkbox("スマホの充電はバッチリ？")
st.checkbox("財布と家の鍵は持った？")

if st.button("準備完了！いってきます 🚀"):
    st.balloons()