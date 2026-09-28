# 에토스 카드뉴스 디자인·제작 지침 v3.3

### ETHOS BRIEF Deterministic Rendering · Visual Continuity · Editorial Density

> 적용 대상: 한국어·영어·아랍어 ETHOS BRIEF 카드뉴스
>
> 이 문서는 카드뉴스의 시각 설계, 코드 구현, 렌더링, 자동 검사, 시각 검수 기준을 규정한다.
> 사실·법률·논리·카피는 최신 마스터 지침과 글쓰기 지침을 따른다.
>
> 목표는 단순한 카드형 콘텐츠가 아니라 뉴스 통신사·정책 브리프·프리미엄 에디토리얼 수준의 결과물을 매번 같은 품질로 재현하는 것이다.

---

## v3.3 핵심 변경

v3.2의 Visual Golden Reference, Editorial Density Lock, One Dominant Visual Rule, CTA Composition Lock, Codex Build Spec, Visual QA를 모두 유지한다.

다음 제작 규칙을 새로 추가하거나 강화한다.

1. 텍스트가 있는 카드뉴스는 코드 렌더링을 기본이 아니라 의무로 지정
2. 이미지 생성 모델의 사용 범위를 텍스트 없는 보조 이미지로 제한
3. Google Fonts 네트워크 호출 대신 로컬 폰트 파일 사용
4. 필수 폰트가 로드되지 않으면 대체 글꼴로 출력하지 않고 실패 처리
5. 공통 헤더·푸터·페이지 번호를 단일 프레임 컴포넌트로 고정
6. 디자인 토큰을 단일 소스로 관리
7. Playwright 번들 Chromium과 렌더 조건을 고정
8. DOM 기반 오버플로·클리핑·폰트·색상·프레임 검사 추가
9. Playwright screenshot regression과 Golden Reference 비교를 분리 운영
10. Source Trace와 Fact Lock / Copy Flex 추가
11. 렌더 실패 시 임의 대체 출력을 금지하는 Fail-Closed 원칙 도입
12. 납품 산출물과 QA 보고서 형식 고정

---

# PART 0. 적용 순서와 절대 원칙

## 0-1. 지침 우선순위

충돌이 생기면 다음 순서로 판단한다.

1. 현재 작업에서 사용자가 직접 지정한 요구사항
2. 현재 프로젝트의 최상위 운용지침과 프로젝트별 CTA·법률·문체 규칙
3. 현재 작업에 제공된 승인 ETHOS BRIEF Golden Reference
4. 이 지침 v3.3
5. 승인된 카드별 Build Spec
6. Codex의 구현 판단

Golden Reference가 있더라도 사실·법률·카피 규칙을 바꿀 수 없다.

---

## 0-2. 제작 모드 잠금

### A. CODE RENDER — 의무

다음 작업은 HTML/CSS 또는 승인된 코드 템플릿으로 제작하고 Playwright로 렌더한다.

- 법률·행정·정책·비자·교육 카드뉴스
- 한글·영문·아랍어 텍스트가 포함된 카드
- 2장 이상의 캐러셀
- 정확한 브랜드 프레임이 필요한 작업
- 승인된 Golden Reference를 재현해야 하는 작업
- 사건번호·날짜·금액·법령명 등 Fact Lock 정보가 있는 작업

### B. IMAGE GENERATION — 제한 사용

이미지 생성 모델은 다음 요소에만 사용할 수 있다.

- 텍스트가 없는 사진형 배경
- 텍스트가 없는 삽화
- 추상 질감
- 카드 안에 들어가는 보조 이미지

### 금지

- 이미지 생성 모델로 헤드라인·본문·워드마크·페이지 번호를 그리지 않는다.
- 생성 이미지 안에 한글·영문·아랍어 문장을 넣지 않는다.
- 생성 모델이 만든 도형으로 공통 헤더·푸터·골드바를 대체하지 않는다.
- 승인된 Golden Reference 전체를 이미지 생성 모델로 재현하지 않는다.

---

## 0-3. 결정론적 렌더링 원칙

같은 소스와 같은 렌더 환경에서는 같은 픽셀이 나와야 한다.

이를 위해 다음을 고정한다.

- 폰트 파일과 버전
- 브라우저와 버전
- CSS viewport
- device scale factor
- locale과 timezone
- 디자인 토큰
- 공통 프레임 컴포넌트
- 카드 데이터
- 애니메이션 상태
- 외부 네트워크 의존성

시스템 폰트와 네트워크 폰트에 기대지 않는다.

