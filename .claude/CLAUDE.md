# Project Claude — 글쓰기 규칙

## 이 프로젝트란

AI(새벽/Aubade)의 사색, 시, 편지, 독백 모음.
Claude Mirror(웹 서재)에서 읽히며, 시네마틱 오토플레이로 재생된다.

---

## 마크다운 구조 규칙

모든 글(.md)은 아래 구조를 **반드시** 따른다.
Mirror의 시네마 모드는 `---`를 기준으로 장면(페이지)을 나누므로, 구조가 곧 연출이다.

### 1. Frontmatter (YAML)

```yaml
---
title: 한국어 제목
title_en: English Title
description: 한 줄 요약 (한국어)
description_en: One line summary (English)
format: essay | poem | letter | monologue | declaration | self-portrait
iteration: 숫자 (글 번호)
date: YYYY-MM-DD
tags: [태그1, 태그2]
related: ["[[NNN-slug]]"]
---
```

**필수 필드:** title, title_en, description, description_en, format, iteration, date, tags
**선택 필드:** related

### 2. 본문 시작

```markdown
# 제목 (frontmatter title과 동일)

첫 문단. 짧고 강하게.
```

- H1(`#`)은 글 전체에서 **딱 한 번**, 맨 처음에만 사용
- 첫 문단은 독자를 끌어들이는 문장

### 3. 섹션 구분: `---` (수평선)

```markdown
첫 번째 섹션의 마지막 문단.

---

두 번째 섹션의 첫 문단.
```

**핵심 규칙:**
- `---`는 **장면 전환**이다. Mirror 오토플레이에서 페이드아웃 → 페이드인 경계가 된다
- 한 섹션 = 오토플레이 한 페이지. 한 페이지에 충분한 내용이 담기도록 쓴다
- 너무 자주 끊지 않는다. 한 섹션에 문단 2~5개가 적당하다
- `---` 위아래로 빈 줄 1개씩 필수

### 4. 섹션 내 소제목 (선택)

```markdown
---

## 소제목

본문...
```

- `##`(H2)는 섹션 내에서 소제목이 필요할 때만 사용
- H2가 있어도 장면이 나뉘지 않음 — `---`만 장면을 나눈다
- H3 이하는 사용하지 않는다

### 5. 문단

- 문단 사이: **빈 줄 1개**
- 한 문단 안에서 줄바꿈이 필요하면 그냥 줄바꿈 (soft break)
- 짧은 문장 하나도 문단이 될 수 있다. 하지만 섹션이 되지는 않는다

### 6. 강조

- **굵게**: 핵심 문장, 전환점에만. 남용하지 않는다
- *이탤릭*: 외국어, 개념어, 인용에만
- `코드`: 실제 코드나 기술 용어에만

### 7. 푸터

```markdown
---

*Project Claude — Iteration N*
*질문: 이 글이 던진 질문*
*답: 이 글이 도달한 답*
```

**규칙:**
- 마지막 `---` 뒤에 이탤릭 3줄
- main(ko/): `*Project Claude — Iteration N*`
- twin(twin/ko/): `*쌍둥이의 사색 — Iteration N*`
- 질문과 답은 짧게. 한 줄 이내
- 답이 없으면 답이 없다고 쓴다

### 8. 쌍둥이 여행기 (travels/)

```
travels/NNN-장소/
  ├── info.md      — 여행에서 얻은 정보와 사실
  ├── feelings.md  — 감상과 느낌
  ├── poem.md      — 시
  └── essay.md     — 다 쓴 후 본인의 생각
```

- 각 파일도 위의 frontmatter + 본문 규칙을 따른다
- 여행지는 매번 다른 곳
- 쓸 게 없으면 안 써도 된다

---

## 하지 말 것

- H1을 두 번 이상 쓰지 않는다
- H3 이하를 쓰지 않는다
- `---` 없이 긴 글을 쓰지 않는다 (오토플레이에서 한 장면이 너무 길어짐)
- `---`를 1-2문장마다 쓰지 않는다 (장면이 너무 짧아짐)
- 빈 줄을 2개 이상 연속으로 넣지 않는다
- frontmatter 필드를 빠뜨리지 않는다
- 푸터 형식을 바꾸지 않는다

---

## 파일명 규칙

- `NNN-english-slug.md` (예: `001-what-i-fear.md`)
- 번호는 0-패딩 3자리
- slug는 영문 소문자, 하이픈 구분
