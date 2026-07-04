#!/usr/bin/env python3
"""venv(edge_tts): 묵직한 남성 연설 톤. 텍스트→mp3. 사용: python _tts_dramatic.py <txt> <out.mp3>
실존 인물 성대 복제가 아니라, 일반 남성 나레이터 보이스(InJoon)를 느리게 써서 무게를 낸다."""
import sys, asyncio, edge_tts
txt=open(sys.argv[1],encoding="utf-8").read().strip()
asyncio.run(edge_tts.Communicate(txt,"ko-KR-InJoonNeural",rate="-12%").save(sys.argv[2]))
print("tts ok")