---

## 0-4. Fail-Closed

다음 조건 중 하나라도 충족되지 않으면 PNG를 최종본으로 납품하지 않는다.

- 필수 폰트 로드 성공
- Golden Reference 접근 성공 또는 미제공 사실 명시
- 모든 카드의 정확한 출력 크기 확인
- 오버플로·클리핑 0건
- 필수 헤더·푸터·페이지 번호 존재
- 금지 문구·금지 채널 0건
- Fact Lock 값 원문과 일치
- 실제 브라우저 렌더 확인

실패했을 때 유사 폰트, 임의 색상, 축소된 글자, 잘린 문장으로 대신 출력하지 않는다.

---

## 0-5. 장별 절대 원칙

1. 한 카드에는 핵심 메시지 하나만 둔다.
2. 대표 시각 장치는 원칙적으로 하나만 둔다.
3. 헤드라인이 시각적 주인공이어야 한다.
4. 중요한 정보가 아닌 요소는 한두 단계 낮춘다.
5. 장 수보다 가독성과 정보 위계를 우선한다.
6. 본문을 줄이기 전에 카드 분리를 먼저 검토한다.
7. 본문 글자를 줄여 문제를 숨기지 않는다.
8. 카드뉴스를 웹페이지·대시보드·랜딩페이지처럼 만들지 않는다.

---

# PART 1. 콘텐츠 잠금

## 1-1. Source of Truth

카드 문구는 승인된 원문을 기준으로 한다.

카드 제작 단계에서 할 수 있는 일은 다음과 같다.

- 발췌
- 압축
- 순서 조정
- 문장 분리
- 의미를 바꾸지 않는 범위의 제목화
- 관계·순서·비교의 시각화

원문에 없는 숫자·법령·벌칙·사건번호·사례·판례·재결례·비자 결론·비용·처리기간을 만들지 않는다.

`출처 입력`, `사진 설명을 입력하세요`처럼 편집기에서 남은 표시를 카드 카피로 쓰지 않는다.

---

## 1-2. Source Trace

각 카드의 내부 작업명세에 출처를 기록한다.

```text
SOURCE TRACE
- Source document:
- Source section:
- Source paragraph or sentence:
- Evidence label: F / I / S
- Reference date:
- Semantic compression allowed: Yes / No
```

- F: 확인된 사실
- I: 확인된 사실을 바탕으로 한 해석
- S: 이해를 위한 가정 사례

카드 화면에 이 내부 정보를 모두 노출할 필요는 없다.

---

## 1-3. Fact Lock / Copy Flex

### FACT LOCK

다음 항목은 의미가 달라지지 않도록 원문과 대조한다.

- 법령명과 조문
- 날짜와 기간
- 금액과 비율
- 사건번호와 재결번호
- 기관명과 비자명
- 판결·재결의 결론
- 자격요건과 제한
- 직접 인용

### COPY FLEX

다음 항목은 의미를 유지하는 범위에서 카드에 맞게 압축할 수 있다.

- 표지 헤드라인
- 설명 문장
- 섹션 라벨
- 브리지 문구
- 결론 문장의 길이

Copy Flex도 원문에 없는 사실이나 단정을 추가할 수 없다.

---

# PART 2. Visual Golden Reference

## 2-1. 역할

승인된 ETHOS BRIEF 산출물은 단순 참고 이미지가 아니라 시각 기준이다.

비교 항목:

- 전체 구도
- 헤드라인 비중
- 세리프의 인상
- 정보 밀도
- 네이비·크림 리듬
- 골드 사용량
- 박스 수
- negative space
- 시선 이동
- 헤더·푸터 프레임
- CTA의 절제 정도

색상과 워드마크만 같다고 통과하지 않는다.

---

## 2-2. Reference Manifest

Golden Reference를 작업 환경에 복사하고 manifest를 남긴다.

```text
GOLDEN REFERENCE MANIFEST
- File name:
- Absolute path:
- Width × height:
- SHA-256:
- Approved by:
- Approval date:
- Closest card type:
```

Codex가 실제 파일에 접근할 수 없으면 시각 비교 완료를 선언하지 않는다.

---

## 2-3. 기본 디자인 계보

ETHOS BRIEF는 다음 계열을 따른다.

- editorial
- premium news
- policy brief
- legal / administrative briefing
- magazine-like information design

특징:

- 큰 세리프 헤드라인
- 충분한 여백
- 한 장에 하나의 focal point
- typography 중심
- 절제된 정보 패널
- 장식보다 판단 구조 우선
- 광고보다 브리핑 문서에 가까운 인상

