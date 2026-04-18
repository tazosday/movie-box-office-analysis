import pandas as pd
import matplotlib.pyplot as plt
import json
import platform
import warnings
warnings.filterwarnings('ignore')

# ==========================================
# 1. 한글 폰트 설정
# ==========================================
def set_korean_font():
    system = platform.system()
    if system == 'Windows':
        plt.rc('font', family='Malgun Gothic')
    elif system == 'Darwin': # Mac
        plt.rc('font', family='AppleGothic')
    else: # Linux/Colab
        plt.rc('font', family='NanumGothic')
    plt.rcParams['axes.unicode_minus'] = False 

set_korean_font()

# ==========================================
# 2. 데이터 로드 및 전처리
# ==========================================
df = pd.read_csv('tmdb_5000_movies.csv')
df = df[(df['revenue'] > 0) & (df['budget'] > 0)].copy()

# 장르 한글 매핑 딕셔너리
genre_map = {
    'Action': '액션', 'Adventure': '모험', 'Fantasy': '판타지', 'Animation': '애니메이션',
    'Science Fiction': 'SF', 'Drama': '드라마', 'Thriller': '스릴러', 'Family': '가족',
    'Comedy': '코미디', 'History': '역사', 'War': '전쟁', 'Western': '서부',
    'Romance': '로맨스', 'Crime': '범죄', 'Mystery': '미스터리', 'Horror': '공포'
}

def extract_names(json_str):
    try: return [item['name'] for item in json.loads(json_str)]
    except: return []

df['장르_리스트'] = df['genres'].apply(extract_names)
df_exp = df.explode('장르_리스트')

# 영문 장르명을 한글로 변환 (매핑되지 않은 건 영문 유지)
df_exp['장르_리스트'] = df_exp['장르_리스트'].map(lambda x: genre_map.get(x, x))

# ==========================================
# 3. 장르별 데이터 그룹화 및 분석
# ==========================================
# 장르별로 '예산(budget)'과 '수익(revenue)'의 평균을 동시에 계산
genre_stats = df_exp.groupby('장르_리스트')[['budget', 'revenue']].mean()

# 보기 좋게 '평균 수익'이 높은 순서대로 내림차순 정렬
genre_stats = genre_stats.sort_values('revenue', ascending=False)

# 그래프의 범례(Legend)에 예쁘게 나오도록 컬럼 이름 변경
genre_stats.columns = ['평균 예산', '평균 수익']

# ==========================================
# 4. 시각화 (다중 막대 그래프)
# ==========================================
plt.style.use('ggplot')

# kind='bar'를 사용하면 데이터프레임의 두 컬럼이 나란히 막대로 그려집니다.
# color로 예산은 파란색 계열, 수익은 붉은/주황색 계열로 설정해 가독성을 높입니다.
ax = genre_stats.plot(kind='bar', figsize=(14, 7), color=['#4C72B0', '#DD8452'], width=0.8)

plt.title('영화 장르별 평균 예산 및 평균 흥행 수익 비교', fontsize=16, pad=15)
plt.xlabel('장르', fontsize=13)
plt.ylabel('금액 ($)', fontsize=13)
plt.xticks(rotation=45, ha='right', fontsize=12)

# y축 단위를 보기 좋게 지수표현식(1e8)에서 일반 숫자로 변경 (선택 사항)
ax.get_yaxis().get_major_formatter().set_scientific(False)

plt.tight_layout()
plt.show()