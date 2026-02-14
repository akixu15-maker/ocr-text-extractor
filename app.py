import streamlit as st
import streamlit.components.v1 as components
import pytesseract
from PIL import Image, ExifTags
import numpy as np
import cv2
import sys
import os
from io import BytesIO

# --- Page Configuration ---
st.set_page_config(
    page_title="無料OCRツール - 画像/カメラからテキスト抽出",
    page_icon="📷",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/tesseract-ocr/tesseract',
        'Report a bug': "https://github.com/streamlit/streamlit/issues",
        'About': "無料のオンラインOCRツールです。Tesseract OCRを使用しています。"
    }
)

# --- AdSense Script Injection (Head) ---
components.html("""
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4443417103189902"
     crossorigin="anonymous"></script>
""", height=0)

# --- SEO & AdSense Meta Tags (Injected via Markdown) ---
st.markdown("""
<meta name="description" content="無料オンラインOCRツール。写真やカメラからテキストを簡単に抽出。日本語と英語に対応。">
""", unsafe_allow_html=True)

# --- Tesseract Configuration ---
# Set Tesseract path explicitly for Linux (Render/Streamlit Cloud)
if sys.platform.startswith('linux'):
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# For Windows, try to find it in common locations
if sys.platform.startswith('win'):
    sub_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.join(os.getenv('LOCALAPPDATA', ''), r'Tesseract-OCR\tesseract.exe')
    ]
    found = False
    for path in sub_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            found = True
            break
    
    if not found:
        # Fallback: check if 'tesseract' is in PATH
        try:
            import subprocess
            subprocess.run(['tesseract', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except FileNotFoundError:
            # We will show a warning later in the UI if needed, or just let it fail naturally
            pass

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

# --- UI Layout ---

st.title("📷 無料OCRツール")
st.write("画像またはカメラからテキストを抽出します。")

# --- Input Method Selection ---
input_method = st.radio("入力方法を選択:", ("画像アップロード", "カメラ撮影"), horizontal=True)

image_file = None

if input_method == "画像アップロード":
    image_file = st.file_uploader("画像をアップロード (JPG, PNG)", type=['jpg', 'png', 'jpeg'])
else:
    image_file = st.camera_input("カメラで撮影")
    st.info("💡 ヒント: 文字が鮮明に写るように撮影してください。暗い場所や手ブレにご注意ください。")

# --- Processing Options ---
high_quality = st.checkbox("高精度モード (画質優先)", value=True, help="オンにすると、画像を縮小せずに元の解像度でOCR処理を行います。処理に時間がかかる場合がありますが、精度が向上します。")

# --- OCR Processing ---
if image_file is not None:
    image = None
    try:
        bytes_data = image_file.getvalue()
        image = Image.open(BytesIO(bytes_data))
        # Verify if the image is valid
        # This is important to catch non-image files before processing
        image.verify() 
        # Re-open the image after verification because verify() moves the cursor to the end
        image = Image.open(BytesIO(bytes_data))
    except Exception as e:
        st.error(f"画像を識別できません: {str(e)}。JPG/PNG形式の有効な画像をお試しください。")
        image = None

    if image is not None:
        # Correct orientation based on EXIF data
        image = correct_orientation(image)

        # High Quality Mode Logic
        if not high_quality:
            # Resize for speed if high quality is not requested
            # Max dimension 800px
            max_size = (800, 800)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Display the image (Natural size, not stretched)
        # Use columns to center or control size if needed, but here simple st.image with use_column_width=False
        st.image(image, caption=f'入力画像 ({image.size[0]}x{image.size[1]})', use_container_width=False)

        if st.button("テキストを抽出する", type="primary"):
            with st.spinner('テキストを抽出中...'):
                try:
                    # Convert PIL image to OpenCV format (if needed for preprocessing, though Tesseract handles PIL)
                    # pytesseract accepts PIL Image directly.
                    
                    # Verify Tesseract builds are available
                    # languages = pytesseract.get_languages() # Sometimes fails if Tesseract not found

                    # Extract Text
                    # lang='jpn+eng' for Japanese and English
                    custom_config = r'--oem 3 --psm 6' # Default config, often good for update
                    # psm 6: Assume a single uniform block of text.
                    
                    text = pytesseract.image_to_string(image, lang='jpn+eng')
                    
                    if text.strip():
                        st.success("抽出成功！")
                        st.text_area("抽出されたテキスト (コピー用)", value=text, height=300)

                        # --- AdSense Ad Unit (Below Results) ---
                        st.markdown("---")
                        st.caption("広告")
                        components.html("""
                        <ins class="adsbygoogle"
                             style="display:block"
                             data-ad-client="ca-pub-4443417103189902"
                             data-ad-slot="YOUR_AD_UNIT_ID_HERE"  <!-- Replace with your Ad Unit ID from AdSense Dashboard -->
                             data-ad-format="auto"
                             data-full-width-responsive="true"></ins>
                        <script>
                             (adsbygoogle = window.adsbygoogle || []).push({});
                        </script>
                        """, height=250)
                    else:
                        st.warning("テキストが検出されませんでした。画像が明瞭か確認してください。")
                
                except pytesseract.TesseractNotFoundError:
                    st.error("エラー: Tesseract OCRエンジンが見つかりません。")
                    if sys.platform.startswith('win'):
                        st.info("Windowsで実行する場合、Tesseract OCRをインストールし、PATHに追加するか、インストール先を指定する必要があります。")
                    else:
                        st.info("サーバー設定を確認してください (packages.txt)。")
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")

# --- Footer / Extras ---
st.markdown("---")

# AdSense Footer Unit
st.caption("広告")
components.html("""
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-4443417103189902"
     data-ad-slot="YOUR_AD_UNIT_ID_HERE"  <!-- Replace with your Ad Unit ID from AdSense Dashboard -->
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
""", height=250)

# Privacy Policy
st.markdown("---")

# Privacy Policy
st.markdown("""
### プライバシーポリシー

このアプリは無料のオンラインOCRツールです。
- アップロードされた画像やカメラ入力データは、テキスト抽出処理後すぐに破棄され、サーバーに保存・共有されません。
- 個人情報（名前、メールアドレス、位置情報など）は一切収集・使用していません。
- Cookieは使用していません。
- 広告について：Google AdSenseを利用しています。広告は第三者配信で、ユーザーのプライバシーを尊重した形で表示されます。
""")

st.caption("© 2024 無料OCRツール By Streamlit")
