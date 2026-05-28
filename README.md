# MagicSquare_33

4×4 **마방진(Magic Square)** 을 다루는 학습·실습 프로젝트입니다.  
현재 단계는 **문제 정의(STEP 1~5)** 이며, 설계·구현은 아직 시작하지 않았습니다.

---

## 프로젝트 목적

| 목적 | 설명 |
|------|------|
| **도메인** | 4×4 격자에 1~16을 한 번씩 배치하고, 행·열·대각선의 합이 모두 같은지 다룸 |
| **방법** | 문제 인식 → Why 분석 → 불변 조건·계약 정리 → (예정) TDD 기반 설계·구현 |
| **맥락** | SW 아키텍트 관점의 규칙 명시화, 검증·생성 분리, 테스트 가능한 요구 정의 연습 |

---

## 현재 상태

| 항목 | 상태 |
|------|------|
| 문제 정의 (STEP 1~5) | ✅ 완료 |
| 수용 기준 (STEP 6) | ⏳ 예정 |
| 설계·구현 | ⏳ 미착수 |

---

## 문제 정의 요약

### 표면 정의 (지양)

> 4×4 칸에 숫자를 넣어 행·열·대각선 합이 같은 마방진을 **완성하는 프로그램**을 만든다.

- 산출물(16칸)만 강조하면 **규칙·검증·설명**이 빠지기 쉽습니다.

### 진짜 정의 (목표)

> 4×4 **마방진 규칙을 명시**하고, 임의의 배치가 규칙을 만족하는지 **일관되게 판정**하며, 규칙을 만족하는 완전한 배치는 **판정기와 동일한 기준으로 재확인**할 수 있게 한다.

**성공의 핵심**

- 규칙을 설명할 수 있다.
- 맞는 배치와 틀린 배치를 구분할 수 있다.
- 제공한 완전한 배치는 판정기로 다시 확인했을 때 일치한다.

---

## Why 요약

```
관찰     → 의도는 있으나 규칙·IO·역할은 아직 열림
Why #1   → “완성”이 아니라 규칙 성립 확인 + 설명 가능성
Why #2   → 반복 실행, 검증 자동화, 오류 방지, 규칙 기반 사고
Why #3   → TDD로 계약·불변식·통제를 먼저 고정 (생성 ⊂ 검증)
```

| 단계 | 한 줄 |
|------|--------|
| **Why #1** | 규칙을 만족하는 배치가 존재함을 **검증·설명**할 수 있어야 한다 |
| **Why #2** | 손계산 대신 프로그램으로 **반복·판정·명시적 규칙**을 다룬다 |
| **Why #3** | 테스트 가능한 **입력·출력·판정**을 먼저 고정한다 |

---

## 핵심 Invariant (4×4 표준 마방진)

| ID | 불변 조건 |
|----|-----------|
| I-1 | 격자는 4×4 |
| I-2 | 완전 배치 시 모든 칸에 값 존재 |
| I-3 | 각 값은 1 이상 16 이하 |
| I-4 | 1~16이 각각 정확히 한 번 |
| I-5 ~ I-7 | 행·열·주대각·부대각의 합이 모두 동일 |
| I-8 | I-3·I-4 성립 시 공통 합 = **34** |
| I-9 | 동일 배치·규칙 → 동일 판정 (결정적) |
| I-10 | 완전 배치 제공 ⟹ 위 조건을 판정기로 확인 가능 |
| I-11 | (선택) 부분 배치: 미완성 vs 이미 위반 구분 |

**신뢰 원칙:** “규칙에 맞는 배치를 제공했다”는 주장은 **반드시 판정기 통과**와 같아야 합니다.

---

## 훈련하려는 사고 능력

- **규칙 명시화** — 직관을 검사 가능한 조건으로 표현
- **불변식 분해** — 구조 / 집합 / 합 / 메타(신뢰) 계층
- **계약·경계** — 판정 · 배치 획득 · 표현의 책임 분리
- **증거 기반 신뢰** — “맞을 것 같다”가 아닌 판정 결과로 성공 정의
- **테스트 주도적 문제 정의** — 기능 목록보다 만족/위반 예시·출력 의미 우선
- **범위 통제** — 현재는 4×4에 집중

---

## 프로젝트 구조

```
MagicSquare_33/
├── README.md
├── .cursor/
│   └── rules/                    ← Cursor Project Rules (.mdc)
├── .cursorrules                  ← (deprecated) rules 이전 안내만 유지
├── Report/
│   ├── 01.문제정의_보고서.md
│   └── 02.DualTrack_CleanArch_TDD_설계.md
├── Prompt/
├── src/magicsquare/              ← ECB 레이어 (boundary / control / entity)
├── tests/                        ← Dual-Track 테스트
└── pyproject.toml
```

