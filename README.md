# 핏타임(FitTime) 정적 데모

**내 시간에 맞는 공공 스포츠강좌 찾기** — 한국체육산업개발(KSPO&CO)이 운영하는 4개 스포츠센터의 강좌 공공데이터를 하나로 합쳐, 요일·시작 시간·종목·가격·대상으로 한 번에 찾는 웹 프로토타입입니다.

- 데모: https://indosaram.github.io/fittime-demo/
- 2026년도 공공데이터 활용 경진대회(한국체육산업개발㈜) 출품 프로토타입

## 할 수 있는 것

- **문장으로 검색**: `화목 퇴근 후 수영 10만원 이하`, `주말 오전 아이 수영`, `일산 저녁 필라테스`처럼 적으면 요일·시간대·종목·센터·대상·가격 조건으로 바꿔 필터에 채워 줍니다. 외부 AI API나 키 없이 브라우저 안의 규칙 기반 파서(`index.html`의 `parseNL`)로 동작합니다.
- **필터 검색**: 센터, 가능한 요일(선택한 요일 안에서만 진행되는 강좌), 시작 시간 범위, 종목, 대상, 월 수강료 상한, 키워드.
- **정렬**: 시작 시간순, 가격 낮은순, 정원 많은순.
- 주소 뒤에 `?q=문장`을 붙이면 바로 검색됩니다. 예: `?q=주말 테니스 송파`

## 데이터 출처와 라이선스

| 데이터 | 제공기관 | 출처 | 이용허락범위 |
|---|---|---|---|
| 올림픽수영장 강좌정보 | 한국체육산업개발주식회사 | https://www.data.go.kr/data/15101610/fileData.do | 제한 없음 |
| 올림픽스포츠센터 강좌정보 | 한국체육산업개발주식회사 | https://www.data.go.kr/data/15110953/fileData.do | 제한 없음 |
| 일산스포츠센터 강좌정보 | 한국체육산업개발주식회사 | https://www.data.go.kr/data/15114776/fileData.do | 제한 없음 |
| 분당스포츠센터 강좌정보 | 한국체육산업개발주식회사 | https://www.data.go.kr/data/15118652/fileData.do | 제한 없음 |

- 공공데이터포털(data.go.kr)에서 2026-11-03에 내려받은 파일데이터를 가공했습니다. 출처: 한국체육산업개발주식회사, 공공데이터포털.
- `courses.json`은 원본을 가공한 파생 데이터입니다. 센터별로 최근 12개월 중 강좌가 가장 많이 등록된 달(기준월)의 강좌만 담았습니다: 올림픽수영장 2025-12, 올림픽스포츠센터 2026-01, 일산 2026-08, 분당 2026-02 (총 1,291개).
- 원본 강좌명에 들어 있는 강사 개인 이름은 지웠습니다. 원본 CSV는 저장소에 넣지 않았습니다(`scripts/download.py`로 내려받을 수 있습니다).
- 과거 공개 데이터 기반 데모이므로 실제 접수 가능 여부·잔여 인원·현재 가격은 각 센터 누리집에서 확인해야 합니다.
- 코드는 MIT 라이선스(`LICENSE`)입니다. 데이터의 권리는 제공기관에 있습니다.

## 다시 만들기

```bash
pip install pandas requests
python scripts/download.py 15101610:pool_courses 15110953:olsports_courses 15114776:ilsan_courses 15118652:bundang_courses
python scripts/normalize.py     # 서로 다른 4개 스키마 -> data/unified_courses.csv
python scripts/build_demo.py    # 기준월 추출, 강사명 마스킹 -> courses.json
python -m http.server           # http://localhost:8000
```

## 구성

기획서 수치를 다시 계산하는 스크립트는 `scripts/analysis/`에 있습니다.


```
index.html            화면, 필터, 규칙 기반 자연어 파서 (프레임워크·빌드 도구 없음)
courses.json          가공된 강좌 데이터
scripts/download.py   공공데이터포털 파일데이터 내려받기
scripts/normalize.py  4개 센터 스키마 정규화
scripts/build_demo.py 데모용 JSON 생성
```