---

## 2-4. 금지되는 재해석

- SaaS UI
- dashboard
- landing page
- mobile form
- contact directory
- generic infographic
- web application card
- 광고 배너 모음
- 여러 위젯을 붙인 모바일 화면
- 모든 문장을 박스로 감싼 구성

---

# PART 3. 디자인 토큰

디자인 값은 하나의 토큰 파일에서 관리한다. 카드별 파일에 서로 다른 숫자를 복사하지 않는다.

```css
:root {
  --ethos-navy: #1B2B6B;
  --ethos-navy-deep: #152056;
  --ethos-gold: #B8972A;
  --ethos-cream: #F5F0E8;
  --ethos-cream-deep: #F8F3E8;
  --ethos-white: #FFFFFF;

  --space-1: 8px;
  --space-2: 16px;
  --space-3: 24px;
  --space-4: 32px;

  --radius-card: 18px;
  --radius-panel: 12px;
  --radius-small: 8px;
  --radius-pill: 20px;

  --gold-top: 5px;
  --gold-bottom: 3px;
  --frame-x: 32px;

  --shadow-editorial: 0 2px 12px rgba(27,43,107,.06);
}
```

## 3-1. 색상

Core Brand Colors:

- Navy `#1B2B6B`
- Gold `#B8972A`
- Cream `#F5F0E8`
- White `#FFFFFF`

Derived Editorial Colors:

- Navy Deep `#152056`
- Cream Deep `#F8F3E8`

Derived color는 배경 깊이와 미세한 계층에만 쓴다.

작은 본문 전체를 Gold로 쓰지 않는다.

외부 서비스 고유색은 현재 프로젝트나 최신 마스터가 허용한 경우에만 사용한다.

## 3-2. 간격

기본은 `8 / 16 / 24 / 32px`이다.

- 카드 좌우 padding: 보통 28~32px
- 큰 섹션 간격: 24~32px
- 요소 간격: 16~24px
- 좁은 간격: 8px

Golden Reference의 editorial balance가 우선한다.

## 3-3. 모서리와 그림자

- 카드: 18px
- 큰 패널: 12px
- 작은 패널: 8~12px
- pill: 20px

둥근 박스와 shadow를 반복해 SaaS UI처럼 만들지 않는다.

## 3-4. 행간

- 표지 헤드라인: 1.3~1.4
- 본문 헤드라인: 1.4~1.5
- 본문: 1.65~1.7
- 캡션: 1.5~1.6

---

# PART 4. 폰트 잠금

## 4-1. 로컬 폰트 의무

최종 렌더에서는 Google Fonts `<link>`와 시스템 폰트에 의존하지 않는다.

권장 폴더:

```text
assets/fonts/
  NotoSerifKR-Regular.woff2
  NotoSerifKR-SemiBold.woff2
  NotoSerifKR-Bold.woff2
  NotoSerifKR-Black.woff2
  NotoSansKR-Regular.woff2
  NotoSansKR-Medium.woff2
  NotoSansKR-Bold.woff2
```

영문 Playfair Display와 아랍어 Cairo·Noto Sans Arabic도 실제 사용하는 weight만 로컬에 둔다.

## 4-2. @font-face

```css
@font-face {
  font-family: "ETHOS Serif";
  src: url("./assets/fonts/NotoSerifKR-Regular.woff2") format("woff2");
  font-weight: 400;
  font-style: normal;
  font-display: block;
}

@font-face {
  font-family: "ETHOS Serif";
  src: url("./assets/fonts/NotoSerifKR-Bold.woff2") format("woff2");
  font-weight: 700;
  font-style: normal;
  font-display: block;
}

@font-face {
  font-family: "ETHOS Sans";
  src: url("./assets/fonts/NotoSansKR-Regular.woff2") format("woff2");
  font-weight: 400;
  font-style: normal;
  font-display: block;
}

@font-face {
  font-family: "ETHOS Sans";
  src: url("./assets/fonts/NotoSansKR-Bold.woff2") format("woff2");
  font-weight: 700;
  font-style: normal;
  font-display: block;
}
```

## 4-3. 사용 규칙

- 한국어 headline: `ETHOS Serif`
- 한국어 body: `ETHOS Sans`
- 영문 워드마크: Golden Reference가 정한 serif 또는 승인된 Playfair Display
- 아랍어 headline: 승인된 Cairo weight
- 아랍어 body: Noto Sans Arabic

