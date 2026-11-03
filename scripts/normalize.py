"""4개 센터 강좌 CSV(서로 다른 스키마)를 하나로 정규화 -> data/unified_courses.csv
원본은 CP949/EUC-KR일 수 있어 UTF-8로 바꾼 u_*.csv를 읽습니다(아래 to_utf8 참고)."""
import pandas as pd, re
D='data/'
import os
def to_utf8(name):
    src, dst = D + name, D + 'u_' + name
    if not os.path.exists(dst):
        raw = open(src, 'rb').read()
        for enc in ('utf-8-sig', 'cp949'):
            try: txt = raw.decode(enc); break
            except UnicodeDecodeError: pass
        open(dst, 'w', encoding='utf-8').write(txt)
for n in sorted(os.listdir(D)):
    if n.endswith('.csv') and not n.startswith('u_') and n != 'unified_courses.csv':
        to_utf8(n)
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
U.to_csv('data/unified_courses.csv',index=False)
print(len(U),'rows')
