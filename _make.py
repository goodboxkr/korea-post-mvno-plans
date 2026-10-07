# -*- coding: utf-8 -*-
"""공개 데이터 저장소 goodboxkr/korea-post-mvno-plans 생성기 (외부유입 #6, 2026-10-07).
원본: tools_24시약국/_data/post_mvno.json (공공데이터포털 15075270 우체국알뜰폰 요금제, 매일 갱신). 다시 만들기: python _make.py → git add -A; git commit; git push"""
import csv, json
from pathlib import Path
H = Path(__file__).resolve().parent
d = json.load(open(H.parent / "tools_24시약국" / "_data" / "post_mvno.json", encoding="utf-8")); rows = d["rows"]
(H / "data").mkdir(exist_ok=True)
F = [("net", "통신망"), ("biz", "사업자"), ("name", "요금제명"), ("gen", "망 세대"), ("div", "약정 구분"), ("fee", "월 요금(원)"),
     ("voice", "음성(분)"), ("sms", "문자(건)"), ("data", "데이터(MB)"), ("ov", "초과 음성(원/초)"), ("os", "초과 문자(원/건)"), ("od", "초과 데이터(원/MB)")]
json.dump({"source": "과학기술정보통신부 우정사업본부 「우체국알뜰폰 요금제 조회 서비스」(공공데이터포털 15075270, 공공누리 제1유형)",
           "fetched": d["fetched"], "count": len(rows), "items": rows}, open(H / "data" / "post_mvno_plans.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
with open(H / "data" / "post_mvno_plans.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow([k for _, k in F])
    for r in sorted(rows, key=lambda r: (r.get("fee") or 0)): w.writerow([r.get(k, "") for k, _ in F])
cheap = sorted(rows, key=lambda r: r.get("fee") or 0)[:10]
tbl = "\n".join(f"| {r['name']} | {r['net']} | {r['fee']:,}원 | {r['data']/1024:.1f}GB | {r['voice']}분 |" for r in cheap)
(H / "README.md").write_text(f"""# 우체국 알뜰폰 요금제 데이터 (2026)

우체국에서 가입할 수 있는 알뜰폰 요금제 **{len(rows)}개**를 정리한 공개 데이터입니다. (기준일 {d['fetched']})

- `data/post_mvno_plans.csv` — 월 요금 낮은 순 정렬(엑셀에서 바로 열림)
- `data/post_mvno_plans.json` — 원본 필드 그대로

## 월 요금 낮은 요금제 10개
| 요금제 | 통신망 | 월 요금 | 데이터 | 음성 |
|---|---|---|---|---|
{tbl}

## 내 사용량에 맞는 요금제 바로 찾기
데이터·통화량을 넣으면 맞는 요금제를 골라 주는 무료 조회 페이지: **https://tools.newbizok.com/post-mvno/**

## 출처
과학기술정보통신부 우정사업본부 「우체국알뜰폰 요금제 조회 서비스」 — [공공데이터포털 15075270](https://www.data.go.kr/data/15075270/openapi.do), 공공누리 제1유형(출처 표시). 할인·가입 조건은 인터넷우체국에서 최종 확인하세요.
""", encoding="utf-8")
print("ok", len(rows))
