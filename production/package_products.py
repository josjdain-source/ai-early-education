# -*- coding: utf-8 -*-
"""유료 프로그램 6종 패키징 — products/{id}_v1.0.zip (스크립트+GUIDE.pdf+LICENSE).
공개 레포이므로 products/는 gitignore. 판매 사본은 경로 하드코딩을 완화(ffmpeg PATH·현재 파이썬 사용)."""
import io, sys, os, re, shutil, zipfile, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = r"C:/Users/admin/Desktop/ai-craft-kids"
DESK = r"C:/Users/admin/Desktop"
PROD = os.path.join(ROOT, "products")
STG = os.path.join(PROD, "_staging")
os.makedirs(PROD, exist_ok=True)
if os.path.isdir(STG): shutil.rmtree(STG)
os.makedirs(STG)

from fpdf import FPDF
MAL = r"C:\Windows\Fonts\malgun.ttf"; MALB = r"C:\Windows\Fonts\malgunbd.ttf"

class Guide(FPDF):
    def __init__(self, title):
        super().__init__("P", "mm", "A4")
        self.title_txt = title
        self.add_font("M", "", MAL); self.add_font("M", "B", MALB)
        self.set_auto_page_break(True, 18)
    def header(self):
        if self.page_no() == 1: return
        self.set_font("M", "", 8); self.set_text_color(150)
        self.cell(0, 6, f"{self.title_txt} · 아이와 AI교실", align="R"); self.ln(2)
        self.set_text_color(0)
    def cover(self, subtitle):
        self.add_page()
        self.ln(50)
        self.set_font("M", "B", 24); self.multi_cell(0, 12, self.title_txt, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(4); self.set_font("M", "", 12); self.set_text_color(90)
        self.multi_cell(0, 8, subtitle, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(8); self.multi_cell(0, 7, "아이와 AI교실 · ai-early-education.pages.dev", align="C", new_x="LMARGIN", new_y="NEXT")
        self.multi_cell(0, 7, "문의: 2011kstudentlife@gmail.com", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0)
    def h1(self, t):
        self.add_page(); self.set_font("M", "B", 15)
        self.set_fill_color(240, 236, 226); self.cell(0, 11, "  " + t, fill=True, new_x="LMARGIN", new_y="NEXT"); self.ln(3)
    def h2(self, t):
        self.ln(2); self.set_font("M", "B", 12); self.set_text_color(180, 74, 49)
        self.cell(0, 8, t, new_x="LMARGIN", new_y="NEXT"); self.set_text_color(0); self.ln(1)
    def p(self, t):
        self.set_font("M", "", 10.5); self.multi_cell(0, 6.4, t, new_x="LMARGIN", new_y="NEXT"); self.ln(1.5)
    def li(self, items):
        self.set_font("M", "", 10.5)
        for it in items: self.multi_cell(0, 6.4, "  •  " + it, new_x="LMARGIN", new_y="NEXT")
        self.ln(1.5)
    def code(self, t):
        # 한글 포함 시 Courier(라틴 전용) 대신 맑은고딕
        f = "Courier" if t.isascii() else "M"
        self.set_font(f, "", 9.5); self.set_fill_color(245, 245, 245)
        self.multi_cell(0, 5.6, t, fill=True, new_x="LMARGIN", new_y="NEXT"); self.set_font("M", "", 10.5); self.ln(1.5)

LICENSE = """[이용 조건 — 개인 사용권]
· 이 프로그램/자료는 구매자 본인의 개인적 사용을 위해 제공됩니다.
· 재판매·재배포·공유(파일 그대로 타인 전달)는 허용되지 않습니다.
· 이 도구로 만든 결과물(영상·이미지·글)은 자유롭게 사용·업로드·수익화할 수 있습니다.
· 설치가 어렵거나 오류가 나면 이메일로 도와드립니다: 2011kstudentlife@gmail.com
· 판매자: 아이와 AI교실 (ai-early-education.pages.dev)
"""

def put_license(d):
    open(os.path.join(d, "LICENSE.txt"), "w", encoding="utf-8").write(LICENSE)

def common_install(g, need_edge=True, need_ffmpeg=True, need_comfy=False, need_ollama=False):
    g.h1("1. 설치 (처음 한 번)")
    g.h2("파이썬")
    g.p("python.org/downloads 에서 Python 3.10 이상을 설치합니다. 설치 첫 화면에서 'Add python.exe to PATH'에 꼭 체크하세요.")
    if need_ffmpeg:
        g.h2("ffmpeg (영상 조립 엔진)")
        g.li(["gyan.dev/ffmpeg/builds 에서 'essentials' zip 다운로드 후 압축 해제",
              "압축 푼 곳의 bin 폴더 경로를 복사 (예: C:\\ffmpeg\\bin)",
              "윈도우 검색 → '환경 변수' → Path에 그 경로 추가",
              "확인: 새 명령창에서  ffmpeg -version  이 출력되면 성공"])
    if need_edge:
        g.h2("edge-tts (무료 음성)")
        g.code("pip install edge-tts")
    if need_ollama:
        g.h2("Ollama (로컬 대본 AI)")
        g.li(["ollama.com/download 에서 설치", "모델 받기:  ollama pull gemma2:9b",
              "이 프로그램은 http://127.0.0.1:11435 로 접속합니다 — 기본 포트(11434)를 쓰신다면 스크립트 상단 주소를 11434로 바꾸세요."])
    if need_comfy:
        g.h2("ComfyUI + 이미지 모델 (그림 생성 · GPU 필요)")
        g.li(["github.com/comfyanonymous/ComfyUI 설치(포터블 권장)",
              "모델: RealVisXL V5.0 (fp16) safetensors를 받아 ComfyUI/models/checkpoints 에 넣기",
              "실행 후 브라우저에서 127.0.0.1:8188 이 열리면 준비 완료",
              "GPU가 없다면: 이미지 생성 단계만 다른 도구(무료 웹 생성기)로 만들어 지정 폴더에 넣는 방식도 가이드 뒷부분에 있습니다."])

def sale_patch(src_text):
    """판매 사본 완화: ffmpeg/ffprobe는 PATH, TTS는 현재 파이썬으로."""
    t = src_text
    t = re.sub(r'FF\s*=\s*"[^"]*ffmpeg\.exe"', 'FF="ffmpeg"  # PATH에 설치(가이드 1장)', t)
    t = re.sub(r'FP\s*=\s*"[^"]*ffprobe\.exe"', 'FP="ffprobe"', t)
    t = re.sub(r'VENV\s*=\s*r?"[^"]*python\.exe"', 'VENV=sys.executable  # 현재 파이썬(edge-tts 설치 필요)', t)
    if "import sys" not in t.split("\n", 20)[0:20] and "sys" not in t:
        t = t.replace("import json", "import json, sys", 1)
    return t

def zip_dir(d, out):
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(d):
            for f in files:
                fp = os.path.join(root, f)
                z.write(fp, os.path.relpath(fp, d))
    return os.path.getsize(out)

results = []

# ══════════════ 1) 쇼츠 자동 빌더 ══════════════
def pkg_shorts():
    pid = "shorts-builder"; d = os.path.join(STG, pid); os.makedirs(d)
    src = open(os.path.join(ROOT, "production/build_ai_edu_shorts.py"), encoding="utf-8").read()
    t = sale_patch(src)
    t = t.replace('REPO="C:/Users/admin/Desktop/ai-craft-kids"; HERE=os.path.join(REPO,"production")',
                  'HERE=os.path.dirname(os.path.abspath(__file__)); REPO=HERE  # 이 폴더 기준')
    t = t.replace('PKG_DIR=os.path.join(REPO,"content_bank","approved","shorts")',
                  'PKG_DIR=os.path.join(REPO,"plans")  # 대본 JSON 폴더')
    t = t.replace('A=f"{REPO}/assets/ai-edu-shorts"', 'A=f"{REPO}/output"')
    # 스튜디오 등록(우리 내부 기능) 제거 → 안전 no-op
    t = re.sub(r'def register_to_studio\(.*?\n(?=def build_one)', 'def register_to_studio(pkg, mp4):\n    pass  # (판매판: 내부 스튜디오 연동 없음)\n\n', t, flags=re.DOTALL)
    open(os.path.join(d, "shorts_builder.py"), "w", encoding="utf-8").write(t)
    for f in ["_tts_param.py", "_tts_synth.py"]:
        shutil.copy(os.path.join(ROOT, "production", f), d)
    os.makedirs(os.path.join(d, "plans"))
    template = {
      "id": "my-first-short", "final_title": "내 첫 쇼츠 제목",
      "duration_target_sec": 45, "hook": "첫 문장 후킹",
      "script": "(전체 대본 — 참고용)",
      "cuts": [], "image_style": {"engine": "ComfyUI/RealVisXL", "aspect": "1080x1920",
        "style_token": "editorial storybook illustration, warm palette, no text",
        "negative": "photo, text, watermark, ugly"},
      "subtitles_all": "", "description": "유튜브 설명", "hashtags": ["태그1"],
      "links": {}, "pinned_comment": "고정댓글",
      "region": "kr",
      "beats": [
        {"role": "hook", "head": "큰 제목(화면 상단)", "text": "이 컷에서 읽을 내레이션 문장.", "prompt": "english image prompt for this cut", "region": "kr"},
        {"role": "fact", "head": "두번째 컷", "text": "두번째 내레이션.", "prompt": "english image prompt", "region": "kr"},
        {"role": "cta", "head": "마무리", "text": "마지막 문장.", "prompt": "english image prompt", "region": "kr"}
      ]
    }
    json.dump(template, open(os.path.join(d, "plans/plan_template.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    g = Guide("쇼츠 자동 빌더"); g.cover("대본 JSON 한 장 → 세로 쇼츠 mp4 자동 조립")
    common_install(g, need_edge=True, need_ffmpeg=True, need_comfy=True)
    g.h1("2. 사용법")
    g.li(["plans/plan_template.json 을 복사해 내 대본으로 수정 (beats = 컷 목록: head=화면 큰 글씨, text=내레이션, prompt=그림 프롬프트)",
          "ComfyUI 실행(127.0.0.1:8188) — GPU 없으면 4장 참고",
          "실행:"])
    g.code("python shorts_builder.py my-first-short")
    g.p("완성 mp4는 output/render/ 에 저장됩니다. 컷 프레임(png)도 output/sframe/ 에 남아 썸네일로 쓸 수 있습니다.")
    g.h1("3. 자주 묻는 문제")
    g.li(["소리 합칠 때 'invalid dts' 경고 → 무해합니다. 결과물 정상.",
          "그림이 실사처럼 나옴 → beats prompt에 'flat 2d illustration' 추가, negative에 photo 유지.",
          "음성이 여성으로 나옴 → _tts_param.py 호출부의 ko-KR-InJoonNeural(남)/SunHiNeural(여)로 교체.",
          "ComfyUI 응답 없음 → 다른 프로그램(Ollama 등)이 GPU 메모리를 잡고 있는지 확인."])
    g.h1("4. GPU가 없다면")
    g.p("이미지 생성만 외부에서 해도 됩니다: 무료 이미지 생성 사이트에서 컷별 그림을 만들어 output/simg/{대본id}_{컷번호}.png 이름으로 넣어두면, 빌더는 그 그림을 그대로 사용해 조립만 합니다.")
    g.output(os.path.join(d, "GUIDE.pdf")); put_license(d)
    return d

# ══════════════ 2) 영상 자동 생성기 ══════════════
def pkg_videomaker():
    pid = "video-maker"; d = os.path.join(STG, pid); os.makedirs(d)
    for f in ["make_illust_video.py", "reassemble_dissolve.py", "_tts_param.py", "_tts_synth.py"]:
        p = os.path.join(ROOT, "production", f)
        if os.path.exists(p):
            t = sale_patch(open(p, encoding="utf-8").read())
            open(os.path.join(d, f), "w", encoding="utf-8").write(t)
    gd = os.path.join(ROOT, "production/ILLUST_VIDEO_PIPELINE_GUIDE.txt")
    if os.path.exists(gd): shutil.copy(gd, os.path.join(d, "PIPELINE_상세설명.txt"))
    g = Guide("영상 자동 생성기"); g.cover("주제 한 줄 → 대본·그림·내레이션·조립까지 자동 롱폼")
    common_install(g, need_edge=True, need_ffmpeg=True, need_comfy=True, need_ollama=True)
    g.h1("2. 사용법")
    g.code('python make_illust_video.py "아이가 챗봇과 대화할 때 부모가 알아야 할 것"')
    g.li(["약 5분 소요(그림 18장 생성 기준)", "완성 mp4와 대본 로그 위치는 실행 후 콘솔에 출력됩니다",
          "스크립트 상단의 경로 상수(저장 폴더 등)는 본인 PC에 맞게 수정 가능합니다"])
    g.h1("3. 자주 묻는 문제")
    g.li(["Ollama 접속 실패 → ollama serve 실행 여부·포트(11435/11434) 확인",
          "그림 생성이 멈춤 → ComfyUI가 GPU 메모리 부족일 수 있음. Ollama 모델을 내리고(ollama stop) 다시 시도",
          "글자가 그림에 섞여 나옴 → 스타일은 파이프라인이 고정 적용하므로 프롬프트에 텍스트 요구를 넣지 마세요"])
    g.output(os.path.join(d, "GUIDE.pdf")); put_license(d)
    return d

# ══════════════ 3) 캡컷 에이전트 ══════════════
def pkg_capcut():
    pid = "capcut-agent"; d = os.path.join(STG, pid); os.makedirs(d)
    src = os.path.join(DESK, "캡컷에이전트")
    for item in ["app.py", "core", "static", "requirements.txt", "run.bat"]:
        s = os.path.join(src, item)
        if os.path.isdir(s):
            shutil.copytree(s, os.path.join(d, item), ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        elif os.path.exists(s):
            shutil.copy(s, d)
    os.makedirs(os.path.join(d, "data"), exist_ok=True)
    g = Guide("캡컷 에이전트"); g.cover("한국어 토킹 영상 — 무음컷·자막·점프컷 초안 자동")
    common_install(g, need_edge=False, need_ffmpeg=True)
    g.h2("파이썬 패키지")
    g.code("pip install -r requirements.txt")
    g.h1("2. 사용법")
    g.li(["run.bat 더블클릭 → 브라우저에서 http://127.0.0.1:8910 접속",
          "영상 파일을 올리면: 무음 구간 컷 목록 · 자막 초안 · 잔말(음… 어…) 후보 · 미리보기 mp4 · 점프컷 초안이 생성됩니다",
          "캡컷을 쓰신다면 생성된 초안을 불러와 마무리 편집"])
    g.h1("3. 자주 묻는 문제")
    g.li(["포트 충돌(8910 사용 중) → app.py 상단 포트 숫자 변경",
          "자막 오탈자 → 자동 전사는 초안입니다. 반드시 사람이 검수하세요"])
    g.output(os.path.join(d, "GUIDE.pdf")); put_license(d)
    return d

# ══════════════ 4) 네이버 블로그 레이더 ══════════════
def pkg_radar():
    pid = "blog-radar"; d = os.path.join(STG, pid); os.makedirs(d)
    src = os.path.join(DESK, "naver_blog_radar")
    for item in os.listdir(src):
        if item in ("__pycache__", "outputs", ".git"): continue
        s = os.path.join(src, item)
        if os.path.isdir(s):
            shutil.copytree(s, os.path.join(d, item), ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else:
            shutil.copy(s, d)
    os.makedirs(os.path.join(d, "outputs"), exist_ok=True)
    g = Guide("네이버 블로그 레이더"); g.cover("붙여넣은 글을 5초 이해 점수로 진단 · 제목/구성 제안")
    common_install(g, need_edge=False, need_ffmpeg=False)
    g.h1("2. 사용법")
    g.li(["글 텍스트를 준비합니다(크롤링 없음 — 본인 글을 복사해서 사용)", "실행:"])
    g.code("python app.py")
    g.li(["안내에 따라 글을 붙여넣으면: 5초 이해 점수 · 제목 후보 · 이미지 배치 제안 · 10단 재구성안이 출력됩니다",
          "결과는 outputs/ 폴더에 저장됩니다"])
    g.h1("3. 참고")
    g.p("이 도구는 텍스트 분석만 합니다. 네이버 접속·크롤링·자동 발행 기능이 없으며, 결과는 글다듬기 보조용입니다.")
    g.output(os.path.join(d, "GUIDE.pdf")); put_license(d)
    return d

# ══════════════ 5) 밈 카툰 변환기 ══════════════
def pkg_meme():
    pid = "meme-cartoon"; d = os.path.join(STG, pid); os.makedirs(d)
    src = os.path.join(DESK, "meme_cartoon_maker")
    keep_files = [f for f in os.listdir(src) if f.endswith((".py", ".md"))]
    for f in keep_files:
        shutil.copy(os.path.join(src, f), d)
    if os.path.isdir(os.path.join(src, "config")):
        shutil.copytree(os.path.join(src, "config"), os.path.join(d, "config"),
                        ignore=shutil.ignore_patterns("__pycache__"))
    os.makedirs(os.path.join(d, "input"), exist_ok=True)
    os.makedirs(os.path.join(d, "output"), exist_ok=True)
    g = Guide("밈 카툰 변환기"); g.cover("사진 → 두꺼운 선 밈 카툰 패널(말풍선 포함) PNG")
    common_install(g, need_edge=False, need_ffmpeg=False)
    g.h2("파이썬 패키지")
    g.code("pip install opencv-python pillow numpy")
    g.h1("2. 사용법")
    g.li(["변환할 사진을 input/ 에 넣습니다", "기본 변환(GPU 불필요):"])
    g.code('python run_cartoonize.py input/사진.jpg --preset meme_panel --text "대사!" --speaker auto')
    g.li(["결과 PNG는 output/ 에 저장", "환경 점검:  python run_cartoonize.py --doctor"])
    g.h1("3. 참고")
    g.p("--compare 옵션을 붙이면 원본과 변환본을 나란히 붙인 비교 이미지도 만들어 줍니다. 고급(디퓨전) 모드는 별도 GPU 설정이 필요하며 기본 모드만으로도 밈 패널 제작에 충분합니다.")
    g.output(os.path.join(d, "GUIDE.pdf")); put_license(d)
    return d

# ══════════════ 6) 12주 워크북 부모 해설판 ══════════════
def pkg_workbook():
    pid = "workbook-guide"; d = os.path.join(STG, pid); os.makedirs(d)
    sys.path.insert(0, ROOT)
    import country_reality as CR
    p = CR.PROG12["uk"]; weeks = p["weeks"]
    EXTRA = {1:("아이가 순서를 빠뜨리지 않고 말했나요?","한 단계만 더 잘게 쪼개서 다시 말해볼까?"),
     2:("틀린 곳을 스스로 찾았나요?","어디를 고치면 될지 네 말로 다시 말해줄래?"),
     3:("반복되는 부분을 묶어서 말했나요?","'3번 반복'처럼 한 번에 말해볼까?"),
     4:("'만약 ~라면'을 써서 말했나요?","다른 경우라면 어떻게 할지 하나만 더 정해볼까?"),
     5:("고양이가 아이 명령대로 움직였나요?","걸음 수를 바꾸면 어떻게 될까? 바꿔서 다시 해볼까?"),
     6:("원하는 말과 소리가 나왔나요?","다른 말로 바꿔서 다시 시켜볼까?"),
     7:("캐릭터가 계속 움직이나요?","더 빠르게(느리게) 하려면 뭘 고칠까?"),
     8:("점수가 잘 올라가나요?","더 재밌게 만들 한 가지를 정해 다시 바꿔볼까?"),
     9:("표와 그래프가 맞게 그려졌나요?","다른 질문으로 한 번 더 조사해볼까?"),
     10:("나눈 규칙을 말로 설명했나요?","헷갈리는 카드 하나로 규칙을 다시 정해볼까?"),
     11:("'어떻게 아는지' 추측을 말했나요?","다른 AI를 찾아 같은 질문을 해볼까?"),
     12:("이상한 부분을 하나 찾았나요?","'이렇게 바꿔줘'라고 정확히 다시 말해볼까?")}
    PART_NOTE = {
      "1부": "1~4주는 '컴퓨팅적 사고'의 뼈대입니다. 컴퓨터 없이도 됩니다 — 핵심은 아이가 자기 생각을 순서·조건·반복으로 말해보는 경험입니다. 부모는 정답을 알려주는 사람이 아니라, 아이의 말이 더 정확해지도록 한 번 더 묻는 사람입니다.",
      "2부": "5~8주는 '직접 만들기'입니다. 결과물의 완성도는 중요하지 않습니다. 아이가 만들다 막혔을 때 '어디를 바꾸면 될까?'로 스스로 고치게 하는 것 — 그 한 번의 수정 경험이 이 파트의 전부입니다.",
      "3부": "9~12주는 '데이터와 AI 생각'입니다. AI의 답을 그대로 믿지 않고, 근거를 따지고, 다시 묻는 습관을 완성합니다. 이 4주가 워크북 전체의 목적지입니다.",
    }
    def part_of(n): return "3부" if n >= 9 else ("2부" if n >= 5 else "1부")
    g = Guide("12주 워크북 · 부모 해설판"); g.cover("주차별 부모 해설 + 대화 스크립트 + 체크시트\n(무료 12주 워크북과 함께 사용하는 확장판)")
    g.h1("이 해설판 사용법")
    g.p("무료 12주 워크북(ai-early-education.pages.dev/free/uk-12weeks-workbook)이 '아이용 활동지'라면, 이 해설판은 '부모용 진행 대본'입니다. 매주 활동 전에 해당 주차 해설을 1분만 읽고 시작하세요.")
    g.li(["주당 총 시간: 30~40분 × 2회면 충분합니다. 길게 한 번보다 짧게 두 번이 낫습니다.",
          "아이가 활동을 거부하는 날은 건너뛰세요. 12주는 목표가 아니라 리듬입니다.",
          "칭찬은 결과가 아니라 행동에: '다시 물어봤네!' '스스로 고쳤네!'"])
    for w in weeks:
        n, title = w[0], w[1]
        rest = [x for x in w[2:] if isinstance(x, str)]
        part = part_of(n)
        g.h1(f"{n}주차 · {title}  ({part})")
        if n in (1, 5, 9):
            g.h2("이 파트를 시작하며"); g.p(PART_NOTE[part])
        g.h2("부모 해설 — 이번 주에 실제로 기르는 힘")
        g.p(f"이번 주 활동의 겉모습은 '{title}'이지만, 속에서 기르는 건 자기 생각을 구조로 표현하는 힘입니다. "
            "아이가 서툴게 해도 고쳐주지 마시고, 아이 입에서 더 정확한 말이 나올 때까지 질문으로 기다려 주세요.")
        if rest:
            g.h2("이번 주 활동 요약(워크북 내용)")
            g.li(rest[:4])
        q1, q2 = EXTRA[n]
        g.h2("이번 주 대화 스크립트")
        g.li([f"활동 중간에: \"{q2}\"",
              f"활동 끝나고: \"{q1}\"",
              "잘 안 됐을 때: \"오늘은 어디까지 됐어? 다음엔 뭐부터 해볼까?\" (실패를 다음 계획으로 바꿔주기)"])
        g.h2("체크시트 (오늘 활동 후 체크)")
        g.li([f"□ {q1}", "□ 아이가 스스로 한 부분을 한 가지 말로 표현했다",
              "□ 부모가 답을 알려주지 않고 질문으로 진행했다"])
    g.h1("수료 후 — 다음 단계")
    g.p("12주를 마쳤다면 아이는 '말하기→고치기→의심하기'의 기초 근육이 생긴 상태입니다. 다음은 매일 10분 수업(daily-class)으로 리듬을 유지하고, 아이 나이에 맞는 다음 계단은 levels 페이지에서 확인하세요.")
    g.output(os.path.join(d, "12주_부모해설판.pdf")); put_license(d)
    return d

# ══════════════ 실행 ══════════════
for fn, pid in [(pkg_shorts, "shorts-builder"), (pkg_videomaker, "video-maker"),
                (pkg_capcut, "capcut-agent"), (pkg_radar, "blog-radar"),
                (pkg_meme, "meme-cartoon"), (pkg_workbook, "workbook-guide")]:
    try:
        d = fn()
        out = os.path.join(PROD, f"{pid}_v1.0.zip")
        size = zip_dir(d, out)
        results.append((pid, "OK", f"{size//1024}KB"))
        print(f"✓ {pid}_v1.0.zip  ({size//1024} KB)")
    except Exception as e:
        results.append((pid, "FAIL", str(e)[:80]))
        print(f"✗ {pid}: {e}")

print("\n요약:")
for r in results: print(" ", r)
