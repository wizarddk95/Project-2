import json
import re
import time
import pandas as pd
import requests
from tqdm import tqdm

# ✅ Google Cloud Translation API 키
API_KEY = ""

# ✅ API 엔드포인트 URL (Google Could Translation API의 번역 요청는 엔드포인트 URL)
TRANSLATE_URL = "https://translation.googleapis.com/language/translate/v2"

# ✅ JSON 파일에서 기존 번역 데이터 불러오기
json_file_path = "japanese_to_korean.json"

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        translation_dict = json.load(f)
        if not isinstance(translation_dict, dict):  # JSON이 딕셔너리인지 확인
            translation_dict = {}
except (FileNotFoundError, json.JSONDecodeError):
    translation_dict = {}

# ✅ 일본어 포함 여부 확인 함수 (일본어가 포함되지 않은 텍스트는 번역하지 않도록 - 불필요한 API 요청 줄이기)
def contains_japanese(text):
    if not text or not isinstance(text, str): # not isinstance(text, str): 변수 text가 문자열이 아닌 경우 True
        return False
    return bool(re.search(r'[\u3040-\u30FF\u31F0-\u31FF\u4E00-\u9FFF]', text))  # 히라가나, 가타카나, 한자 포함 여부

# ✅ Google Cloud Translation API를 활용한 번역 함수
def translate_text(text):
    if not contains_japanese(text):  # 일본어가 없으면 번역하지 않음
        return text
    if text in translation_dict:  # 이미 번역한 경우 캐싱된 값 사용
        return translation_dict[text]

    params = {
        "q": text,
        "source": "ja",
        "target": "ko",
        "format": "text",
        "key": API_KEY,  # API 키 추가
    }

    attempts = 3  # 최대 3번 재시도
    for attempt in range(attempts):
        try:
            response = requests.post(TRANSLATE_URL, params=params) # 데이터를 보내서 처리하는 방식이라 POST를 사용
            result = response.json()
            if "data" in result:
                translated = result["data"]["translations"][0]["translatedText"]
                translation_dict[text] = translated  # 번역 결과 저장
                return translated
            else:
                print(f"⚠ 번역 실패: {result}")
        except Exception as e:
            print(f"⚠ 번역 오류 (시도 {attempt+1}/{attempts}): {text} → 오류: {e}")
            time.sleep(1)  # 재시도 전 대기

    return text  # 3번 실패하면 원본 반환

# ✅ 번역 수행
for col in tqdm(japanese_columns, desc="번역 진행 중"):
    unique = df[col].astype(str).unique()
    for text in unique:
        translate_text(text)

# ✅ 번역된 데이터 JSON 파일로 저장
with open(json_file_path, 'w', encoding='utf-8') as f:
    json.dump(translation_dict, f, ensure_ascii=False, indent=4)

print("✅ 번역 완료 및 JSON 저장 완료!")
