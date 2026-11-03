"""공공데이터포털 파일데이터 내려받기 (로그인·키 불필요).
사용: python scripts/download.py 15101610:pool_courses 15110953:olsports_courses 15114776:ilsan_courses 15118652:bundang_courses
"""
import os, sys, re, json, requests, urllib.parse
s=requests.Session(); s.headers['User-Agent']='Mozilla/5.0'
def dl(pk,name):
    page=s.get(f'https://www.data.go.kr/data/{pk}/fileData.do',timeout=30).text
    m=re.search(r"fn_fileDataDown\('(\d+)', '(uddi:[^']+)', '([^']*)','([^']*)', '([^']*)'\)",page)
    if not m: print(pk,'no button'); return
    _,uddi,aid,sn,hist=m.groups()
    r=s.post('https://www.data.go.kr/tcs/dss/selectFileDataDownload.do',data=dict(publicDataDetailPk=uddi,publicDataPk=pk,atchFileId=aid,fileDetailSn=sn,publicDataTyCode='PR0051'),timeout=30,headers={'X-Requested-With':'XMLHttpRequest','Referer':f'https://www.data.go.kr/data/{pk}/fileData.do'})
    try: j=json.loads(r.text)
    except Exception: print(pk,'bad json',r.text[:200]); return
    if not j.get('status'): print(pk,'status false',str(j)[:300]); return
    aid,sn=j['atchFileId'],j['fileDetailSn']; nm=j['dataSetFileDetailInfo'].get('dataNm','x')
    c=s.post('https://www.data.go.kr/cmm/cmm/check-limit.json',data=dict(atchFileId=aid,fileDetailSn=sn),timeout=30).text
    f=s.get(f'https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId={aid}&fileDetailSn={sn}&dataNm='+urllib.parse.quote(nm),timeout=90)
    ext='csv'
    os.makedirs('data',exist_ok=True); open(f'data/{name}.{ext}','wb').write(f.content); print(pk,name,nm,len(f.content),c[:80])
for a in sys.argv[1:]:
    pk,name=a.split(':'); 
    try: dl(pk,name)
    except Exception as e: print(pk,'ERR',e)
