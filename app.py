import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ExifTags
import numpy as np
import base64
from io import BytesIO

# --- Page Configuration ---
st.set_page_config(
    page_title="無料OCRツール - 画像/カメラからテキスト抽出",
    page_icon="📷",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/naptha/tesseract.js',
        'Report a bug': "https://github.com/streamlit/streamlit/issues",
        'About': "無料のオンラインOCRツールです。Tesseract.jsを使用し、ブラウザ上で安全に処理されます。"
    }
)

# --- AdSense Script Injection (Head) ---
components.html("""
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4443417103189902"
     crossorigin="anonymous"></script>
""", height=0)

# --- SEO & AdSense Meta Tags ---
st.markdown("""
<meta name="description" content="無料オンラインOCRツール。Tesseract.jsを使用してブラウザ上で画像からテキストを抽出。インストール不要、プライバシー重視。">
""", unsafe_allow_html=True)

# --- Helper Functions ---
def correct_orientation(image):
    """
    Corrects the orientation of an image based on its EXIF data.
    """
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                exif = image._getexif()
                if exif is not None:
                    exif = dict(exif.items())
                    if orientation in exif:
                        orientation_value = exif[orientation]
                        if orientation_value == 3:
                            image = image.rotate(180, expand=True)
                        elif orientation_value == 6:
                            image = image.rotate(270, expand=True)
                        elif orientation_value == 8:
                            image = image.rotate(90, expand=True)
                        break
    except Exception:
        pass
    return image

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# --- UI Layout ---

st.title("📷 無料OCRツール (Browser-based)")
st.write("画像またはカメラからテキストを抽出します。処理はすべてお使いのブラウザ内で行われます。")

# --- Input Method Selection ---
input_method = st.radio("入力方法を選択:", ("画像アップロード", "カメラ撮影"), horizontal=True)

image_file = None

if input_method == "画像アップロード":
    image_file = st.file_uploader("画像をアップロード (JPG, PNG)", type=['jpg', 'png', 'jpeg'])
else:
    image_file = st.camera_input("カメラで撮影")
    if not image_file:
         st.info("💡 ヒント: 文字が鮮明に写るように撮影してください。")

# --- OCR Processing with Tesseract.js ---
if image_file is not None:
    try:
        bytes_data = image_file.getvalue()
        image = Image.open(BytesIO(bytes_data))
        image.verify()
        image = Image.open(BytesIO(bytes_data)) # Re-open
        
        # Orientation correction
        image = correct_orientation(image)
        
        # Display Image
        st.image(image, caption=f'入力画像 ({image.size[0]}x{image.size[1]})', use_container_width=False)
        
        # Convert to Base64 for JS
        img_base64 = image_to_base64(image)
        
        if st.checkbox("テキストを抽出する", value=True):
            st.info("ブラウザでOCR処理を実行中... 数秒お待ちください。")
            
            # Embed Tesseract.js logic
            # Note: We use a CDN for tesseract.js.
            # We display the result inside this iframe.
            components.html(f"""
            <!DOCTYPE html>
            <html>
            <head>
                <script src='https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js'></script>
                <style>
                    body {{ font-family: sans-serif; margin: 0; padding: 10px; }}
                    #progress {{ margin-bottom: 10px; color: #666; font-size: 0.9em; }}
                    #result-area {{ width: 100%; height: 300px; padding: 10px; box-sizing: border-box; border: 1px solid #ddd; border-radius: 5px; font-family: monospace; white-space: pre-wrap; overflow-y: auto; }}
                    button {{ padding: 8px 16px; background-color: #ff4b4b; color: white; border: none; border-radius: 4px; cursor: pointer; margin-top: 10px; }}
                    button:hover {{ background-color: #ff3333; }}
                </style>
            </head>
            <body>
                <div id="progress">準備中...</div>
                <textarea id="result-area" placeholder="ここに抽出されたテキストが表示されます..."></textarea>
                <button onclick="copyText()">テキストをコピー</button>

                <script>
                    const imgBase64 = "data:image/png;base64,{img_base64}";
                    const progressDiv = document.getElementById('progress');
                    const resultArea = document.getElementById('result-area');

                    (async () => {{
                        try {{
                            progressDiv.textContent = "OCRエンジンを読み込み中...";
                            
                            const worker = await Tesseract.createWorker('jpn+eng', 1, {{
                                logger: m => {{
                                    if (m.status === 'recognizing text') {{
                                        progressDiv.textContent = `処理中: ${{(m.progress * 100).toFixed(1)}}%`;
                                    }} else {{
                                        progressDiv.textContent = `ステータス: ${{m.status}}`;
                                    }}
                                }}
                            }});
                            
                            progressDiv.textContent = "解析中...";
                            const {{ data: {{ text }} }} = await worker.recognize(imgBase64);
                            
                            resultArea.value = text;
                            progressDiv.textContent = "完了しました！";
                            await worker.terminate();
                            
                        }} catch (error) {{
                            console.error(error);
                            progressDiv.textContent = "エラーが発生しました: " + error.message;
                        }}
                    }})();

                    function copyText() {{
                        const copyText = document.getElementById("result-area");
                        copyText.select();
                        copyText.setSelectionRange(0, 99999); 
                        navigator.clipboard.writeText(copyText.value).then(() => {{
                            alert("コピーしました");
                        }});
                    }}
                </script>
            </body>
            </html>
            """, height=500, scrolling=True)

            # --- AdSense Ad Unit (Below Results) ---
            st.markdown("---")
            st.caption("広告")
            components.html("""
            <ins class="adsbygoogle"
                    style="display:block"
                    data-ad-client="ca-pub-4443417103189902"
                    data-ad-slot="YOUR_AD_UNIT_ID_HERE"
                    data-ad-format="auto"
                    data-full-width-responsive="true"></ins>
            <script>
                    (adsbygoogle = window.adsbygoogle || []).push({});
            </script>
            """, height=250)

    except Exception as e:
        st.error(f"エラー: {e}")

# --- Footer / Extras ---
st.markdown("---")

# AdSense Footer Unit
st.caption("広告")
components.html("""
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-4443417103189902"
     data-ad-slot="YOUR_AD_UNIT_ID_HERE"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
""", height=250)

# Privacy Policy
st.markdown("---")

st.markdown("""
### プライバシーポリシー
- **OCR処理**: Tesseract.jsを使用し、**お客様のブラウザ内ですべて処理されます**。画像データが外部サーバーに送信されることはありません。
- **広告**: Google AdSenseを使用しています。
""")

st.caption("© 2024 無料OCRツール")