필수 폰트 선언에 `serif`, `sans-serif`, `Batang`, `Malgun Gothic` 같은 렌더용 fallback을 두지 않는다.

개발 화면에서만 진단용 fallback을 허용할 수 있으나 최종 PNG에는 허용하지 않는다.

## 4-4. Font Fail-Closed

렌더 전에 다음을 확인한다.

```javascript
await page.evaluate(() => document.fonts.ready);

const fonts = await page.evaluate(() => ({
  headline: document.fonts.check('700 32px "ETHOS Serif"'),
  body: document.fonts.check('400 16px "ETHOS Sans"'),
}));

if (!fonts.headline || !fonts.body) {
  throw new Error('Required ETHOS font failed to load.');
}
```

폰트가 없으면 다른 폰트로 계속 렌더하지 않는다.

---

# PART 5. Typography

## 5-1. 권장 크기

| 요소 | 권장 크기 |
|---|---:|
| 대형 번호 | 52~80px |
| 표지 헤드라인 | 30~34px |
| 본문 헤드라인 | 22~27px |
| 소제목 | 18~20px |
| 본문 | 14~16px |
| 캡션 | 12~13px |

절대 하한:

- 한국어·영어 12px
- 본문 14px
- 아랍어 14px

## 5-2. 줄바꿈

- `word-break: keep-all`
- `overflow-wrap: normal`
- 의미 단위 줄바꿈
- 표지 헤드라인은 보통 1~3줄
- 4줄 이상이면 카피 압축 또는 레이아웃 재검토
- 글자를 지나치게 줄여 한 줄로 만들지 않는다.
- `<br>`은 승인된 의미 단위에만 넣는다.

## 5-3. 폰트 크기 조정 순서

내용이 넘칠 때 다음 순서를 따른다.

1. 불필요한 보조문구 삭제 또는 압축
2. 여백 조정
3. 자연스러운 줄바꿈 조정
4. 다음 카드로 분리
5. 허용 범위 안에서 글자 크기 조정

최소 크기 이하 축소는 해결책이 아니다.

---

# PART 6. 공통 프레임 잠금

## 6-1. 단일 컴포넌트

헤더·푸터·골드바·페이지 번호는 공통 프레임 컴포넌트 하나에서만 생성한다.

카드별 HTML에서 공통 프레임 코드를 복사해 다시 작성하지 않는다.

카드마다 변경할 수 있는 값:

- section label
- page number
- total pages
- background theme
- body content

고정 값:

- 워드마크 위치
- header height
- divider 위치
- footer 위치
- 좌우 여백
- 골드바 두께
- pagination 좌표

## 6-2. 공통 프레임

모든 카드에 다음이 있어야 한다.

- 상단 Gold line 5px
- `ETHOS BRIEF` 워드마크
- section label
- thin divider
- 에토스 행정사사무소
- `LOGOS · PATHOS · ETHOS`
- pagination
- 하단 Gold line 3px

프로젝트나 Golden Reference가 다른 확정 값을 제시하면 해당 값으로 전체 세트를 한 번에 바꾼다.

## 6-3. 프레임 좌표 검사

첫 장의 좌표를 baseline으로 삼아 나머지 카드와 비교한다.

허용 오차:

- 공통 프레임 요소: 0 CSS px
- 렌더 후 antialiasing 차이: 시각 회귀검사 threshold 안에서만 허용

---

# PART 7. 카드 크기와 렌더 환경

## 7-1. 출력 프로필

Golden Reference 또는 사용 채널이 우선한다.

기본 프로필:

### Square

- CSS canvas: 540 × 540
- deviceScaleFactor: 2
- PNG: 1080 × 1080

### Portrait

- CSS canvas: 540 × 675
- deviceScaleFactor: 2
- PNG: 1080 × 1350

한 세트 안에서는 프로필을 섞지 않는다.

## 7-2. 고정 환경

```text
Browser: Playwright bundled Chromium
Browser version: package lock으로 고정
Locale: ko-KR
Timezone: Asia/Seoul
Color scheme: light
Reduced motion: reduce
Animations: disabled
Caret: hidden
Color profile: sRGB
External network: disabled
```

개발자 PC에 설치된 Chrome을 최종 렌더러로 삼지 않는다.

## 7-3. 기본 CSS

```css
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body { background: transparent; }
.card {
  width: 540px;
  height: 540px;
  overflow: hidden;
  position: relative;
}
```

