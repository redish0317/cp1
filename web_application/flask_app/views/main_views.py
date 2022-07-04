from flask import Blueprint, render_template, request
import psycopg2
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/result', methods=['GET', 'POST'])
def result():
    #request로 사용자 입력값 전달
    jobgroup = request.form['jobgroup'] # 직군 사용자 입력값
    if request.form['career'] == '신입': # 경력여부 사용자 입력값 신입
        career = '0'
    else:
        career = request.form['career'][3] # 경력여부 사용자 입력값 경력
    skill = ' '.join(request.form.getlist('skill')) # 기술스택 사용자 입력값(tfidf)
    skill2 = ', '.join(request.form.getlist('skill')) # 기술스택 사용자 입력값(추천 키워드)
    task = ' '.join(request.form.get('task').split()) # 업무경험 사용자 입력값(tfidf)

    #tfidf 해석 위한 함수 호출
    recommended_list = tfidf(jobgroup, career, skill + ' ' + task)

    return render_template('result.html', recommended_list=recommended_list, keyword=', '.join([jobgroup,request.form['career'],skill2]))

def tfidf(jobgroup, career, skill):
    #db 연결
    host = 'arjuna.db.elephantsql.com'
    user = 'pvltcvea'
    password = 'koXbh3YWTCItiJduk1ioNrRBp3eOhlbz'
    database = 'pvltcvea'

    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cur = conn.cursor()

    #db에서 조건에 해당하는 값 불러오기
    cur.execute(f"select * from job where category_tags like '%{jobgroup}%' and (career like '%{career}%' or career = '-1');") # 사용자 입력 직군과 경력 조건
    rows = cur.fetchall()

    #tfidf 모델링
    df_db = pd.DataFrame(rows, columns=["id","skill","position","requirement","task","prefer","company","logo","url","career"]) # DB 데이터 -> 데이터프레임
    df_db['tfidf'] = df_db['skill'] + ' ' + df_db['requirement'] + ' ' + df_db['task'] + ' ' + df_db['prefer'] # 기술스택, 디테일 합치기

    df_tfidf = pd.Series(df_db['tfidf']) # tfidf 위한 시리즈 생성
    df_tfidf.loc[len(df_tfidf)] = skill # 시리즈에 사용자 입력값 추가

    tfidf_vect = TfidfVectorizer(max_features=100) # tfidf 객체 생성

    dtm_tfidf = tfidf_vect.fit_transform(df_tfidf) # tfidf fit 수행

    dtm_tfidf = pd.DataFrame(dtm_tfidf.todense(), columns=tfidf_vect.get_feature_names()) # dtm 테이블 생성(문서-단어 행렬)

    #유사도 분석
    nn = NearestNeighbors(n_neighbors=min(11, len(df_tfidf)), algorithm='kd_tree') # NearestNeighbors 객체 생성
    nn.fit(dtm_tfidf) # NearestNeighbors fit 수행

    idx = nn.kneighbors([dtm_tfidf.iloc[len(dtm_tfidf)-1]]) # 유사도 분석 결과 (유사도, index)

    nn_cosine = NearestNeighbors(n_neighbors=len(df_tfidf), algorithm='brute', metric='cosine') # NearestNeighbors 객체 생성
    nn_cosine.fit(dtm_tfidf) # NearestNeighbors fit 수행

    idx_cosine = nn_cosine.kneighbors([dtm_tfidf.iloc[len(dtm_tfidf)-1]]) # 유사도 분석 결과 (유사도, index)    

    recommended = list() # 추천 결과 list에 저장
    flag = True
    for factor, i in zip(idx[0][0], idx[1][0]):
        if flag:
            flag = False
            continue
        recommended.append([df_db.loc[i,'url'],df_db.loc[i,'logo'],df_db.loc[i,'company'],df_db.loc[i,'position'],round(factor,3),round(idx_cosine[0][0][np.where(idx_cosine[1][0] == i)][0],3)]) # [url, 로고 url, 회사이름, 잡포지션, knn 거리, 코사인 유사도]

    cur.close()
    conn.close()
    
    return recommended