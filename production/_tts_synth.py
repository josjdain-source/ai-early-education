#!/usr/bin/env python3
"""venv(edge_tts)로 실행: 텍스트파일 → mp3. 사용: python _tts_synth.py <txt> <out.mp3>"""
import sys, asyncio, edge_tts
txt=open(sys.argv[1],encoding="utf-8").read().strip()
asyncio.run(edge_tts.Communicate(txt,"ko-KR-SunHiNeural",rate="-8%").save(sys.argv[2]))
print("tts ok")
