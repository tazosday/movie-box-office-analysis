import pandas as pd

# 데이터 불러오기
df = pd.read_csv('tmdb_5000_movies.csv')

print("=== 1. 데이터 전체 건수 및 결측치(Null) 확인 ===")
# 각 컬럼별로 비어있는 데이터가 몇 개인지 출력합니다.
print(df.isnull().sum()) 

print("\n=== 2. 주요 수치형 데이터 기본 통계값 ===")
# 예산, 수익, 인지도 등 주요 숫자 데이터의 통계 요약(개수, 평균, 최소/최대값 등)을 봅니다.
# 과학적 표기법(e+07 등)을 일반 숫자로 보기 쉽게 옵션을 설정합니다.
pd.set_option('display.float_format', lambda x: f'{x:.2f}')
print(df[['budget', 'revenue', 'popularity', 'vote_average']].describe())
