import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
    elif system == 'Darwin':
        plt.rc('font', family='AppleGothic')
    else:
        plt.rc('font', family='NanumGothic')
    plt.rcParams['axes.unicode_minus'] = False 

set_korean_font()

# ==========================================
# 2. 데이터 로드 및 전처리
# ==========================================
df = pd.read_csv('tmdb_5000_movies.csv')
# 유의미한 분석을 위해 예산과 수익이 존재하는 데이터만 필터링
df = df[(df['revenue'] > 0) & (df['budget'] > 0)].copy()
df = df.dropna(subset=['release_date'])

# '개봉연도' 추출
df['개봉연도'] = pd.to_datetime(df['release_date']).dt.year

# 데이터가 충분히 쌓인 1980년 이후 데이터만 추출
df = df[df['개봉연도'] >= 1980]

# 장르 데이터 파싱 및 한글화
genre_map = {
    'Action': '액션', 'Adventure': '모험', 'Fantasy': '판타지', 'Animation': '애니메이션',
    'Science Fiction': 'SF', 'Drama': '드라마', 'Thriller': '스릴러', 'Family': '가족',
    'Comedy': '코미디', 'Horror': '공포', 'Romance': '로맨스'
}

def extract_names(json_str):
    try: return [item['name'] for item in json.loads(json_str)]
    except: return []

df['장르_리스트'] = df['genres'].apply(extract_names)
df_exp = df.explode('장르_리스트')
df_exp['장르_리스트'] = df_exp['장르_리스트'].map(lambda x: genre_map.get(x, x))

# ==========================================
# 💡 3. 주요 타겟 장르 선정 및 그룹화
# ==========================================
# 시각적 가독성을 위해 비교할 주요 장르 6가지만 선택
target_genres = ['액션', 'SF', '애니메이션', '코미디', '공포', '드라마']
df_target = df_exp[df_exp['장르_리스트'].isin(target_genres)]

# '연도'와 '장르'별로 묶어서 평균 수익 계산
trend_data = df_target.groupby(['개봉연도', '장르_리스트'])['revenue'].mean().reset_index()

# ==========================================
# 4. 시각화 (다중 선 그래프)
# ==========================================
plt.style.use('ggplot')
plt.figure(figsize=(14, 7))

# hue='장르_리스트'를 통해 장르별로 선 색깔을 다르게 그림
sns.lineplot(data=trend_data, x='개봉연도', y='revenue', hue='장르_리스트', 
             marker='o', linewidth=2.5, markersize=6, palette='tab10')

plt.title('연도별 주요 장르의 평균 흥행 수익 흐름 (1980년 이후)', fontsize=16, pad=15)
plt.xlabel('개봉 연도', fontsize=13)
plt.ylabel('평균 흥행 수익 ($)', fontsize=13)

# 범례 위치 및 설정
plt.legend(title='영화 장르', fontsize=11, title_fontsize=12, loc='upper left')
plt.grid(True, alpha=0.4)

plt.tight_layout()
plt.show()