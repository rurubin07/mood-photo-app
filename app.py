# 📦 필요한 모듈 불러오기
import streamlit as st # Streamlit 웹앱 프레임워크
import requests # 외부 API 요청을 위한 HTTP 라이브러리

# 🔑 Unsplash API 키 (반드시 본인의 키로 교체해야 작동함!)
UNSPLASH_ACCESS_KEY = st.secrets['API_KEY']

# 📸 Unsplash에서 사진 검색 함수 정의
def search_unsplash_images(query, count=3):
    """
    사용자가 입력한 무드(query)에 따라 Unsplash에서 관련 사진을 검색해
    count 수만큼 반환한다. 결과는 이미지 URL, 설명, 작가 정보 포함.
    """
    url = "https://api.unsplash.com/photos/random" # 무작위 사진 엔드포인트
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}" # API 인증 키 헤더
    }
    params = {
        "query": query, # 검색 키워드 (사용자 입력 무드)
        "count": count # 가져올 이미지 수
    }

    # API 요청 보내기
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        # 요청 성공 시 응답 결과(JSON)를 파싱
        images = response.json()
        results = []
        for img in images:
            image_url = img["urls"]["regular"] # 사진 URL
            description = img.get("description") or img.get("alt_description") or "설명이 없습니다." # 사진 설명
            photographer = img["user"]["name"] # 사진 작가 이름
            results.append({
                "url": image_url,
                "description": description,
                "photographer": photographer
            })
        return results
    else:
        # 요청 실패 시 에러 메시지 출력
        st.error(f"사진을 불러오는 데 실패했습니다. 상태 코드: {response.status_code}")
        return []

# 🖥️ Streamlit 사용자 인터페이스 시작
st.title("🎨 무드 기반 사진 추천 웹앱") # 앱 제목

# 사용자로부터 무드(감정)를 입력 받음
mood = st.text_input("지금 당신의 기분은 어떤가요? (예: 설렘, 외로움, 고요함 등)")

# 버튼을 눌렀을 때 사진 검색 실행
if st.button("사진 보기"):
    if mood:
        st.subheader(f"'{mood}' 무드에 어울리는 사진들") # 검색 결과 제목 출력
        images = search_unsplash_images(mood, count=3) # API를 통해 이미지 검색
        for i, img in enumerate(images, start=1):
            st.image(img["url"], caption=f"사진 {i}") # 이미지 출력
            st.write(f"📝 설명: {img['description']}") # 사진 설명 출력
            st.write(f"📸 사진작가: {img['photographer']}") # 작가 정보 출력
            st.markdown("---") # 구분선 추가
    else:
        st.warning("먼저 무드를 입력해주세요.") # 무드 미입력 시 경고