| 문서 | 설명 |
|------|------|
| [Report/01.문제정의_보고서.md](Report/01.문제정의_보고서.md) | 관찰, Why #1~#3, 진짜 문제 정의, Invariant 전체 |
| [Report/02.DualTrack_CleanArch_TDD_설계.md](Report/02.DualTrack_CleanArch_TDD_설계.md) | Dual-Track TDD, ECB 설계, Test-ID·계약 |
| [Prompt/01.cursor_4x4_magic_square_problem_definit.md](Prompt/01.cursor_4x4_magic_square_problem_definit.md) | Cursor에서 진행한 문제 정의 대화 원문 |

---

## Cursor AI 규칙 (Project Rules)

AI 에이전트·채팅에 적용되는 프로젝트 규칙은 **루트 `.cursorrules`가 아니라** [`.cursor/rules/`](.cursor/rules/) 아래 `.mdc` 파일로 관리합니다.  
(레거시 `.cursorrules`는 이전 경로 안내만 남겨 두었으며, **삭제해도 동작에 문제 없습니다**.)

| 규칙 파일 | 적용 방식 | 내용 |
|-----------|-----------|------|
| [magicsquare-project.mdc](.cursor/rules/magicsquare-project.mdc) | 항상 (`alwaysApply`) | 프로젝트 목적, 고정 계약(`int[4][4]`→`int[6]`, M=34), 디렉터리, AI 작업 순서 |
| [magicsquare-forbidden.mdc](.cursor/rules/magicsquare-forbidden.mdc) | 항상 | 금지 패턴(`print`, 매직 넘버, RED 생략, mock 남용 등) |
| [magicsquare-python-code-style.mdc](.cursor/rules/magicsquare-python-code-style.mdc) | `**/*.py` 열릴 때 | Python 3.14, PEP8, type hints, Black, Google docstring |
| [magicsquare-ecb-architecture.mdc](.cursor/rules/magicsquare-ecb-architecture.mdc) | `src/magicsquare/**`, `tests/**` | ECB 레이어·의존 방향, Dual-Track Mock 정책 |
| [magicsquare-tdd-testing.mdc](.cursor/rules/magicsquare-tdd-testing.mdc) | `tests/**`, `src/magicsquare/**` | RED/GREEN/REFACTOR, pytest, 커버리지(80%/Boundary 85%) |

**권위 문서와의 관계:** 규칙의 계약·Test-ID·Invariant는 `Report/01`, `Report/02`, 본 README와 일치하도록 유지합니다. 규칙을 수정할 때는 해당 보고서와 함께 검토하세요.

**확인:** Cursor **Settings → Rules**에서 위 파일이 보이는지, 또는 관련 `.py` 파일을 연 새 Agent 채팅에서 TDD·ECB 제약이 반영되는지 확인합니다.

---

## 범위 (현재)

**포함 (문제 정의 단계)**

- 4×4 고정
- 규칙: 1~16 각 1회, 행·열·대각 합 동일
- 판정·신뢰 관계·TDD적 접근 방향

**아직 포함하지 않음**

- 구현 언어·프레임워크
- UI·CLI·API
- n×n 일반화, 모든 해 탐색
- 배포·성능·영속화

---

## 다음 단계

1. **STEP 6 — Acceptance framing**  
   검증 가능한 요구 문장, 통과/실패 수용 예시 정리
2. **설계**  
   판정 · 생성 · 표현 경계 확정 (보고서 승인 후)
3. **구현 (TDD)**  
   검증 → 생성 → 표현 순으로 점진적 구축

---

## 문서 이력

| 버전 | 일자 | 내용 |
|------|------|------|
| 1.0 | 2026-05-28 | README 최초 작성 (문제 정의 STEP 1~5 반영) |
| 1.1 | 2026-05-28 | `.cursor/rules/*.mdc` Project Rules 섹션·프로젝트 구조 반영 |

---

## 참고

- 상세 분석·표·Why 전개는 [Report/01.문제정의_보고서.md](Report/01.문제정의_보고서.md)를 참고하세요.
- 설계·TDD·ECB·Test-ID는 [Report/02.DualTrack_CleanArch_TDD_설계.md](Report/02.DualTrack_CleanArch_TDD_설계.md)를 참고하세요.
- Cursor 에이전트 규칙은 [`.cursor/rules/`](.cursor/rules/)의 `magicsquare-*.mdc`를 참고하세요.
- 본 README는 **구현·알고리즘·코드**를 상세히 다루지 않습니다.
