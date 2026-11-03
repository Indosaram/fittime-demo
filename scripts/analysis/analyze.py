import pandas as pd, re, json
D='data/'
def ld(f): return pd.read_csv(D+f, dtype=str)
P=ld('u_pool_courses.csv'); O=ld('u_olsports_courses.csv'); I=ld('u_ilsan_courses.csv'); B=ld('u_bundang_courses.csv')
def norm(df, center, m):
    out=pd.DataFrame({'center':center,'month':df[m['month']],'item':df[m['item']],'name':df[m['name']].str.strip(),
      'time':df[m['time']],'cap':pd.to_numeric(df[m['cap']],errors='coerce'),'days':df[m['days']],'target':df[m['target']],
      'price':pd.to_numeric(df[m['price']],errors='coerce')})
    return out
U=pd.concat([
 norm(P,'올림픽수영장',dict(month='시작월',item='강좌코드명',name='강좌명',time='시작종료시간',cap='정원',days='요일',target='강습반',price='강좌금액')),
 norm(O,'올림픽스포츠센터',dict(month='수강월',item='종목',name='강좌명',time='수강시간',cap='정원',days='수강요일',target='수강대상',price='수강금액')),
 norm(I,'일산올림픽스포츠센터',dict(month='시작월',item='종목',name='강좌명',time='시작종료시간',cap='정원',days='요일',target='강습반',price='금액')),
 norm(B,'분당올림픽스포츠센터',dict(month='수강월',item='종목',name='강좌명',time='시작종료시간',cap='정원',days='수강요일',target='수강대상',price='수강료')),
])
U['month']=pd.to_datetime(U['month'],errors='coerce')
U['start']=U['time'].str.extract(r'(\d{1,2}):?(\d{2})')[0].astype(float)
R={}
R['rows_total']=len(U)
R['by_center']={c:dict(rows=int(len(g)),min=str(g.month.min().date()),max=str(g.month.max().date()),items=int(g['item'].nunique())) for c,g in U.groupby('center')}
# latest month per center
lat={}
for c,g in U.groupby('center'):
    m=g.month.max(); x=g[g.month==m]
    lat[c]=dict(month=str(m.date()),courses=int(len(x)),cap_sum=int(x.cap.sum()),price_median=float(x.price.median()),
      evening_share=round(float((x.start>=18).mean()),3),morning_share=round(float((x.start<9).mean()),3),
      top_items=x['item'].value_counts().head(5).to_dict())
R['latest']=lat
# swim price history example: median price of 수영 by year per center
sw=U[U['item'].fillna('').str.contains('수영')]
sw=sw.assign(y=sw.month.dt.year)
R['swim_median_price_by_year']={c:g.groupby('y').price.median().dropna().astype(int).to_dict() for c,g in sw.groupby('center')}
# naming inconsistency: number of distinct schema column names
R['schema_cols']={'pool':list(P.columns),'olsports':list(O.columns),'ilsan':list(I.columns),'bundang':list(B.columns)}
T=ld('u_tennis.csv'); T['이용자수']=pd.to_numeric(T['이용자수']); T['y']=T['시작일'].str[:4]; T['m']=T['시작일'].str[5:7]
R['tennis_year']=T.groupby(['y','구분'])['이용자수'].sum().unstack().to_dict()
R['tennis_month_avg']=T.groupby('m')['이용자수'].sum().to_dict()
R['tennis_range']=[T['시작일'].min(),T['시작일'].max()]
MP=ld('u_monthly_parking.csv'); MP['주차대수']=pd.to_numeric(MP['주차대수'])
R['parking_year']=MP.groupby(['연도','주차장소'])['주차대수'].sum().unstack().to_dict()
R['parking_olpark_month']={f'{a}-{b}':int(v) for (a,b),v in MP[MP['주차장소']=='올림픽공원'].groupby(['연도','월'])['주차대수'].sum().items()}
PC=ld('u_parking_congestion.csv')
R['congestion']=dict(rows=len(PC),levels=PC['혼잡도'].value_counts().to_dict(),zones=PC['주차구역'].nunique(),dmin=PC['등록일'].min(),dmax=PC['등록일'].max())
V=ld('u_online_videos.csv'); R['videos']=dict(n=len(V),views=int(pd.to_numeric(V['조회수']).sum()))
S=ld('u_sports_items.csv'); R['items_n']=len(S)
C=ld('u_courses_all.csv'); R['course_desc']=C['스포츠센터'].value_counts().to_dict()
U.to_csv('data/unified_courses.csv',index=False)
json.dump(R,open('stats.json','w'),ensure_ascii=False,indent=1,default=str)
print(json.dumps(R,ensure_ascii=False,indent=1,default=str)[:6000])
