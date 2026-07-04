#!/usr/bin/env python3
"""venv(edge_tts): 파라미터 TTS. 사용: python _tts_param.py <txt> <out.mp3> <voice> <rate> <pitch>
실존 인물 성대 복제 아님 — 일반 남성 나레이터 보이스의 속도/피치만 문장별로 조절."""
import sys, asyncio, edge_tts
txt=open(sys.argv[1],encoding="utf-8").read().strip()
out=sys.argv[2]; voice=sys.argv[3]; rate=sys.argv[4]; pitch=sys.argv[5]
asyncio.run(edge_tts.Communicate(txt,voice,rate=rate,pitch=pitch).save(out))
print("ok")
