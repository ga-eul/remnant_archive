"""배포용 묶음 만들기
  python release/build_release.py        → release/dist/ 에 zip 3개
    1) RemnantArchive-web-<버전>.zip        웹 배포용(itch.io HTML 등). zip 맨 위에 index.html
    2) RemnantArchiveDemo-<버전>-win-itch.zip     itch.io용 Windows exe + 실행 안내
    3) RemnantArchiveDemo-<버전>-win-dropbox.zip  드롭박스 공유용 exe + 실행 안내(드롭박스 경고 줄 포함)
  python release/build_release.py site   → site/ 에 GitHub Pages용 폴더 (/ = 랜딩, /play/ = 허브+게임)
원본 게임 파일은 고치지 않는다. 복사본에서만 허브 파일 이름을 index.html로 바꾸고 허브 주소 세 곳을 함께 바꾼다.
exe는 desktop/에서 `npm run dist`로 먼저 만들어 둔다. site는 exe가 없어도 만들어진다.
실행: 저장소 루트에서"""
import json, os, shutil, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, 'dist')
SITE = os.path.join(ROOT, 'site')
VERSION = json.load(open(os.path.join(ROOT, 'desktop', 'package.json'), encoding='utf-8'))['version']

PAGES = ['index (1).html', 'first-launch-notice-terminal.html', 'loading.html', 'shinip_demo_complete.html']
HUB_OLD, HUB_NEW = 'index (1).html', 'index.html'
# 웹용 복사본에서만 바꾸는 곳: (파일, 원래 문자열, 바꿀 문자열) — 각각 정확히 한 번 있어야 한다
WEB_EDITS = [
    ('shinip/js/main.js', "const HUB_URL = '../index (1).html';", "const HUB_URL = '../index.html';"),
    ('shinip_demo_complete.html', "const HUB_URL = 'index (1).html';", "const HUB_URL = 'index.html';"),
    ('loading.html', 'data-next="index (1).html"', 'data-next="index.html"'),
]
DROPBOX_LINE = '- 드롭박스 로그인·가입 창 → 창을 닫고 [다운로드] (로그인 없이 받을 수 있습니다)\n'


def fail(msg):
    print('[release] ' + msg); sys.exit(1)


def web_files():
    """(zip 안 경로, 원본 경로) 목록"""
    files = [(HUB_NEW if p == HUB_OLD else p, os.path.join(ROOT, p)) for p in PAGES]
    for base, _, names in os.walk(os.path.join(ROOT, 'shinip')):
        for n in names:
            src = os.path.join(base, n)
            files.append((os.path.relpath(src, ROOT).replace(os.sep, '/'), src))
    return sorted(files)


def web_entries():
    """(배포 경로, 원본 경로, 바꾼 내용 또는 None) — 허브 주소 세 곳을 복사본에서만 바꾼다"""
    edits = {f: (a, b) for f, a, b in WEB_EDITS}
    out = []
    for arc, src in web_files():
        if arc in edits:
            text = open(src, encoding='utf-8').read()
            old, new = edits.pop(arc)
            if text.count(old) != 1:
                fail(f'{arc}: "{old}"가 {text.count(old)}번 있습니다 (1번이어야 함)')
            out.append((arc, src, text.replace(old, new)))
        else:
            out.append((arc, src, None))
    if edits:
        fail('바꾸지 못한 파일: ' + ', '.join(edits))
    return out


def build_web():
    name = os.path.join(OUT, f'RemnantArchive-web-{VERSION}.zip')
    with zipfile.ZipFile(name, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for arc, src, text in web_entries():
            if text is None:
                z.write(src, arc)
            else:
                z.writestr(arc, text.encode('utf-8'))
        n = len(z.namelist())
    if n > 1000:
        fail(f'파일 {n}개 — itch.io HTML 업로드 한도(1000개)를 넘습니다')
    return name, n


def build_site():
    """GitHub Pages용 폴더 site/ — / = 랜딩 페이지, /play/ = 허브와 게임"""
    landing = os.path.join(ROOT, 'landing')
    if not os.path.exists(os.path.join(landing, 'index.html')):
        fail('landing/index.html 이 없습니다')
    if os.path.exists(SITE):
        shutil.rmtree(SITE)
    os.makedirs(SITE)
    # 랜딩 페이지 → 사이트 루트 (README.md는 올리지 않는다)
    shutil.copy2(os.path.join(landing, 'index.html'), os.path.join(SITE, 'index.html'))
    shutil.copytree(os.path.join(landing, 'images'), os.path.join(SITE, 'images'))
    # 허브와 게임 → /play/
    n = 2
    for arc, src, text in web_entries():
        dst = os.path.join(SITE, 'play', *arc.split('/'))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if text is None:
            shutil.copy2(src, dst)
        else:
            open(dst, 'w', encoding='utf-8', newline='').write(text)
        n += 1
    # Jekyll이 밑줄로 시작하는 파일을 빼먹지 않도록
    open(os.path.join(SITE, '.nojekyll'), 'w').close()
    return SITE, n


def build_exe(host):
    exe = os.path.join(ROOT, 'desktop', 'dist', f'RemnantArchiveDemo-{VERSION}-portable.exe')
    if not os.path.exists(exe):
        fail(f'{exe} 이 없습니다. desktop/에서 npm run dist를 먼저 실행하세요.')
    note = open(os.path.join(HERE, '실행 안내.txt'), encoding='utf-8').read()
    note = note.replace('{VERSION}', VERSION).replace('{HOST_WARNING}', DROPBOX_LINE if host == 'dropbox' else '')
    note = '﻿' + note.replace('\r\n', '\n').replace('\n', '\r\n')     # 메모장에서 한글이 깨지지 않게 UTF-8(BOM)·CRLF
    name = os.path.join(OUT, f'RemnantArchiveDemo-{VERSION}-win-{host}.zip')
    with zipfile.ZipFile(name, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr('RemnantArchiveDemo/실행 안내.txt', note.encode('utf-8'))
        z.write(exe, f'RemnantArchiveDemo/{os.path.basename(exe)}')
    return name


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'site':
        path, n = build_site()
        print(f'[release] {os.path.relpath(path, ROOT)}/  (파일 {n}개) — / 랜딩, /play/ 게임')
        sys.exit(0)
    if len(sys.argv) > 1:
        fail(f'모르는 인자: {sys.argv[1]} (쓸 수 있는 값: site)')
    os.makedirs(OUT, exist_ok=True)
    web, n = build_web()
    print(f'[release] {os.path.relpath(web, ROOT)}  (파일 {n}개)')
    for host in ('itch', 'dropbox'):
        print('[release] ' + os.path.relpath(build_exe(host), ROOT))
