import pandas as pd, json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
fm.fontManager.addfont('/usr/share/fonts/truetype/nanum/NanumGothic.ttf')
plt.rcParams['font.family']='NanumGothic'; plt.rcParams['axes.unicode_minus']=False
U=pd.read_csv('data/unified_courses.csv',parse_dates=['month'])
V=U[(U.month.dt.year>=2005)&(U.month<='2026-11-01')].copy()
R={}
# 2025 full year supply by start hour (all centers), rows = course-month
y=V[V.month.dt.year==2025]
R['rows_2025']=len(y); R['centers_2025']=y.center.value_counts().to_dict()
bins=[0,9,12,18,24]; labels=['~9시','9~12시','12~18시','18시~']
y=y.assign(slot=pd.cut(y.start,bins=bins,right=False,labels=labels))
tab=y.groupby(['center','slot'],observed=False).size().unstack(fill_value=0)
share=(tab.T/tab.sum(axis=1)).T.round(3)
R['slot_share_2025']=share.to_dict(orient='index'); R['slot_counts_2025']=tab.to_dict(orient='index')
R['slot_share_2025_all']=(tab.sum()/tab.values.sum()).round(3).to_dict()
# course continuity: months per course id (center+id)
# need course id: reload originals quickly
ids={'올림픽수영장':('u_pool_courses.csv','강좌번호','시작월'),'올림픽스포츠센터':('u_olsports_courses.csv','강좌일련번호','수강월'),
     '일산올림픽스포츠센터':('u_ilsan_courses.csv','강좌번호','시작월'),'분당올림픽스포츠센터':('u_bundang_courses.csv','강좌번호','수강월')}
cont={}
for c,(f,k,m) in ids.items():
    d=pd.read_csv('data/'+f,dtype=str); n=d.groupby(k)[m].nunique()
    cont[c]=dict(courses=int(len(n)),median_months=float(n.median()),ge12=int((n>=12).sum()),ge12_share=round(float((n>=12).mean()),3))
R['continuity']=cont
json.dump(R,open('stats3.json','w'),ensure_ascii=False,indent=1,default=str)
print(json.dumps(R,ensure_ascii=False,indent=1,default=str))
# chart1 slot share
fig,ax=plt.subplots(figsize=(7.2,3.0),dpi=200)
share.plot(kind='barh',stacked=True,ax=ax,color=['#9DB4D3','#5B84B1','#2E5E8C','#E07B39'],width=0.6)
ax.set_xlabel('2025년 개설 강좌(강좌×월) 중 시작시각 비중'); ax.set_ylabel('')
ax.legend(ncol=4,loc='upper center',bbox_to_anchor=(0.5,1.22),frameon=False,fontsize=8)
ax.set_xlim(0,1); ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
for i,(c,row) in enumerate(share.iterrows()):
    ax.text(row.sum()-0.01, i, f"18시~ {row['18시~']*100:.0f}%", va='center', ha='right', fontsize=7.5, color='white')
plt.tight_layout(); plt.savefig('img/chart_slots.png'); plt.close()
# chart2 tennis monthly avg (daily entries) + chart3 parking
T=pd.read_csv('data/u_tennis.csv'); T['m']=T['시작일'].str[5:7].astype(int); T['y']=T['시작일'].str[:4]
dd=T[T['구분']=='일일입장'].groupby('m')['이용자수'].mean()
MP=pd.read_csv('data/u_monthly_parking.csv'); MP['m']=MP['월'].str[:2].astype(int)
op=MP[MP['주차장소']=='올림픽공원'].groupby('m')['주차대수'].mean()
fig,ax=plt.subplots(1,2,figsize=(7.2,2.6),dpi=200)
ax[0].bar(dd.index,dd.values,color='#2E5E8C'); ax[0].set_title('올림픽테니스장 일일입장 월평균(2021~2025)',fontsize=9); ax[0].set_xticks(range(1,13))
ax[1].bar(op.index,op.values,color='#E07B39'); ax[1].set_title('올림픽공원 주차대수 월평균(2023~2025)',fontsize=9); ax[1].set_xticks(range(1,13))
for a in ax: a.tick_params(labelsize=7); a.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v,p:f'{int(v):,}'))
plt.tight_layout(); plt.savefig('img/chart_tennis_parking.png'); plt.close()
R2={'tennis_daily_month_mean':dd.round(0).to_dict(),'olpark_parking_month_mean':op.round(0).to_dict()}
json.dump(R2,open('stats4.json','w'),ensure_ascii=False,indent=1)
print(R2)
