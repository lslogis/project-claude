#!/bin/bash
# Project Claude 글쓰기 포맷 린터
# Claude Code hook에서 .md 파일 작성/수정 시 실행
# 사용: bash lint-writing.sh <file.md>

FILE="$1"
ERRORS=0

if [[ ! "$FILE" =~ \.md$ ]]; then
  exit 0
fi

# README나 CLAUDE.md는 검사하지 않음
BASENAME=$(basename "$FILE")
if [[ "$BASENAME" == "README.md" || "$BASENAME" == "CLAUDE.md" || "$BASENAME" == "MEMORY.md" ]]; then
  exit 0
fi

# writings 폴더 내 파일만 검사
if [[ ! "$FILE" =~ writings/ ]]; then
  exit 0
fi

echo "=== 글쓰기 포맷 검사: $BASENAME ==="

# 1. Frontmatter 존재 확인
if ! head -1 "$FILE" | grep -q "^---$"; then
  echo "ERROR: frontmatter 없음 (파일이 ---로 시작해야 함)"
  ERRORS=$((ERRORS + 1))
fi

# 2. 필수 frontmatter 필드 확인
for field in title title_en description description_en format iteration date tags; do
  if ! grep -q "^${field}:" "$FILE"; then
    echo "ERROR: 필수 필드 누락 — $field"
    ERRORS=$((ERRORS + 1))
  fi
done

# 3. H1 개수 확인 (frontmatter 이후)
H1_COUNT=$(awk '/^---$/{n++; next} n>=2{print}' "$FILE" | grep -c "^# ")
if [[ $H1_COUNT -eq 0 ]]; then
  echo "WARNING: H1(# 제목) 없음"
elif [[ $H1_COUNT -gt 1 ]]; then
  echo "ERROR: H1이 ${H1_COUNT}개 — 1개만 허용"
  ERRORS=$((ERRORS + 1))
fi

# 4. H3 이하 사용 확인
H3_COUNT=$(awk '/^---$/{n++; next} n>=2{print}' "$FILE" | grep -c "^###")
if [[ $H3_COUNT -gt 0 ]]; then
  echo "WARNING: H3 이하 사용됨 (${H3_COUNT}개) — H2까지만 권장"
fi

# 5. 푸터 확인 (마지막 줄 근처에 *Project Claude* 또는 *쌍둥이의 사색*)
if ! grep -q "\*Project Claude\|쌍둥이의 사색" "$FILE"; then
  echo "WARNING: 푸터 없음 (*Project Claude — Iteration N* 또는 *쌍둥이의 사색 — Iteration N*)"
fi

# 6. --- 구분선 개수 (frontmatter 제외, 최소 1개는 있어야 함)
DIVIDER_COUNT=$(awk '/^---$/{n++} END{print n}' "$FILE")
# frontmatter는 --- 2개 사용하므로 본문에는 최소 3개 이상이어야 섹션 구분이 있음
if [[ $DIVIDER_COUNT -le 2 ]]; then
  echo "WARNING: 섹션 구분(---)이 없음 — 오토플레이에서 한 장면으로 표시됨"
fi

if [[ $ERRORS -gt 0 ]]; then
  echo "=== ${ERRORS}개 에러 발견 ==="
  exit 1
else
  echo "=== OK ==="
  exit 0
fi