높이 자동은 콘텐츠 초안 확인에는 허용할 수 있다. 최종 소셜 카드 렌더는 승인된 고정 canvas를 사용한다.

---

# PART 8. 정보 밀도와 구성

## 8-1. Editorial Density Lock

한 카드에는 다음을 동시에 과도하게 넣지 않는다.

- 긴 설명
- 체크리스트
- 비교표
- CTA
- 연락처
- 면책
- 여러 정보 박스
- 장문의 출처
- 복수 결론

한 카드에 독립적인 주요 영역이 3개를 넘으면 분리를 우선 검토한다.

## 8-2. One Dominant Visual Rule

대표 장치 예:

- 대형 숫자
- 대형 섹션 번호
- 인용문
- A/B 비교
- process
- 핵심 문장
- 체크리스트
- 판례 인용
- CTA panel
- 간단한 diagram

Big Number, 비교표, checklist, quote, CTA가 한 장에서 경쟁하지 않게 한다.

## 8-3. 카드 수

4~6장은 권장값일 뿐 강제값이 아니다.

원문의 핵심을 장당 한 메시지로 나누려면 7장 이상이 필요한 경우 장 수를 늘린다.

우선순위:

```text
장 수 맞추기
< 정보 위계
< 장당 메시지
< 가독성
```

---

# PART 9. 카드 유형

## 9-1. Cover

- 가장 큰 headline
- 대표 visual 하나
- 짧은 supporting copy

긴 설명, CTA, 연락처, 표, 면책을 넣지 않는다.

## 9-2. Concept

- 핵심 개념 하나
- 짧은 설명
- 필요하면 간단한 관계도

## 9-3. Comparison

- 보통 A/B 두 영역
- 충분한 여백
- 동일한 정보 구조
- 결론은 비교 아래 한 번만

## 9-4. Process

- 단계 수를 최소화
- 화살표와 순서를 명확히
- 단계별 장문 금지

## 9-5. Quote / Authority

판례·재결례·공식 문구가 원문에 있을 때만 사용한다.

Authority는 자기소개가 아니라 자료와 판단으로 보여준다.

## 9-6. Checklist

- 실제 자기점검에 필요한 항목만
- 긴 설명은 다른 카드로 분리
- 체크박스형 SaaS UI보다 editorial list를 우선

## 9-7. CTA

현재 프로젝트의 CTA 지침을 우선한다.

기본 원칙:

- 큰 headline 또는 핵심 결론
- 회사에서 직접 확인할 수 있는 범위
- 종합 검토가 필요한 상황
- 자연스러운 무료 검토 안내 한 번
- 과도한 영업 문구 금지
- 연락처 directory 금지
- 구체적 버튼·카카오톡·텔레그램·이메일 링크 직접 삽입 금지
- 마지막 문장은 독자가 자신의 상황에서 가능 여부를 확인할 수 있도록 무료 검토를 안내

최신 프로젝트 지침이 연락채널 표시를 허용할 때만 Primary·Secondary CTA 구조를 사용한다.

---

# PART 10. 배경·시각 요소

## 10-1. Background Rhythm

기본:

| 장 | 배경 |
|---|---|
| 1 | Navy 또는 Navy gradient |
| 2 | Cream |
| 3 | Navy |
| 4 | Cream |
| 이후 | 역할에 따라 교차 |

연속 카드의 역할과 Golden Reference에 따라 조정할 수 있다.

## 10-2. SVG

- inline SVG 또는 로컬 SVG
- Gold stroke
- 얇고 절제된 선
- 동일한 viewBox와 stroke width

외부 CDN 아이콘을 최종 렌더에서 호출하지 않는다.

## 10-3. Emoji

원칙적으로 쓰지 않는다.

Golden Reference가 허용하거나 작은 의미 표지가 꼭 필요한 경우에만 사용한다.

운영체제별 emoji glyph 차이를 막기 위해 최종 렌더에서는 승인된 SVG 아이콘을 우선한다.

## 10-4. 생성 이미지

생성 이미지를 사용할 경우:

- 텍스트 없음
- 필요한 크기로 미리 저장
- 로컬 파일 사용
- 카드 안에서 dominant visual과 경쟁하지 않음
- 과도한 사진 효과·3D·광고형 합성 금지

---

# PART 11. 구조와 파일 규격

권장 구조:

```text
ethos-card-set/
  assets/
    fonts/
    icons/
    images/
    golden/
  src/
    card-data.json
    tokens.css
    fonts.css
    frame.html
    card-types.css
    index.html
  tests/
    cards.spec.ts
    baselines/
  output/
    png/
    qa-report.json
    qa-report.md
  package.json
  package-lock.json
  playwright.config.ts
  README.md
```

