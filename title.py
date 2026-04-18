import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# 1. 데이터 불러오기 및 전처리
df = pd.read_csv('tmdb_5000_movies.csv')
df = df[(df['revenue'] > 0) & (df['budget'] > 0)].copy()

# 파생 변수: 제목 길이 계산
df['title_length'] = df['title'].apply(lambda x: len(str(x)))

# 2. 시각화 설정
plt.figure(figsize=(12, 6))

# 3. 히스토그램 및 밀도 곡선(KDE) 그리기
# bins=30은 막대의 촘촘함을 의미합니다. 숫자를 키우면 더 잘게 쪼개집니다.
sns.histplot(data=df, x='title_length', bins=30, kde=True, color='purple', alpha=0.6)

# 4. 축 및 제목 설정 (영문)
plt.title('Distribution of Movies by Title Length', fontsize=15)
plt.xlabel('Title Length (Number of Characters)', fontsize=12)
plt.ylabel('Number of Movies (Count)', fontsize=12)

# 대부분의 영화 제목이 60자 이내이므로 보기 좋게 X축 범위 제한
plt.xlim(0, 60) 
plt.grid(True, alpha=0.3)

# 5. 출력
plt.show()

# 가장 많은 영화가 속한 제목 길이 구간 확인하기
mode_length = df['title_length'].mode()[0]
print(f"가장 영화가 많이 제작된 제목 길이: {mode_length}글자")