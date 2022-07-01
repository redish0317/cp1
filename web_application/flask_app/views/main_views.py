from flask import Blueprint, render_template, request
import psycopg2
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/result', methods=['GET', 'POST'])
def result():
    #request로 사용자 입력값 전달
    jobgroup = request.form['jobgroup']
    if request.form['career'] == '신입':
        career = '0'
    else:
        career = request.form['career'][3]
    skill = ' '.join(request.form.getlist('skill'))
    skill2 = ', '.join(request.form.getlist('skill'))
    task = ' '.join(request.form.get('task').split())

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
    cur.execute(f"select * from job where category_tags like '%{jobgroup}%' and (career like '%{career}%' or career = '-1');")
    rows = cur.fetchall()

    #tfidf 모델링
    df_db = pd.DataFrame(rows, columns=["id","skill","position","requirement","task","prefer","company","logo","url","career"])
    df_db['tfidf'] = df_db['skill'] + ' ' + df_db['requirement'] + ' ' + df_db['task'] + ' ' + df_db['prefer']

    df_tfidf = pd.Series(df_db['tfidf'])
    df_tfidf.loc[len(df_tfidf)] = skill

    tfidf_vect = TfidfVectorizer(max_features=100)

    dtm_tfidf = tfidf_vect.fit_transform(df_tfidf)

    dtm_tfidf = pd.DataFrame(dtm_tfidf.todense(), columns=tfidf_vect.get_feature_names())

    #유사도 분석
    nn = NearestNeighbors(n_neighbors=min(11, len(df_tfidf)), algorithm='kd_tree')
    nn.fit(dtm_tfidf)

    idx = nn.kneighbors([dtm_tfidf.iloc[len(dtm_tfidf)-1]])

    recommended = list()
    flag = True
    for factor, i in zip(idx[0][0], idx[1][0]):
        if flag:
            flag = False
            continue
        recommended.append([df_db.loc[i,'url'],df_db.loc[i,'logo'],df_db.loc[i,'company'],df_db.loc[i,'position']])

    cur.close()
    conn.close()
    
    return recommended