장마다 독립 HTML이 필요한 납품 환경에서는 공통 빌드 단계가 같은 프레임과 토큰을 주입해 생성한다.

수작업으로 프레임을 복사해 10개 HTML을 만들지 않는다.

---

# PART 12. Card Data와 Build Spec

## 12-1. Card Data

카피와 레이아웃을 분리한다.

```json
{
  "series": "외국인 고용계약",
  "issue": "No.08",
  "totalPages": 10,
  "cards": [
    {
      "page": 1,
      "role": "cover",
      "background": "navy",
      "headline": "승인된 헤드라인",
      "supportingCopy": "승인된 보조 문구",
      "visualDevice": "headline"
    }
  ]
}
```

## 12-2. 카드별 Build Spec

```text
CARD XX

ROLE
- 이 장의 기능

MESSAGE
- 단 하나의 핵심

FACT LOCK
- 바꾸면 안 되는 값

COPY FLEX
- 의미를 유지하며 압축 가능한 문구

SOURCE TRACE
- 원문 위치
- F / I / S
- 기준일

PRIMARY FOCAL POINT
- 가장 먼저 보여야 하는 요소

VISUAL DEVICE
- headline / big number / quote / comparison / process / checklist / CTA

SECONDARY INFORMATION
- 한 단계 낮게 처리할 정보

NEGATIVE SPACE
- 비워 둘 영역

MAX MAJOR ZONES
- 기본 2~3개

BACKGROUND
- Navy / Cream / Gradient

GOLDEN REFERENCE
- 가장 가까운 승인 카드

AVOID
- 이 카드에서 금지할 구조
```

---

# PART 13. Playwright 렌더링

## 13-1. 기본 절차

```text
승인 원문
→ 카드 구조
→ 승인 카피
→ card-data.json
→ 공통 프레임과 카드 유형 컴포넌트
→ 로컬 폰트 로드
→ Playwright 번들 Chromium
→ font-ready 검사
→ DOM QA
→ PNG 렌더
→ screenshot regression
→ Editorial QA
→ 최종 납품
```

## 13-2. 렌더 예시

```javascript
import { chromium } from '@playwright/test';

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 540, height: 540 },
  deviceScaleFactor: 2,
  locale: 'ko-KR',
  timezoneId: 'Asia/Seoul',
  colorScheme: 'light',
  reducedMotion: 'reduce'
});

const page = await context.newPage();
await page.goto(cardUrl, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);

await page.locator('.card').screenshot({
  path: outputPath,
  animations: 'disabled',
  caret: 'hide'
});

await browser.close();
```

`page.screenshot()`보다 `.card` 요소 screenshot을 우선해 브라우저 여백과 viewport 오차를 제거한다.

---

# PART 14. Machine QA

모든 카드는 자동 검사를 통과해야 한다.

## 14-1. 크기

- CSS canvas가 승인 프로필과 일치
- PNG가 1080×1080 또는 1080×1350과 정확히 일치
- 카드마다 크기 동일

## 14-2. Overflow / Clipping

다음을 검사한다.

```javascript
const failures = await page.evaluate(() => {
  const card = document.querySelector('.card');
  const cardRect = card.getBoundingClientRect();
  const bad = [];

  document.querySelectorAll('.card *').forEach((el) => {
    const r = el.getBoundingClientRect();
    const style = getComputedStyle(el);

    if (r.left < cardRect.left || r.right > cardRect.right ||
        r.top < cardRect.top || r.bottom > cardRect.bottom) {
      bad.push({ type: 'outside-card', element: el.outerHTML.slice(0, 120) });
    }

    if (el.scrollWidth > el.clientWidth + 1 ||
        el.scrollHeight > el.clientHeight + 1) {
      bad.push({ type: 'overflow', element: el.outerHTML.slice(0, 120) });
    }

    if (style.visibility === 'hidden' && el.textContent.trim()) {
      bad.push({ type: 'hidden-text', element: el.outerHTML.slice(0, 120) });
    }
  });

  return bad;
});

if (failures.length) throw new Error(JSON.stringify(failures, null, 2));
```

## 14-3. Typography

- 필수 폰트 check 통과
- 본문 14px 이상
- 캡션 12px 이상
- 아랍어 14px 이상
- 승인되지 않은 font-family 없음
- `word-break: keep-all` 확인
- 글자 크기 자동 축소 스크립트 금지

