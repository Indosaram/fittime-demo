"""핏타임 데모용 courses.json 생성: 센터별 최근 기준월(최근 12개월 중 강좌 수 최대 월) 강좌만 추출, 강사명 마스킹."""
import pandas as pd, re, json, os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = D
os.makedirs(OUT, exist_ok=True)
d = pd.read_csv(os.path.join(D, 'data/unified_courses.csv'))
d['month'] = pd.to_datetime(d['month'], errors='coerce')
d = d[(d.month >= '2013-01-01') & (d.month <= '2026-12-01')]

S = '김이박최정강조윤장임한오서신권황안송류전홍고문양손배백허유남심노하곽성차주우구민진나지엄채원천방공현함변염여추도소석선설마길연위표명기반왕금옥육인맹제모탁국어은편용예봉경사부'
STOP = set('보조풀 오리발 연수 기초 성인 신기초 어린이 고급 배영 주말 탁구 강습 강사 진도표 성인반 신설 이상 방특 공휴일 오후 반으로 오전 한달 유아풀 여성 서킷핏 지하 반과 국제식 모던 주말반 신규 마스터 배민 주일 양성반 기구 반야사 여학생 경험자 이벤트 한달더 주의 서현초 조깅 임직원 보관 반합반 한글수 배우신 예정 금지 연계반 부부반 서킷 마감 한글 안내 명운영 연수반 기초반 강좌 배형 연계 어르신 사이클 주부 노르딕 고등생 배영킥 지유형 남아 여아 사용 진도 추가 전체 명은 모두 명이상 오리초 이매초 장안초 보평초'.split())
pat = re.compile(r'(?<![가-힣])([' + S + r'][가-힣]{1,2})(?![가-힣])')
masked = set()
def mask(n):
    def r(m):
        t = m.group(1)
        if t in STOP: return t
        if len(t) == 2 and t != '허정': return t
        masked.add(t); return ''
    out = pat.sub(r, str(n))
    return re.sub(r'\s{2,}', ' ', out).strip(' _-')

rows = []; meta = {}
CK = {'올림픽수영장': 'pool', '올림픽스포츠센터': 'olpark', '일산올림픽스포츠센터': 'ilsan', '분당올림픽스포츠센터': 'bundang'}
for c, g in d.groupby('center'):
    recent = g[g.month > g.month.max() - pd.DateOffset(months=12)]
    m = recent.month.value_counts().idxmax()
    x = g[g.month == m].drop_duplicates(['name', 'time', 'days', 'price'])
    meta[CK[c]] = dict(name=c, month=m.strftime('%Y-%m'), courses=int(len(x)))
    for _, r in x.iterrows():
        t = str(r.time); mm = re.findall(r'(\d{1,2}):(\d{2})', t)
        if not mm: continue
        s = int(mm[0][0]) * 60 + int(mm[0][1]); e = int(mm[1][0]) * 60 + int(mm[1][1]) if len(mm) > 1 else None
        days = str(r.days) if pd.notna(r.days) else ''
        core = re.sub(r'\([^)]*\)', '', days)
        dl = [ch for ch in '월화수목금토일' if ch in core]
        rows.append(dict(c=CK[c], i=str(r['item']) if pd.notna(r['item']) else '기타', n=mask(r['name']), s=s, e=e,
                         d=''.join(dl), dr=days, t=str(r.target) if pd.notna(r.target) else '',
                         p=int(r.price) if pd.notna(r.price) else None, q=int(r.cap) if pd.notna(r.cap) else None))
json.dump(dict(meta=meta, generated='2026-11-03', rows=rows), open(os.path.join(OUT, 'courses.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
print(meta, len(rows)); print('masked tokens:', len(masked))
