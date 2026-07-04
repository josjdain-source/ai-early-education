# 국가별 AI교육 콘텐츠 패키지 시스템 (진실원본 런북)

> 한 국가 주제 하나로 **조사 → 롱폼 다큐 → 쇼츠 → 심층 페이지 → 유튜브 비공개 업로드**까지 한 번에.
> 첫 패키지 = **중국 편**(완성). 이 구조를 미국·영국·싱가포르·한국으로 복제한다.

## 편성 원칙 (절대 규칙)
1. **각 영상은 3단으로 완결**: `[그 나라는 이렇게] → [한국은 이렇게] → [그럼 아이는 이렇게 자란다]`
   - 남의 나라 소개로 끝내지 않는다. 반드시 한국 부모 행동 + 아이 효과로 닫는다.
   - 아이 효과 예: 스스로 확인하는 아이 / 스스로 판단하는 아이 / 속지 않는 아이.
2. **쇼츠 첫 2초 = 칼날 후킹** (롱폼을 자르지 말고 독립 후킹으로 재작성).
3. **출처 없는 수치·정책 금지**. 모든 수치는 `facts/*.json`에 근거(sources 연결). 조사 먼저.
4. **자극화 금지**: 감시국가/공포/군사/뇌파밴드/얼굴감시 프레임 금지. 관점 = 국가주도 AI 리터러시·교육과정 편입·윤리적 사용.
5. **인물은 동아시아**, 비트별 국적 분리: 그 나라 파트 = 그 나라 사람(중국편=Chinese), 한국 파트 = Korean. (SDXL 프롬프트에 민족 주입 + NEG에 western/caucasian)
6. **공개는 사람**: 업로드는 항상 private. 채널 = 아이와 AI교실. 공개 승인은 사람이 스튜디오에서.

## 산출물 규격
- **롱폼**: 6~8분, 일러스트 다큐 explainer, 1280x720, 약한 켄번즈 1.0→1.06 + 디졸브. 섹션 8~10 × 3컷. 3층 구조(역사→운영→미래세대→한국→아이효과).
- **쇼츠**: 3편, 세로 1080x1920, 각 8비트, 재생속도 120%(atempo 1.2) ≈ 33~40초. 상단 후킹·중앙 일러스트·하단 자막·빠른 디졸브(XF 0.25).
- **심층 페이지**: `/world-cases/{country}.html` — 타임라인·3층 운영구조·한국 배울점·**아이 효과 섹션**·부모 질문 10·롱폼 임베드·쇼츠 카드·출처. + `/videos/{country}-ai-education.html`.

## 파일 지도 (중국 예시 → 국가별 교체)
```
sources/china_ai_education_sources.json      # 출처 목록 (research)
facts/china_ai_education_facts.json          # 근거 사실 (각 fact→sources)
production/china_ai_education_longform_plan.json   # 10섹션×3컷 (narration+beats+fact)
production/china_ai_education_shorts_plan.json     # 3쇼츠×8비트 (region:cn/kr, role, head/text/prompt)
production/china_ai_education_metadata.json        # 제목후보·설명·태그·썸네일문구
production/build_china_ai_longform.py         # SDXL+오버레이+디졸브 조립
production/build_china_ai_shorts.py           # 세로 프레임+120%+디졸브 (eth(region), sdxl 3회 재시도)
build_china_page.py                           # 심층 페이지 (build_site 헬퍼 재사용, 임베드 ID는 큐에서)
youtube/register_china_queue.py               # 큐 등록(private)+포스터
```

## 실행 순서 (파이프라인)
```bash
cd C:/Users/admin/Desktop/ai-craft-kids
# 0) ★VRAM 확보 (필수): Ollama 모델 언로드 안 하면 ComfyUI가 VRAM 부족으로 hang
curl -s "http://127.0.0.1:11435/api/generate" -d '{"model":"gemma2:9b","keep_alive":0}'
# 1) 조사 → sources/facts JSON 작성 (WebSearch, 출처 필수)
# 2) 롱폼 플랜 + 빌드
python production/build_china_ai_longform.py      # 이미지 캐시: img/ 있으면 재사용
# 3) 쇼츠 플랜 + 빌드
python production/build_china_ai_shorts.py
# 4) 큐 등록(private) + 포스터
python youtube/register_china_queue.py
# 5) ★업로드 자동 금지. 조종판 '🎬 업로드 검수대'(python youtube/upload_desk.py, 8971)에서
#    사람이 '승인' 누른 것만 비공개 업로드. 파이프라인은 큐에 ready_to_upload로 등록만 한다.
#    (수동 단건은 python youtube/upload_to_aiclassroom.py --id <vid> 도 가능하나 원칙은 검수대)
#    ※ 유튜브 일일 업로드 한도 있음 — 최종 확정 후 1회만. 재렌더 재업로드 남발 금지.
# 6) 페이지 생성(임베드 ID 자동 반영) + 배포
python build_site.py                              # build_china_page 포함 호출됨
git archive main | tar -x -C $TMP && npx -y wrangler pages deploy $TMP --project-name=ai-early-education --branch=main --commit-dirty=true
```

## 함정과 해결 (실전 교훈)
- **ComfyUI hang**: 원인 대개 **Ollama가 GPU VRAM 점유**(gemma2:9b ≈ 7.4GB). 빌드 전 `keep_alive:0`로 언로드. `nvidia-smi`로 확인.
- **동시 빌드 충돌**: 빌드 프로세스는 **한 번에 하나만**. 좀비 프로세스가 ComfyUI 큐를 오염시킴. `nohup` 대신 관리형 백그라운드/포그라운드.
- **대사만 바꿀 때**: 프롬프트 유지하면 `simg/img` 이미지 **캐시 재사용**(os.path.exists) → TTS+조립만, GPU 안 씀, 빠름. (단, 비트 삽입은 인덱스 밀림 주의)
- **sdxl 견고화**: 3회 재시도 + `h[pid].get("outputs")` 확인 내장.
- **로컬 용량**: 렌더 mp4는 gitignore(유튜브가 원본). youtube_url 기록 후 1일 뒤 `cleanup_local_videos.py`가 자동 삭제.
- **임베드 재생**: private면 홈페이지에서 "재생 불가". 사람이 공개 승인해야 재생. ID는 큐에서 읽어 자동 반영.

## 새 국가 복제 방법
1. 조사: WebSearch로 그 나라 AI교육 정책/수치 수집 → `sources/{c}_sources.json`, `facts/{c}_facts.json` (출처 필수).
2. 중국 플랜 3종(longform_plan/shorts_plan/metadata) 복사 → 내용을 그 나라 facts로 교체. **쇼츠는 반드시 [그나라→한국→아이효과] 구조**.
3. build 스크립트 2개 복사, 경로/파일명만 교체(A=assets/{c}-ai-education). eth(region) 그대로.
4. build_{c}_page.py 복사, TIMELINE/LAYERS/EFFECTS 교체.
5. 파이프라인 실행. 채널·private·공개 규칙 동일.

## 중국 편 결과 (레퍼런스)
- 롱폼 6.85분(10섹션): youtu.be/L3wfb0G4yDY
- 쇼츠 3편(각 그나라→한국→아이효과): -8GdfpFm-70 / 0G1i0Bt1L5I / rub0f4ZqhlY
- 페이지: /world-cases/china (타임라인·3층·한국·아이효과·질문10·출처14)
- ※ 위 ID는 재업로드 시 갱신됨. 실제 최신은 youtube/upload_queue.json 참조.
