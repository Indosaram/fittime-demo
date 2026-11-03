# 기획서 수치 계산 스크립트

기획서에 쓴 통계(stats*.json)와 그림(img/)을 만드는 스크립트입니다. 저장소 루트에서 실행합니다.

```bash
python scripts/download.py 15101610:pool_courses 15110953:olsports_courses 15114776:ilsan_courses 15118652:bundang_courses \
  15147992:courses_all 15144839:sports_items 15119388:online_videos 15133891:tennis 15131671:monthly_parking 15164156:parking_congestion
python scripts/normalize.py            # data/u_*.csv(UTF-8) 및 data/unified_courses.csv 생성
python scripts/analysis/analyze.py     # stats.json
python scripts/analysis/analyze2.py    # stats2.json (데이터 품질·기준월 통계)
mkdir -p img && python scripts/analysis/charts.py   # 그림, stats3/4.json (matplotlib 필요)
```
