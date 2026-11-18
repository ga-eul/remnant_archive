# 랜딩 페이지 (홍보용 소개 페이지)

SNS·텀블벅 등에서 들어온 사람에게 CASE 01 데모를 소개하는 페이지입니다.
게임 본편(`shinip/`)·허브(`index (1).html`)와는 별개이며, 서로 영향을 주지 않습니다.

```
landing/
├─ index.html      ← 랜딩 페이지 (디자인·동작이 이 파일 하나에 전부)
├─ images/         ← 페이지에서 쓰는 이미지 (스크린샷/ 폴더에서 복사해 온 사본)
└─ README.md
```

## 화면 구성 (버튼으로 넘기기)

길게 스크롤하는 대신 **한 번에 한 화면만 보이고, 버튼을 눌러 넘깁니다.**
화면은 9개이고 순서는 다음과 같습니다.

| # | id | 상단 바 버튼 | 내용 |
|---|---|---|---|
| 1 | `home` | 홈 | 히어로 — 제목·슬로건·[브라우저로 플레이]·[Windows 다운로드] |
| 2 | `about` | 소개 | 01 WELCOME — 줄거리 |
| 3 | `how` | 플레이 방식 | 02 HOW TO PLAY — 조사 방식 |
| 4 | `features` | 특징 | 03 FEATURES — 데모의 특징 |
| 5 | `shots` | 화면 | 04 SCREENS — 스크린샷·GIF (이미지를 누르면 확대) |
| 6 | `info` | 플레이 정보 | 05 INFO — 분량·사양 |
| 7 | `start` | 시작하기 | 06 START — 브라우저 플레이 / Windows 다운로드 안내 |
| 8 | `notice` | 안내 | 07 BEFORE YOU PLAY — 플레이 전 안내 |
| 9 | `next` | 다음 기록 | 08 NEXT — 후속 소식 |

넘기는 방법은 네 가지입니다.

- 상단 바의 화면 버튼 (지금 보는 화면은 청록색으로 표시)
- 각 화면 아래쪽 **[← 이전] / [다음 →]**
- 키보드 **← →**
- 주소창 `#about` 같은 해시. 브라우저 뒤로 가기·앞으로 가기도 화면 전환으로 동작합니다.

화면이 열릴 때마다 그 화면 안의 등장 효과(`.reveal`)가 다시 재생됩니다.
기기 설정이 '움직임 줄이기'면 전환 효과 없이 바로 바뀝니다.

화면을 더하거나 뺄 때는 ① `<section class="screen" id="...">`로 만들고 ② 상단 바 `.navlinks`에 `<button data-screen="...">`를 넣고 ③ `<script>`의 `NAMES`에 한글 이름을 추가합니다. [이전]/[다음]은 문서 순서대로 자동으로 붙습니다.

## 열어보기

- `landing/index.html`을 더블클릭하면 브라우저에서 바로 열립니다.
- 글꼴(Noto Sans KR, JetBrains Mono)은 인터넷에서 불러옵니다.
- [브라우저로 플레이]는 같은 사이트의 `play/`를 가리켜서, 파일을 직접 열면 동작하지 않습니다. 그 흐름까지 보려면 저장소 루트에서 `python release/build_release.py site` 뒤에 `site/`에서 서버를 띄웁니다.

## 버튼 주소 넣기 (중요)

`index.html` 아래쪽 `<script>` 맨 위 `LINKS` 세 줄만 채우면 버튼이 살아납니다.
비워 두면 그 버튼은 `(준비 중)`으로 잠기고 눌러도 아무 일도 일어나지 않습니다.

```js
const LINKS = {
  play:     'play/',                                        // 브라우저 플레이 (같은 사이트의 게임 폴더)
  download: 'https://summertumn.itch.io/remnant-archive',   // Windows 내려받기 (itch.io)
  x:        'https://x.com/remi_r_archive'                  // 공식 X 계정
};
```

같은 사이트 안의 주소(`play/`)면 같은 창에서, `http`로 시작하는 바깥 주소면 새 탭에서 열립니다.
세 줄 모두 채워져 있어 잠긴 버튼은 없습니다.

## 문구·이미지

- 문구는 `release/itch-store-page.md`(itch.io 상점 초안)와 같은 내용입니다. 한쪽을 고치면 다른 쪽도 함께 맞춥니다.
- 공개 범위는 `case 01/disclosure.md` CASE 01 기준입니다. 전임자의 정체·실험의 목적·최종 반전은 쓰지 않습니다.
- 이미지는 `스크린샷/`에서 복사한 사본입니다. 원본을 바꾸면 `landing/images/`에도 다시 복사해야 합니다.

| landing/images | 원본 |
|---|---|
| `01-hub.png` | `스크린샷/01-허브.png` |
| `02-intranet.png` | `스크린샷/02-사내인트라넷-래미.png` |
| `03-search.png` | `스크린샷/03-1차수색-기록보관실.png` |
| `04-interview.png` | `스크린샷/04-심문.png` |
| `05-cctv.png` | `스크린샷/05-단서-CCTV기록.png` |
| `06-myarchive.png` | `스크린샷/06-MyArchive-단서조합.png` |
| `g1-combine.gif` | `스크린샷/09-MyArchive-단서조합.gif` |
| `g2-remi-hint.gif` | `스크린샷/11-래미-십자말풀이-힌트.gif` |
| `logo.png` | `로고/기본_가로형_로고_흰색.png` |

## 올리기 (GitHub Pages 자동 배포)

`main`에 올리면 GitHub Actions(`.github/workflows/pages.yml`)가 사이트를 만들어 배포합니다.

```
/              ← landing/index.html
/images/       ← landing/images/
/play/         ← 허브 (index (1).html 을 index.html 로 바꿔 복사)
/play/shinip/  ← 게임
```

- 사이트 폴더를 만드는 것은 `python release/build_release.py site` 입니다. 결과는 저장소의 `site/` 폴더(Git에 올리지 않음)이며, 원본 파일은 고치지 않습니다.
- 올리기 전 눈으로 확인하려면: `python release/build_release.py site` → `site/`에서 `python -m http.server` → `http://127.0.0.1:8000/`
- 저장소 **Settings → Pages → Source**를 한 번 **GitHub Actions**로 설정해 두어야 합니다.
- 다른 호스팅(Netlify 등)에 올릴 때도 만들어진 `site/` 폴더를 그대로 올리면 됩니다.

## 화면 기준

PC 기준으로 만들었습니다(D80). 폭이 좁아지면 1~2단으로 접히지만, 휴대폰 화면 맞춤 검수는 하지 않았습니다.
`prefers-reduced-motion`(기기의 동작 줄이기)이 켜져 있으면 배경 확대·타이핑·카운터·등장 효과가 모두 멈춥니다.
