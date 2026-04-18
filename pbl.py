import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import platform
import warnings
warnings.filterwarnings('ignore')

# ==========================================
# 1. 한글 폰트 설정 (환경별 자동 감지)
# ==========================================
def set_korean_font():
    system = platform.system()
    if system == 'Windows':
        plt.rc('font', family='Malgun Gothic')
    elif system == 'Darwin': # Mac
        plt.rc('font', family='AppleGothic')
    else: # Linux/Colab (나눔폰트 설치 필요)
        plt.rc('font', family='NanumGothic')
    plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

set_korean_font()

# ==========================================
# 2. 데이터 로드 및 전처리
# ==========================================
df = pd.read_csv('tmdb_5000_movies.csv')
df = df[(df['revenue'] > 0) & (df['budget'] > 0)].copy()

# 장르 한글 매핑 딕셔너리 (주요 장르)
genre_map = {
    'Action': '액션', 'Adventure': '모험', 'Fantasy': '판타지', 'Animation': '애니메이션',
    'Science Fiction': 'SF', 'Drama': '드라마', 'Thriller': '스릴러', 'Family': '가족',
    'Comedy': '코미디', 'History': '역사', 'War': '전쟁', 'Western': '서부',
    'Romance': '로맨스', 'Crime': '범죄', 'Mystery': '미스터리', 'Horror': '공포'
}

# 언어 코드 한글 매핑 (상위권 위주)
lang_map = {
    'en': '영어', 'ja': '일본어', 'fr': '프랑스어', 'zh': '중국어', 'ko': '한국어',
    'de': '독일어', 'hi': '힌디어', 'es': '스페인어', 'it': '이탈리아어', 'sa': '산스크리트어',
    'ne': '네팔어', 'ta': '타밀어', 'si': '신할라어', 'sv': '스웨덴어'
}

def extract_names(json_str):
    try: return [item['name'] for item in json.loads(json_str)]
    except: return []

def extract_lang_codes(json_str):
    try: return [item['iso_639_1'] for item in json.loads(json_str)]
    except: return []

# ==========================================
# 💡 확인하고 싶은 그래프 번호 (1 ~ 5)
# ==========================================
TARGET_GRAPH = 1
# ==========================================

plt.style.use('ggplot')
plt.figure(figsize=(12, 6))

if TARGET_GRAPH == 1:
    sns.regplot(data=df, x='budget', y='revenue', 
                scatter_kws={'alpha':0.3, 'color':'blue'}, line_kws={'color':'red'})
    plt.title('제작 예산과 흥행 수익의 상관관계', fontsize=15)
    plt.xlabel('제작 예산 ($)', fontsize=12)
    plt.ylabel('흥행 수익 ($)', fontsize=12)

elif TARGET_GRAPH == 2:
    df['제목_길이'] = df['title'].apply(lambda x: len(str(x)))
    res = df.groupby('제목_길이')['revenue'].mean().sort_index()
    plt.plot(res.index, res.values, marker='o', color='red')
    plt.title('영화 제목 길이에 따른 평균 흥행 수익', fontsize=15)
    plt.xlabel('제목 글자 수', fontsize=12)
    plt.ylabel('평균 수익 ($)', fontsize=12)
    plt.xlim(0, 60)

elif TARGET_GRAPH == 3:
    # 💡 3번 분석 (수정됨)
    df['제작사_리스트'] = df['production_companies'].apply(extract_names)
    df_exp = df.explode('제작사_리스트')
    
    # [Step 1] '총 누적 수익(sum)' 기준으로 1등부터 15등까지 제작사 이름 추출
    top15_names = df_exp.groupby('제작사_리스트')['revenue'].sum().sort_values(ascending=False).head(15).index
    
    # [Step 2] 그 15개 제작사의 데이터만 필터링한 뒤, '평균 수익(mean)' 계산
    # reindex(top15_names)를 써서 X축 순서를 총 수익 1위~15위 순서대로 유지함
    res = df_exp[df_exp['제작사_리스트'].isin(top15_names)].groupby('제작사_리스트')['revenue'].mean().reindex(top15_names)
    
    # [Step 3] 그래프 그리기 및 요청하신 한글 이름 적용
    plt.plot(res.index, res.values, marker='o', color='green', linewidth=2)
    plt.title('주요 제작사 평균 흥행수익 (총흥행순위 TOP 15 제작사)', fontsize=15)
    plt.xlabel('총흥행순위 TOP 15 제작사', fontsize=12)
    plt.ylabel('평균 흥행수익 ($)', fontsize=12)
    plt.xticks(rotation=45, ha='right')

elif TARGET_GRAPH == 4:
    df['언어_코드'] = df['spoken_languages'].apply(extract_lang_codes)
    df_exp = df.explode('언어_코드')
    res = df_exp.groupby('언어_코드')['revenue'].mean().sort_values(ascending=False).head(15)
    # 한글 이름으로 변환
    res.index = [lang_map.get(x, x) for x in res.index]
    plt.plot(res.index, res.values, marker='o', color='purple')
    plt.title('사용 언어별 평균 흥행 수익 (TOP 15)', fontsize=15)
    plt.xlabel('사용 언어', fontsize=12)
    plt.ylabel('평균 수익 ($)', fontsize=12)
    plt.xticks(rotation=45)


elif TARGET_GRAPH == 5:
    df['개봉연도'] = pd.to_datetime(df['release_date']).dt.year
    res = df[df['개봉연도'] >= 1970].groupby('개봉연도')['revenue'].mean()
    plt.plot(res.index, res.values, marker='o', color='teal')
    plt.title('연도별 평균 흥행 수익 변화 (1970년 이후)', fontsize=15)
    plt.xlabel('개봉 연도', fontsize=12)
    plt.ylabel('평균 수익 ($)', fontsize=12)

plt.tight_layout()
plt.show()