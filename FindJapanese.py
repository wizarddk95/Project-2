import re

def find_japanese_columns(df):
    # 일본어(히라가나, 가타카나, 한자) 포함 여부를 판별하는 정규 표현식
    japanese_pattern = re.compile(r"[\u3040-\u30FF\u4E00-\u9FFF]")

    # 일본어 포함 여부 반환 함수
    def contains_japanese(text):
        if pd.isna(text):  # NaN 값 처리
            return False
        return bool(japanese_pattern.search(str(text)))
        
    # 일본어 포함된 컬럼 찾기
    japanese_columns = [col for col in df.columns if df[col].astype(str).apply(contains_japanese).any()]
    
    # 결과 출력
    return japanese_columns
