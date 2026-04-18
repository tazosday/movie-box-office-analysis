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
# 예산과 수익이 유의미한 데이터만 필터링 (초저예산 이상치 방지를 위해 예산 1만 달러 이상으로 설정)
df = df[(df['revenue'] > 0) & (df['budget'] > 10000)].copy()

genre_map = {
    'Action': '액션', 'Adventure': '모험', 'Fantasy': '판타지', 'Animation': '애니메이션',
    'Science Fiction': 'SF', 'Drama': '드라마', 'Thriller': '스릴러', 'Family': '가족',
    'Comedy': '코미디', 'History': '역사', 'War': '전쟁', 'Western': '서부',
    'Romance': '로맨스', 'Crime': '범죄', 'Mystery': '미스터리', 'Horror': '공포',
    'Documentary': '다큐멘터리', 'Music': '음악'
}

def extract_names(json_str):
    try: return [item['name'] for item in json.loads(json_str)]
    except: return []

df['장르_리스트'] = df['genres'].apply(extract_names)
df_exp = df.explode('장르_리스트')
df_exp['장르_리스트'] = df_exp['장르_리스트'].map(lambda x: genre_map.get(x, x))

# ==========================================
# 💡 3. 가성비(수익배수) 계산
# ==========================================
# 방법: 각 장르의 '총 수익'을 '총 예산'으로 나눕니다. 
# (개별 영화의 비율을 평균 내면, 100만 원으로 1억을 번 극단적인 영화 하나가 전체를 왜곡할 수 있기 때문입니다.)
genre_stats = df_exp.groupby('장르_리스트')[['budget', 'revenue']].sum()
genre_stats['수익배수'] = genre_stats['revenue'] / genre_stats['budget']

# 수익배수가 높은 순서대로 내림차순 정렬
genre_stats = genre_stats.sort_values('수익배수', ascending=False)

# 데이터가 너무 적은 마이너 장르 제외 (예산 총합 기준)
mean_budget = genre_stats['budget'].mean()
genre_stats = genre_stats[genre_stats['budget'] > (mean_budget * 0.1)]

# ==========================================
# 4. 시각화 (막대 그래프)
# ==========================================
plt.style.use('ggplot')
plt.figure(figsize=(14, 7))

# 막대 그래프 그리기 (수익배수가 높을수록 진한 색상이 되도록 설정)
ax = sns.barplot(x=genre_stats.index, y=genre_stats['수익배수'], palette='YlOrRd_r')

# 💡 막대 위에 정확한 배수 숫자(텍스트) 적어주기
for i, v in enumerate(genre_stats['수익배수']):
    ax.text(i, v + 0.1, f"{v:.1f}배", ha='center', fontsize=11, fontweight='bold')

plt.title('영화 장르별 투자 대비 수익 비율 (가성비)', fontsize=16, pad=15)
plt.xlabel('장르', fontsize=13)
plt.ylabel('수익 배수 (수익 ÷ 예산)', fontsize=13)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.grid(axis='y', alpha=0.4)

plt.tight_layout()
plt.show()