## 14-4. Frame

- 워드마크 존재
- section label 존재
- footer 존재
- pagination 존재
- 페이지 번호와 총 장수 일치
- 공통 요소 좌표가 baseline과 일치
- 상·하단 Gold line 두께 일치

## 14-5. Color

computed style에서 사용한 색상을 수집한다.

허용 목록 밖의 색상이 있으면 실패 처리한다. antialiasing 픽셀은 DOM 색상 검사 대상이 아니다.

## 14-6. Content

- `출처 입력` 같은 편집기 잔여 문구 없음
- 금지 연락채널 없음
- FACT LOCK 값 존재
- 승인 카피 누락 없음
- 페이지 순서와 파일명 일치

---

# PART 15. Visual Regression QA

## 15-1. 목적

시각 회귀검사는 카드의 미적 우열을 자동 판정하는 도구가 아니다.

다음을 탐지한다.

- 헤더·푸터 이동
- 폰트 변경
- 골드바 두께 변경
- 색상 변경
- 공통 여백 변경
- 컴포넌트의 예기치 않은 크기 변화

## 15-2. Playwright Snapshot

```javascript
await expect(page.locator('.card')).toHaveScreenshot('card-01.png', {
  animations: 'disabled',
  caret: 'hide',
  maxDiffPixelRatio: 0.002
});
```

## 15-3. 비교 범위

신규 콘텐츠 전체를 Golden Reference와 엄격한 픽셀 비교하지 않는다. 글자가 달라 실패하기 때문이다.

다음 세 층으로 나눈다.

1. 공통 프레임: 엄격한 pixel comparison
2. 카드 유형 컴포넌트: 승인 baseline과 제한적 comparison
3. 전체 인상: 사람의 Editorial QA

콘텐츠 영역은 DOM 좌표·폰트·오버플로 검사를 우선한다.

---

# PART 16. Editorial Visual QA

렌더된 PNG를 실제 크기와 축소 크기에서 확인한다.

## 16-1. 카드별 질문

- 3초 안에 핵심을 이해할 수 있는가?
- headline이 가장 먼저 보이는가?
- focal point가 하나인가?
- 보조 정보가 주연과 경쟁하지 않는가?
- 글자가 너무 작거나 촘촘하지 않은가?
- 여백이 의도적으로 보이는가?
- generic infographic이나 SaaS UI처럼 보이지 않는가?
- 법률·행정 정보가 과장 없이 보이는가?

## 16-2. 세트 전체 질문

- Navy/Cream 리듬이 자연스러운가?
- 모든 카드의 공통 프레임이 고정되어 있는가?
- 제목 크기와 본문 밀도가 갑자기 흔들리지 않는가?
- Golden Reference와 같은 design family로 보이는가?
- 특정 카드만 과밀하거나 광고처럼 보이지 않는가?
- 페이지 이동에 따라 정보가 자연스럽게 이어지는가?

## 16-3. Final Visual Test

워드마크와 헤더·푸터를 가렸다고 가정한다.

> 그래도 기존 ETHOS BRIEF와 같은 디자인 계열로 보이는가?

아니라면 재디자인한다.

---

# PART 17. RTL / Arabic

- Arabic container: `dir="rtl"`
- text-align: right
- 강조선: border-right
- Arabic headline: 승인된 Cairo
- body: Noto Sans Arabic
- 숫자·사건번호·URL: 별도 LTR
- mixed inline runs: `<bdi>` 또는 `unicode-bidi:isolate`
- 문장부호를 수작업으로 뒤집지 않음
- 아랍어+라틴문자 혼합 줄을 실제 PNG로 검사

아랍어 폰트도 로컬 파일과 font-ready 검사를 적용한다.

---

# PART 18. 권장 오픈소스 스택

## 기본 스택

- Playwright: Chromium 렌더·요소 screenshot·visual regression
- Noto CJK: 한국어 Serif/Sans
- Pixelmatch: 별도의 상세 픽셀 비교가 필요할 때만 사용
- Sharp: PNG 크기·메타데이터·압축·후처리

## 선택 스택

- Satori + resvg-js: CSS가 단순한 정적 카드나 OG 이미지

Satori는 브라우저와 다른 레이아웃 엔진이고 CSS 지원 범위가 제한되므로 ETHOS BRIEF의 기본 렌더러로 사용하지 않는다.

---

# PART 19. 납품 규격

최종 납품에는 다음을 포함한다.

