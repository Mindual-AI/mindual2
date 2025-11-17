import google.generativeai as genai
from PIL import Image
from core.config import GEMINI_API_KEY  # .env에서 불러오는 구조 유지

# --------------------------
# Gemini 모델 설정
# --------------------------
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# --------------------------
# 이미지 로드 (네가 보여준 경로 그대로)
# --------------------------
img = Image.open("project/scripts/page_10.png").convert("RGB")

# --------------------------
# Retrieval 텍스트 예시 (실제 RAG output 자리)
# --------------------------
retrieved_sentences = [
    "설치할 장소를 선택해 주세요.",
    "세탁기와 후면 벽과의 거리는 5 cm 이상, 좌우 벽과의 거리는 2 cm 이상 떨어져 설치하세요.",
    "TYPE 1: 잠금 너트, 조절 너트, 수평 조절 다리, 스패너가 포함됩니다.",
    "TYPE 2: 수평 조절 다리, 너트, 스패너가 포함됩니다."
]

joined_text = "\n".join(retrieved_sentences)

# --------------------------
# 테스트 질문 2개
# --------------------------
questions = [
    "TYPE 1 그림에서 잠금 너트와 조절 너트의 위치 관계를 설명해줘.",
    "세탁기 후면 벽과의 최소 설치 거리는 얼마나 떨어져야 하나요?"
]

# --------------------------
# 테스트 실행
# --------------------------
for q in questions:
    print("\n========================================")
    print("🧑‍💬 질문:", q)
    print("========================================")

    # 👉 AnswerSynthesisAgent 내부 프롬프트 100% 복사본
    prompt = f"""
당신은 가전제품 사용설명서 상담 전문가입니다.

아래 정보를 기반으로 사용자의 질문에 답하세요.

📌 답변 규칙
1) TEXT(설명서 내용)을 최우선적으로 기반으로 답변하세요.
2) IMAGE가 제공된 경우, 질문과 직접 관련 있을 때만 사용하세요.
3) 이미지가 질문과 무관하면 사용하지 말고 TEXT만 기반으로 답하세요.
4) 허구의 정보는 추가하지 마세요.
5) 가능한 명확하고 구체적으로 답변하세요.

🧑‍💬 사용자 질문:
{q}

📄 TEXT (Retrieval 결과):
{joined_text}
"""

    response = model.generate_content(
        [prompt, img],   # 👉 AnswerSynthesisAgent의 multimodal 방식 그대로
        generation_config={
            "temperature": 0.2,
            "max_output_tokens": 300
        }
    )

    print("\n💬 Gemini 답변:")
    print(response.text.strip())
