import google.generativeai as genai
from PIL import Image
import os

# --- API Key ---
genai.configure(api_key="AIzaSyBipqUw67CEv6HiafV7gMVMQlWzjHmC7mc")

# --- 사용할 모델 ---
model = genai.GenerativeModel("gemini-2.0-flash")  # 빠르고 저렴한 Vision 모델

# --- 시각자료 판단 함수 ---
def has_visual_content(image: Image.Image) -> bool:
    prompt = """
이 페이지에 '제품 관련 시각자료'가 있는지 YES 또는 NO로만 답하세요.

시각자료 정의:
- 제품/부품 그림(일러스트, 라인 드로잉)
- 조작 순서 그림(손동작 포함)
- STEP 번호가 붙은 이미지


시각자료 아님:
- 텍스트만 있는 페이지
- 표만 있는 페이지
"""

    try:
        response = model.generate_content(
            [prompt, image],
            generation_config={"max_output_tokens": 5}
        )
        answer = response.text.strip().upper()
        return "YES" in answer
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


# ------------------------------------
# 📁 폴더 안 이미지 30장만 검사 (로그만 출력)
# ------------------------------------

target_dir = r"C:\Users\박지혜\PycharmProjects\GenerativeAI\project\db\pdf_pages\삼성세탁기"

print("📁 검사 폴더:", target_dir)

# PNG 파일만 가져오기
images = sorted([f for f in os.listdir(target_dir) if f.endswith(".png")])
images = images[:30]  # 앞 30장만 검사

print("총 검사 이미지 수:", len(images))

# 실행 (로그만 출력)
for file in images:
    page_num = int(file.replace("page_", "").replace(".png", ""))
    img_path = os.path.join(target_dir, file)
    img = Image.open(img_path).convert("RGB")

    print(f"\n🔎 페이지 {page_num} 검사 중...")
    has_vis = has_visual_content(img)
    print("➡ 시각자료:", "있음" if has_vis else "없음")

