import pandas as pd, json
U=pd.read_csv('data/unified_courses.csv',parse_dates=['month'])
R={}
bad=U[(U.month.dt.year>2027)|(U.month.dt.year<2005)|U.month.isna()]
R['anomaly_month_rows']=bad.groupby('center').size().to_dict()
R['anomaly_examples']=bad.month.astype(str).value_counts().head(5).to_dict()
R['price_missing']=U.price.isna().groupby(U.center).sum().astype(int).to_dict()
R['start_missing']=U.start.isna().groupby(U.center).sum().astype(int).to_dict()
V=U[(U.month.dt.year>=2005)&(U.month<='2026-11-01')]
out={}
for c,g in V.groupby('center'):
    cnt=g.groupby('month').size()
    m=cnt[cnt>=20].index.max()
    x=g[g.month==m]
    out[c]=dict(month=str(m.date()),courses=int(len(x)),items=int(x['item'].nunique()),cap_sum=int(x.cap.sum()),
      price_min=int(x.price.min()),price_median=int(x.price.median()),price_max=int(x.price.max()),
      evening18_share=round(float((x.start>=18).mean()),3),before9_share=round(float((x.start<9).mean()),3),
      weekend_share=round(float(x.days.fillna('').str.contains('토|일').mean()),3),
      top_items=x['item'].value_counts().head(6).to_dict())
R['latest_real']=out
R['distinct_item_names_total']=int(V['item'].nunique())
R['target_values_sample']=V['target'].value_counts().head(15).to_dict()
R['days_format_sample']=V['days'].value_counts().head(8).to_dict()
R['time_format_sample']=V['time'].str.replace(r'\d','9',regex=True).value_counts().head(6).to_dict()
json.dump(R,open('stats2.json','w'),ensure_ascii=False,indent=1,default=str)
print(json.dumps(R,ensure_ascii=False,indent=1,default=str))