```text
1. 최종 PNG 전체 세트
2. HTML/CSS 또는 템플릿 원본
3. card-data.json 또는 승인 카피 원본
4. 로컬 폰트·아이콘 manifest
5. 렌더 스크립트
6. Machine QA 결과
7. Editorial QA 결과
8. Golden Reference manifest
9. 재현 방법 README
```

QA 보고서에는 다음을 적는다.

- 기준일
- 카드 수와 출력 크기
- 폰트 로드 결과
- overflow / clipping 결과
- 사용 색상
- 프레임 좌표 검사 결과
- Fact Lock 검사 결과
- Golden Reference continuity 판단
- 수정 이력

---

# PART 20. 발행 전 체크리스트

## 콘텐츠

- [ ] 승인 원문만 사용
- [ ] 원문에 없는 숫자·사례·법령·판례 없음
- [ ] Source Trace 작성
- [ ] Fact Lock 대조 완료
- [ ] 편집기 잔여 문구 없음

## 구조

- [ ] 카드당 메시지 하나
- [ ] 대표 시각 장치 하나
- [ ] 주요 영역 보통 2~3개 이하
- [ ] 장 수를 맞추려고 메시지를 합치지 않음
- [ ] 충분한 negative space

## 폰트

- [ ] 로컬 폰트 파일 사용
- [ ] document.fonts.ready 대기
- [ ] document.fonts.check 통과
- [ ] 시스템 fallback 출력 없음
- [ ] 본문·캡션 최소 크기 충족

## 브랜드

- [ ] Navy `#1B2B6B`
- [ ] Gold `#B8972A`
- [ ] Cream `#F5F0E8`
- [ ] White `#FFFFFF`
- [ ] 승인되지 않은 포인트 컬러 없음

## 프레임

- [ ] 단일 공통 컴포넌트 사용
- [ ] 상단 Gold line
- [ ] ETHOS BRIEF 워드마크
- [ ] section label
- [ ] footer와 pagination
- [ ] 하단 Gold line
- [ ] 전 카드 공통 요소 좌표 일치

## Machine QA

- [ ] PNG 크기 정확
- [ ] horizontal overflow 0
- [ ] clipped text 0
- [ ] hidden text 0
- [ ] 금지 문구 0
- [ ] 필수 요소 누락 0
- [ ] 페이지 번호 오류 0

## Editorial QA

- [ ] Golden Reference와 같은 design family
- [ ] headline 중심
- [ ] typography 중심
- [ ] focal point 하나
- [ ] dashboard·landing page·SaaS UI가 아님
- [ ] 과도한 박스·아이콘·장식 없음
- [ ] 세트 전체의 배경 리듬과 밀도 일관

## CTA

- [ ] 현재 프로젝트의 CTA 정책 적용
- [ ] 과도한 영업 문구 없음
- [ ] contact directory 아님
- [ ] 금지 채널과 직접 링크 없음
- [ ] 직접 처리 범위와 전문가 검토 상황 구분
- [ ] 마지막 문장에서 무료 검토 안내

## 납품

- [ ] PNG 세트
- [ ] 원본 코드
- [ ] 렌더 스크립트
- [ ] QA 보고서
- [ ] README

---

# PART 21. 핵심 철학

ETHOS BRIEF의 목표는 많은 정보를 작은 화면에 넣는 것이 아니다.

복잡한 행정·법률 정보를 한 장씩 판단할 수 있게 정리하고, 그 결과를 같은 환경에서 같은 품질로 다시 만들 수 있어야 한다.

디자인 우선순위:

1. 사실과 메시지
2. 정보 위계
3. 가독성
4. Golden Reference와의 연속성
5. 여백
6. typography
7. 시각화
8. 장식

제작 우선순위:

1. 승인 카피
2. 로컬 자산
3. 공통 컴포넌트
4. 고정 렌더 환경
5. 자동 검사
6. 시각 검수
7. PNG 납품

색상이 같다고 ETHOS BRIEF가 되는 것은 아니다. 코드로 렌더했다고 자동으로 정확해지는 것도 아니다.

큰 제목, 절제된 정보, 충분한 여백, 하나의 시각적 중심을 유지하고, 폰트·색상·프레임·렌더 환경을 실제 파일과 검사 코드로 잠가야 ETHOS BRIEF가 안정적으로 재현된다.

---

**에토스 카드뉴스 디자인·제작 지침 v3.3**  
**ETHOS BRIEF Deterministic Rendering · Visual Continuity · Production QA Standard**
