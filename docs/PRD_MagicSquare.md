# PRD — Magic Square 4x4 TDD Practice

| 항목 | 내용 |
|------|------|
| **문서 ID** | PRD-MSQ-4X4-001 |
| **버전** | 1.0 (Draft) |
| **작성 기준일** | 2026-05-28 |
| **상태** | 구현 전 기준 문서 (Normative) |
| **권위 출처** | Report/01, Report/02, Report/03, `.cursor/rules/*.mdc` |
| **저장 경로** | `docs/PRD_MagicSquare.md` |

---

## 1. Executive Summary

Magic Square 4×4 TDD Practice는 **알고리즘 난이도 훈련이 아니라**, 4×4 마방진 퍼즐(빈칸 2개)에 대해 **고정된 입출력 계약**을 만족하는 해를 반환하는 순수 로직 시스템을 **Dual-Track UI + Logic TDD**와 **ECB(Clean Architecture)** 로 구축하는 학습 프로젝트이다. 호출자는 `int[4][4]` 퍼즐 격자를 제출하고, 시스템은 계약 검증 후 `int[6] = [r1,c1,n1,r2,c2,n2]`(1-index)를 반환하거나 **고정된 `ErrorResponse`** 를 반환한다. 성공 시 완성 격자는 `MagicSquareValidator` 기준(I-D2~I-D7, M=34)을 **반드시** 통과해야 하며(I-10), 동일 입력은 동일 출력을 보장한다(I-D12).

**훈련하려는 핵심 역량:** (1) 불변식·비즈니스 규칙 명시화, (2) Boundary/Domain 입출력 계약 고정, (3) Track A(계약)·Track B(불변식) 분리 TDD, (4) RED→GREEN→REFACTOR와 Concept→Test→Component 추적성.

---

## 2. Background

Report/01에 따르면, 초기 의도는 “4×4 마방진을 만든다”였으나 규칙·입출력·역할이 분리되지 않아 **산출물(16칸) 중심**, **검증 생략**, **생성·판정·표현 혼재** 위험이 있다. 본 프로젝트는 교육·아키텍트 실습 맥락에서 **제약 만족 문제를 계약·불변식·테스트 가능 요구로 고정**하는 것을 목표로 한다.

단순 “마방진 풀이기”가 아닌 이유: 손계산은 일회성이며, 프로그램은 **반복 실행·자동 판정·오류 방지·규칙 명시**(Why #2)를 가능하게 한다. TDD는 “완성된 격자” 요구에 수렴하는 **범위 creep**를 막고, **검증 가능한 단위(입력·출력·판정)** 를 먼저 고정한다(Why #3). 따라서 본 PRD는 UI/DB/Web 없이 **Boundary 계약 + Domain 불변식**만으로 구현 가능한 범위를 정의한다.

---

## 3. Problem Statement

### 3.1 표면 정의 (지양)

“4×4 칸에 숫자를 넣어 행·열·대각선 합이 같은 마방진을 **완성하는 프로그램**을 만든다.”

### 3.2 진짜 정의 (Normative)

시스템은 다음을 **동시에** 만족해야 한다.

1. 4×4 마방진 **규칙을 명시**한다(1~16 각 1회, 행·열·주대각·부대각 합 = M=34).
2. 주어진 **부분 배치(빈칸 2개)** 에 대해, 규칙을 만족하는 **완전 배치로의 채움**을 시도 A→B 순으로 결정한다.
3. 반환된 해 `int[6]`로 완성한 격자는 **`MagicSquareValidator` 통과와 동치**이다(I-10).
4. 모든 외부 관측 가능 동작은 **입력/출력 계약 및 고정 에러 스키마**로 검증 가능하다.

### 3.3 입력/출력 계약이 핵심인 이유

- 실패 원인이 학습·디버깅 정보가 되려면 **필드·코드·메시지**가 사전 고정되어야 한다.
- Boundary(0-index 배열)와 외부 좌표(1-index) 혼동을 **계약으로 차단**한다.
- Dual-Track TDD에서 Track A는 **계약**, Track B는 **불변식**을 각각 독립 RED/GREEN 한다.

---

## 4. Why Now / Why Chain

| 단계 | 핵심 | 학습자 Pain Point |
|------|------|-------------------|
| **Why #1** | “완성”이 아니라 **규칙 성립 확인·재검증** | 정답 격자만 출력하고 판정기와 불일치 |
| **Why #2** | 프로그램 = **반복·자동 검증·규칙 명시** | 손검산·대각 누락·기준 불일치 |
| **Why #3** | TDD = **계약·불변식 선고정** (생성 ⊂ 검증) | 구현 먼저, 테스트 기준 사후 작성 |

**Why Now:** 구현 착수 전에 PRD로 **계약·불변식·실패 정책·Dual-Track 검증**을 고정하지 않으면, Boundary와 Domain 책임이 섞이고 REFACTOR 후 **에러 메시지·출력 형식 회귀**가 발생한다.

**닫아야 하는 Gap**

| Gap | PRD 대응 |
|-----|----------|
| 테스트 기준 불명확 | FR-xx AC, §16 Test Plan, §21 Traceability |
| Boundary/Domain 혼합 | §17 Architecture, FR-01 vs FR-02~05 Layer |
| 리팩토링 후 계약 파손 | §13 고정 메시지, §15.3 REFACTOR 제약, REG-1~2(Report/02) |
| 구현 우선 | §15 Dual-Track RED 선행 |

---

## 5. Target Users

| 역할 | 목적 | 사용 환경 |
|------|------|-----------|
| **TDD 학습자** | RED-GREEN-REFACTOR, 계약 테스트 작성 | pytest, 로컬 CLI/테스트 하네스 |
| **Clean Architecture·ECB 학습자** | 레이어·의존 방향 훈련 | `src/{boundary,control,entity}` |
| **코드 리뷰어** | 계약·불변식·Traceability 검증 | PR diff, Test-ID 대조 |

**범위 밖 사용자·환경:** 최종 GUI 사용자, DB 운영자, Web/API 클라이언트, 인증·권한 관리자.

---

## 6. Vision & Epic Goal

### 6.1 Vision

**“불변식 기반 사고와 계약 기반 검증을 하나의 실행 가능한 4×4 퍼즐 해결 흐름으로 고정한다.”**

### 6.2 Epic

| Epic ID | 이름 | Goal | 완료 정의 |
|---------|------|------|-----------|
| **EPIC-1** | 불변식 기반 사고 훈련 시스템 구축 | 2빈칸 퍼즐 → `int[6]` 또는 `ErrorResponse` | §16 Normal·Exception 시나리오 전부 통과, §14 커버리지 충족, §21 Traceability 100% 연결 |

> **출처 참고:** `Report/4.UserJourney_Epic_to_TechnicalScenario_Report.md`는 저장소에 없음. Epic·Journey는 Report/02 §2.1·§4.2 및 Report/01 학습 목표에서 **파생**하였음(§22 참조).

### 6.3 User Stories (Epic-1)

| Story ID | As a … | I want … | So that … |
|----------|--------|----------|-----------|
| **US-1** | TDD 학습자 | 유효한 4×4 퍼즐을 제출하면 6원 해 벡터를 받는다 | Domain 불변식이 충족됨을 검증할 수 있다 |
| **US-2** | TDD 학습자 | 잘못된 입력은 Domain 호출 없이 즉시 거절된다 | Boundary 계약을 독립 RED할 수 있다 |
| **US-3** | TDD 학습자 | 해가 없으면 고정 코드·메시지로 실패한다 | 실패 정책이 테스트로 고정된다 |
| **US-4** | 리뷰어 | Concept→Test→Component 추적표를 본다 | 요구 누락·책임 혼합을 검출한다 |

---

## 7. Persona

### 7.1 Persona A — “계약 우선” TDD 학습자 (Primary)

- **목표:** Boundary RED부터 작성, Domain Mock으로 UI Track 완료.
- **성공:** `E_*` 메시지 바이트 일치, Domain resolver 미호출 분기 검증.
- **실패 패턴:** Solver 로직을 Boundary에 구현.

### 7.2 Persona B — “불변식 우선” Domain 학습자

- **목표:** Mock 없이 `Grid`·Validator·Solver RED.
- **성공:** D-T 시나리오로 I-D* 보호, A/B 시도·A 우선 규칙 검증.
- **실패 패턴:** 정답 격자 스냅샷만 비교.

### 7.3 Persona C — 아키텍트·리뷰어

- **목표:** ECB 의존 방향, I-10 신뢰 원칙, 커버리지 gate.
- **성공:** §21 매트릭스와 PR Test-ID 일치.

---

## 8. User Journey Summary

| 단계 | 활동 | Pain Point | Learning Outcome | 관련 산출물 |
|------|------|------------|------------------|-------------|
| 1. 문제 인식 | “16칸 채우기”에서 규칙·판정 분리 필요 인식 | 규칙 모호 | 진짜 문제 정의(§3) | Report/01 |
| 2. 계약 정의 | Input/Output/Error 스키마 고정 | 0/1-index 혼동 | §12, §13 | Report/02 §2.2 |
| 3. 도메인 분리 | I-D*, UC-D*, 컴포넌트 후보 확정 | Solver⊂Validator 혼동 | §11, §18 | Report/02 §1 |
| 4. Dual-Track TDD | Track A·B 각각 RED→GREEN | Domain 전부 후 Boundary | §15 | `.mdc` tdd-testing |
| 5. 통합·회귀 | IT 시나리오, 메시지 REG | REFACTOR 후 메시지 변경 | §16, REG-1 | Report/02 §4 |

**호출자 기술 흐름 (Normative):**

```
Caller → int[4][4]
  → Boundary: InputContract 검증
      ├─ 실패 → ErrorResponse (Domain 미호출)
      └─ 성공 → Control: SolvePuzzleUseCase → Domain: solve
            ├─ DomainError → ErrorResponse (매핑)
            └─ SolutionVector → Boundary: OutputContract 검증 → int[6]
```

---

## 9. Scope

### 9.1 In-Scope

| ID | 항목 |
|----|------|
| S-01 | 4×4 퍼즐 입력, `0` 빈칸 정확히 2개 |
| S-02 | 행 우선(row-major) 1·2번 빈칸 식별 |
| S-03 | 누락 숫자 2개, `m1 < m2` |
| S-04 | 시도 A(small-first)→시도 B(reverse), A·B 모두 성공 시 **A 결과** |
| S-05 | 완전 격자 마방진 판정(M=34, I-D2~D7) |
| S-06 | Boundary 입력·출력 계약 검증 |
| S-07 | Control `SolvePuzzleUseCase` 오케스트레이션 |
| S-08 | Dual-Track pytest, AAA, Test-ID, 커버리지 gate |
| S-09 | 통합 경로: Boundary→Control→Domain (IT-01급) |

### 9.2 Out-of-Scope

| ID | 항목 | 비고 |
|----|------|------|
| O-01 | GUI 화면·위젯 | Boundary=계약만 |
| O-02 | DB·파일 영속화·`MatrixRepository` | Report/02 Data Layer는 **본 PRD 범위 외** |
| O-03 | Web/API 서버 | — |
| O-04 | N×N 일반화 | — |
| O-05 | 빈 격자부터 완전 마방진 **생성** 알고리즘 | 본 제품은 2빈칸 **완성**만 |
| O-06 | 사용자 인증·권한·`User` 엔티티 | Report/03 보조 실습, 제품 FR 아님 |
| O-07 | QR·외부 연동·네트워크 오류 | — |
| O-08 | n×n 전체 해 탐색 | — |
| O-09 | Report/01 I-11 일반 부분 격자 조기 위반 API | 2빈칸 퍼즐만 대상 |

---

## 10. Functional Requirements

### FR-01 Input Verification (Boundary)

- **Description:** 호출자가 제출한 `int[4][4]`가 Input Contract를 만족하는지 검증한다.
- **Layer:** Boundary (`InputContractValidator` / `PuzzleBoundary`)
- **Input:** `int[4][4]` (호출자 소유, 0-index)
- **Processing Rules:**
  - 행 수 = 4, 각 행 열 수 = 4이 아니면 즉시 실패.
  - 각 셀 ∈ `{0} ∪ [1,16]`이 아니면 즉시 실패.
  - `count(0) ≠ 2`이면 즉시 실패.
  - 비零 값 중복이면 즉시 실패.
  - 검증 순서는 구현 선택 가능하나, **첫 위반 규칙에 대응하는 Error Code**가 결과에 반영되어야 한다(동일 입력→동일 code).
- **Output:** 검증 통과 시 Control에 위임; 실패 시 `ErrorResponse`
- **Acceptance Criteria:**
  - AC-FR01-1: 3×4 격자 제출 시 `code=E_SIZE`, message=`ERROR: Grid must be 4x4.` (U-T01)
  - AC-FR01-2: `0`이 1개인 격자 제출 시 `E_EMPTY_COUNT` (U-T02)
  - AC-FR01-3: 값 17 포함 시 `E_RANGE` (U-T03)
  - AC-FR01-4: 비零 중복 시 `E_DUPLICATE` (U-T04)
  - AC-FR01-5: 위 4종 실패 시 **Domain `solve` 0회 호출** (Mock 호출 횟수 검증)
- **Error / Exception Policy:** `ErrorResponse` 반환; 예외를 호출자에 전파하지 않는다(본 PRD Normative).
- **Related Business Rules:** BR-01~BR-05
- **Related Test Direction:** Track A — U-T01~U-T04; `unit` marker
- **Component Candidate:** `InputContractValidator`, `PuzzleBoundary`

---

### FR-02 Blank Coordinate Discovery (Domain)

- **Description:** 유효 퍼즐 `Grid`에서 row-major 스캔으로 1번·2번 빈칸 좌표(1-index)를 결정한다.
- **Layer:** Entity — `EmptyCellLocator`
- **Input:** I-D8·I-D9를 만족하는 `Grid`
- **Processing Rules:**
  - `r=1..4`, `c=1..4` 순으로 스캔하며 첫 `0` → 1번, 둘째 `0` → 2번.
  - `count(0) ≠ 2`이면 `DomainError(INVALID_EMPTY_COUNT)`.
- **Output:** `EmptySlotPair` — `((r1,c1),(r2,c2))` 1-index
- **Acceptance Criteria:**
  - AC-FR02-1: (2,3),(3,1)에 `0`인 격자에서 1번=(2,3), 2번=(3,1) (D-T03)
  - AC-FR02-2: `0`이 1개·3개면 `INVALID_EMPTY_COUNT` (D-T10, D-T11)
- **Error / Exception Policy:** Domain 내부 `DomainError`; Boundary에서는 입력 검증 후에만 호출되므로 `INVALID_EMPTY_COUNT`는 **이중 방어** 시나리오.
- **Related Business Rules:** BR-02, BR-05
- **Related Test Direction:** Track B — D-T03, D-T10, D-T11; Mock 금지
- **Component Candidate:** `EmptyCellLocator` (BlankFinder)

---

### FR-03 Missing Number Discovery (Domain)

- **Description:** 비零 14개 값으로부터 `{1..16}`에 없는 두 수 `m1,m2` (`m1<m2`)를 계산한다.
- **Layer:** Entity — `MissingNumberFinder`
- **Input:** `Grid` (14 non-zero, I-D9)
- **Processing Rules:** `missing = {1..16} \ values_nonzero`, `|missing|=2`, 정렬 후 `m1<m2`
- **Output:** `MissingPair(m1,m2)`
- **Acceptance Criteria:**
  - AC-FR03-1: 고정 14칸 픽스처에서 `m1,m2`가 기대와 일치 (D-T05)
  - AC-FR03-2: 누락 수 개수 ≠ 2이면 `INVALID_MISSING_COUNT` (D-T16류와 구분: 크기 오류는 `INVALID_GRID_SIZE`)
- **Error / Exception Policy:** `DomainError(INVALID_MISSING_COUNT)`
- **Related Business Rules:** BR-06, BR-07
- **Related Test Direction:** Track B — D-T05
- **Component Candidate:** `MissingNumberFinder`

---

### FR-04 Magic Square Validation (Domain)

- **Description:** **완전 채워진** 4×4 격자가 I-D2~I-D7을 만족하는지 판정한다.
- **Layer:** Entity — `MagicSquareValidator`
- **Input:** 완전 `Grid` (빈칸 없음)
- **Processing Rules:**
  - 모든 값 ∈ [1,16], 1~16 각 1회.
  - 네 행·네 열·주대각·부대각 합 = `MagicConstant.M` (=34).
- **Output:** `boolean` (`true` = 유효 마방진)
- **Acceptance Criteria:**
  - AC-FR04-1: 알려진 유효 완성 4×4에 `true` (D-T04)
  - AC-FR04-2: 행 합이 M을 초과하는 완성 격자에 `false`
  - AC-FR04-3: FR-05가 성공 주장한 완성 격자는 **항상** `true` (I-10)
- **Error / Exception Policy:** 판정 실패는 `false`; 예외 아님.
- **Related Business Rules:** BR-08~BR-10
- **Related Test Direction:** Track B — D-T04, D-T15; 통합 IT-01 validator=true
- **Component Candidate:** `MagicSquareValidator`

---

### FR-05 Two-Combination Solver and Result Formatting (Domain + Boundary)

- **Description:** 시도 A(small-first) 후 시도 B(reverse)로 빈칸을 채우고, 성공 시 `int[6]`를 반환한다.
- **Layer:** Entity `PuzzleSolver` + Control `SolvePuzzleUseCase` + Boundary 출력 검증
- **Input:** I-D8·I-D9 만족 `Grid`
- **Processing Rules:**
  1. FR-02, FR-03 실행.
  2. **시도 A:** 1번 빈칸←`m1`, 2번←`m2` → 완성 격자 → FR-04; `true`이면 `[r1,c1,m1,r2,c2,m2]` 반환.
  3. **시도 B:** 1번←`m2`, 2번←`m1` → FR-04; `true`이면 `[r1,c1,m2,r2,c2,m1]` 반환.
  4. A·B 모두 `false` → `DomainError(NO_VALID_COMPLETION)` → Boundary `E_NO_SOLUTION`.
  5. A·B 모두 `true` → **A 결과만** 반환 (I-D12).
  6. 호출자 입력 배열은 **변경하지 않는다**(§14.3).
- **Output:** 성공 `int[6]`; 실패 `ErrorResponse(E_NO_SOLUTION, …)`
- **Acceptance Criteria:**
  - AC-FR05-1: A만 성공 시 small-first 벡터 (D-T01)
  - AC-FR05-2: A 실패·B 성공 시 reverse 벡터 (D-T02)
  - AC-FR05-3: A·B 모두 실패 시 `E_NO_SOLUTION` (D-T13, U-T06, IT-F02)
  - AC-FR05-4: A·B 모두 성공 시 A 벡터 (D-T14)
  - AC-FR05-5: 성공 시 `(r1,c1)≠(r2,c2)`, `{n1,n2}=missing`, 좌표가 입력 `0` 위치와 일치 (Output Contract)
  - AC-FR05-6: Boundary가 반환 전 Output Contract 위반 시 `E_OUTPUT_FORMAT` (U-T07)
- **Error / Exception Policy:** Domain `NO_VALID_COMPLETION` → Boundary `E_NO_SOLUTION`; 메시지 고정(§13).
- **Related Business Rules:** BR-05~BR-07, BR-11~BR-14
- **Related Test Direction:** Track B D-T01,02,13,14,15; Track A U-T05~07; Integration IT-01, IT-03
- **Component Candidate:** `PuzzleSolver`, `SolutionVector`, `SolvePuzzleUseCase`, `OutputContractValidator`

---

## 11. Business Rules / Domain Rules

| ID | 규칙 (항상 참) | 검증 레이어 |
|----|----------------|-------------|
| **BR-01** | 입력 격자는 정확히 4행×4열이다. | Boundary |
| **BR-02** | 셀 값은 `0` 또는 `[1,16]`의 정수이다. | Boundary |
| **BR-03** | `0`의 개수는 정확히 2이다. | Boundary (+ Domain 이중 방어 가능) |
| **BR-04** | `0`이 아닌 값은 격자 내에서 유일하다. | Boundary |
| **BR-05** | 1번 빈칸은 row-major 스캔에서 **첫 번째** `0`의 1-index 좌표이다. | Domain |
| **BR-06** | 2번 빈칸은 row-major 스캔에서 **두 번째** `0`의 1-index 좌표이다. | Domain |
| **BR-07** | 누락 숫자는 `{1..16}`에서 비零 값을 제외한 집합이며, 크기는 2이다. | Domain |
| **BR-08** | 누락 숫자 `m1`, `m2`는 `m1 < m2`이다. | Domain |
| **BR-09** | 완전 격자에서 1~16은 각각 정확히 1회 나타난다. | Domain (FR-04) |
| **BR-10** | 완전 격자에서 네 행·네 열·주대각·부대각의 합은 모두 `M=34`이다. | Domain (FR-04) |
| **BR-11** | 시도 A는 1번 빈칸←`m1`, 2번←`m2`이다. | Domain (FR-05) |
| **BR-12** | 시도 B는 1번 빈칸←`m2`, 2번←`m1`이다. | Domain (FR-05) |
| **BR-13** | A·B 모두 마방진이면 **A의 `int[6]`** 를 반환한다. | Domain (FR-05) |
| **BR-14** | 외부 성공 출력은 `int[6]=[r1,c1,n1,r2,c2,n2]`이며 `r*,c*`는 1..4, `n*`는 1..16이다. | Boundary |
| **BR-15** | 성공 시 `n1`은 1번 빈칸에 배치된 값, `n2`는 2번 빈칸에 배치된 값이다. | Boundary + Domain |
| **BR-16** | 완전 배치 성공 주장 ⟹ `MagicSquareValidator.isValid==true` (I-10). | Domain + Integration |

---

## 12. Input / Output Contract

### 12.1 Input Contract

| Field / Item | Type | Rule | Valid Example | Invalid Example | Error Code |
|--------------|------|------|---------------|-----------------|------------|
| `grid` | `int[4][4]` | 4 rows, each len 4 | 4×4 all ints | 3×3, 4×5 | `E_SIZE` |
| `grid[r][c]` | `int` | `0` or 1..16 | `0`, `7`, `16` | `-1`, `17` | `E_RANGE` |
| empty count | derived | `count(0)==2` | two `0`s | one or three `0`s | `E_EMPTY_COUNT` |
| non-zero uniqueness | derived | \|nonzero\| = \|set(nonzero)\| | 1..14 distinct | two `5`s | `E_DUPLICATE` |
| indexing (internal) | — | Boundary 내부 0-index | `grid[0][0]` | — | — |
| caller mutation | policy | 시스템은 **입력 배열 원소를 변경하지 않음** | — | in-place 수정 | §22 DN-03 |

### 12.2 Output Contract (Success)

| Index | Name | Type | Rule | Valid Example | Invalid Example | Error Code |
|-------|------|------|------|---------------|-----------------|------------|
| 0 | r1 | int | 1..4 | `2` | `0` | `E_OUTPUT_FORMAT` |
| 1 | c1 | int | 1..4 | `3` | `5` | `E_OUTPUT_FORMAT` |
| 2 | n1 | int | 1..16 | `7` | `0` | `E_OUTPUT_FORMAT` |
| 3 | r2 | int | 1..4 | `3` | — | `E_OUTPUT_FORMAT` |
| 4 | c2 | int | 1..4 | `1` | — | `E_OUTPUT_FORMAT` |
| 5 | n2 | int | 1..16 | `12` | — | `E_OUTPUT_FORMAT` |
| length | array | `len==6` | 6 ints | 5 ints | `E_OUTPUT_FORMAT` |
| slot match | constraint | `(r1,c1),(r2,c2)` = input zero positions (1-index) | — | swapped slots | `E_OUTPUT_FORMAT` |
| missing set | constraint | `{n1,n2}={m1,m2}` | — | wrong pair | `E_OUTPUT_FORMAT` |

### 12.3 Success Response Shape

- **형식:** `int[6]` **단독** 반환 (래퍼 객체 없음) — UX-1.
- **실패와 혼합 반환 금지** — UX-2.

---

## 13. Error / Failure Policy

**Normative 정책:** 모든 관측 가능 실패는 **`ErrorResponse { code: string, message: string }`** 를 반환한다. `message`는 아래 표와 **완전 일치**(대소문자·구두점·공백 포함) — UX-3.

**Domain resolver 호출:** Input Contract 실패 시 **호출 금지** (AC-FR01-5).

| 조건 | Error Code | Message (exact) | Layer | Domain 호출 | Related AC |
|------|------------|-----------------|-------|-------------|------------|
| 4×4 아님 | `E_SIZE` | `ERROR: Grid must be 4x4.` | Boundary | **No** | AC-FR01-1 |
| 빈칸 수 ≠ 2 | `E_EMPTY_COUNT` | `ERROR: Grid must contain exactly 2 empty cells (0).` | Boundary | **No** | AC-FR01-2 |
| 값 범위 위반 | `E_RANGE` | `ERROR: Cell value must be 0 or between 1 and 16.` | Boundary | **No** | AC-FR01-3 |
| 비零 중복 | `E_DUPLICATE` | `ERROR: Non-zero cell values must be unique.` | Boundary | **No** | AC-FR01-4 |
| A·B 모두 비마방진 | `E_NO_SOLUTION` | `ERROR: No valid magic square completion exists.` | Boundary (Domain `NO_VALID_COMPLETION` 매핑) | **Yes** (solve 시도 후) | AC-FR05-3 |
| 출력 계약 위반 | `E_OUTPUT_FORMAT` | `ERROR: Internal output contract violation.` | Boundary | Yes (내부 버그·계약 불일치) | AC-FR05-6 |

**Domain 내부 코드 (Boundary 외부 노출 금지):** `INVALID_GRID_SIZE`, `INVALID_EMPTY_COUNT`, `INVALID_MISSING_COUNT`, `NO_VALID_COMPLETION` — Control이 Boundary 코드로 매핑한다.

**두 조합 모두 실패:** 예외를 호출자에게 throw하지 않고 **`E_NO_SOLUTION` `ErrorResponse`** 를 반환한다 (본 PRD에서 확정).

---

## 14. Non-Functional Requirements

| ID | 요구 | 검증 방법 |
|----|------|-----------|
| **NFR-01** | Domain Logic **branch coverage ≥ 95%** (`EmptyCellLocator`, `MissingNumberFinder`, `MagicSquareValidator`, `PuzzleSolver`) | pytest-cov, CI gate |
| **NFR-02** | Boundary Validation **branch coverage ≥ 85%** (입력·출력·에러 매핑 분기) | pytest-cov |
| **NFR-03** | 전역 line/branch coverage **≥ 80%** (프로젝트 기본) | pytest-cov |
| **NFR-04** | **결정성:** 동일 `int[4][4]` 입력 → 동일 성공 `int[6]` 또는 동일 `ErrorResponse` (I-D12) | 반복 실행 테스트 |
| **NFR-05** | **부작용 없음:** 호출자가 전달한 `grid` 배열의 요소 값·구조를 변경하지 않음 | 입력 스냅샷 before/after assert |
| **NFR-06** | **성능:** 4×4 단일 solve 호출 wall-clock **≤ 50ms** (로컬 개발 PC, 워밍 후 1회 측정) | 벤치마크 또는 통합 테스트 상한 |
| **NFR-07** | Boundary는 Domain 알고리즘(합 계산·빈칸 탐색)을 **구현하지 않음** | 정적 검토·ECB WARNING |
| **NFR-08** | `34`, `4`, `16`, 고정 에러 문구를 **리터럴로 산재 금지** — `MagicConstant`, `GridSize`, `ErrorMessages` 등 명명 상수·VO | 코드 리뷰·forbidden 규칙 |
| **NFR-09** | `print()` 디버그 출력 금지 (UX-4) | capsys/리뷰 |
| **NFR-10** | `except:` / `except Exception` 광포 catch 금지 | 리뷰 |
| **NFR-11** | assertion 삭제·완화·`skip`·`xfail`로 통과 금지 | 리뷰·CI |
| **NFR-12** | 에러 메시지 변경 시 UI 테스트·CHANGELOG 동시 갱신 (REG-1) | PR 체크리스트 |

---

## 15. Dual-Track TDD Strategy

### 15.1 Track A — Boundary / UI Contract TDD

| 목표 | RED 예시 (Test-ID) | GREEN 최소 산출 | Mock |
|------|-------------------|-----------------|------|
| 크기 검증 | U-T01 | `E_SIZE` | Domain **미호출** |
| 빈칸 수 | U-T02 | `E_EMPTY_COUNT` | 미호출 |
| 값 범위 | U-T03 | `E_RANGE` | 미호출 |
| 중복 | U-T04 | `E_DUPLICATE` | 미호출 |
| 성공 경로 | U-T05 | `int[6]` len=6, solve 1회 | Domain/Application Mock |
| Domain 무해 | U-T06 | `E_NO_SOLUTION` | Mock `NO_VALID_COMPLETION` |
| 출력 검증 | U-T07 | `E_OUTPUT_FORMAT` | Mock 잘못된 벡터 |
| 메시지 회귀 | U-T08 | 모든 `E_*` 문구 일치 | — |

### 15.2 Track B — Domain / Logic TDD

| 목표 | RED 예시 | GREEN 최소 산출 | Mock |
|------|----------|-----------------|------|
| 행·열·대각 합 | D-T04 | `MagicSquareValidator` | **금지** |
| 빈칸 순서 | D-T03 | `EmptyCellLocator` | 금지 |
| 누락 수 | D-T05 | `MissingNumberFinder` | 금지 |
| small-first 성공 | D-T01 | `PuzzleSolver` A 경로 | 금지 |
| reverse 성공 | D-T02 | B 경로 | 금지 |
| dual fail | D-T13 | `NO_VALID_COMPLETION` | 금지 |
| A 우선 | D-T14 | A 결과 | 금지 |
| 조기 불가능 | D-T15 | `NO_VALID_COMPLETION` | 금지 |

### 15.3 Parallel Progression Rules

1. Track A·B 각각 **독립 RED**를 유지한다.
2. 각 Track은 **해당 실패 테스트 PASS에 필요한 최소 코드**만 GREEN한다.
3. **REFACTOR**는 해당 Track GREEN 확인 **후에만** 수행하며, 공개 계약·`E_*` 메시지·`int[6]` 의미는 변경하지 않는다.
4. **금지:** 전체 Domain 완료 후 Boundary만 붙이는 단일 워터폴.
5. **금지:** assertion 약화·삭제·skip·xfail.
6. **통합 테스트(IT-*)** 는 Track A·B **모두 GREEN** 이후에 추가·실행한다.
7. 권장 병렬 순서(Report/02·`.mdc` 정합): **Boundary 슬라이스 RED/GREEN** ↔ **Domain 슬라이스 RED/GREEN** 교차 진행, 마지막 통합.

---

## 16. Test Plan / QA

### 16.1 Normal Scenarios

| ID | 시나리오 | 기대 | Test-ID |
|----|----------|------|---------|
| N-01 | 시도 A만 성공 | `[r1,c1,m1,r2,c2,m2]` | D-T01, IT-01 |
| N-02 | A 실패, B 성공 | `[r1,c1,m2,r2,c2,m1]` | D-T02, IT-03 |
| N-03 | 유효 입력 E2E | `int[6]` + validator true | IT-01 |

### 16.2 Exception Scenarios

| ID | 시나리오 | 기대 | Test-ID |
|----|----------|------|---------|
| E-01 | 4×5 입력 | `E_SIZE`, Domain 미호출 | U-T01, IT-F01 |
| E-02 | 빈칸 3개 | `E_EMPTY_COUNT` | U-T02, IT-F04 |
| E-03 | 값 17 | `E_RANGE` | U-T03 |
| E-04 | 비零 중복 | `E_DUPLICATE` | U-T04 |
| E-05 | A·B 모두 실패 | `E_NO_SOLUTION` | D-T13, U-T06, IT-F02 |

### 16.3 Boundary Scenarios

| ID | 시나리오 | 기대 |
|----|----------|------|
| B-01 | `n1=1`, `n2=16` (경계 값) | Output Contract 통과 |
| B-02 | `r,c ∈ {1,4}` | Output Contract 통과 |
| B-03 | `0`은 빈칸만 | `E_RANGE` if misused |
| B-04 | 반환 배열 길이 6 | U-T05 |
| B-05 | A·B 동시 성공 | A 벡터 (D-T14) |

### 16.4 Representative Test Data

**Invalid (구조 명확 — 구현 픽스처로 고정 가능)**

| Label | Grid (0-index rows) | Expected |
|-------|---------------------|----------|
| `invalid_size` | `[[1,2,3],[4,5,6],[7,8,9]]` | `E_SIZE` |
| `invalid_blank_1` | 4×4 with exactly one `0` | `E_EMPTY_COUNT` |
| `invalid_range` | any cell `17` or `-1` | `E_RANGE` |
| `duplicate_five` | two cells with value `5`, rest valid | `E_DUPLICATE` |

**Valid / Success (수치는 Report/02 Test-ID 픽스처와 동기화 필수)**

| Label | 설명 | Test-ID anchor |
|-------|------|----------------|
| `small_first_success` | A만 마방진 | D-T01 |
| `reverse_only_success` | B만 마방진 | D-T02 |
| `both_valid_A_wins` | A·B 모두 마방진 | D-T14 |
| `no_completion` | A·B 모두 실패 | D-T13, IT-F02 |
| `row_major_blanks` | 1번=(2,3), 2번=(3,1) | D-T03 |

> **주의:** 성공 격자의 **구체 16개 정수**는 RED 작성 시 Report/02 D-T/IT 픽스처와 동일한지 Validator로 확인한 뒤 고정한다. PRD는 구조·규칙만 Normative로 둔다.

### 16.5 Verification Checklist (Release)

- [ ] §13 모든 `E_*` message byte-equal (U-T08)
- [ ] AC-FR01-5 Domain 미호출 분기
- [ ] AC-FR05-6 Output Contract
- [ ] I-10: 모든 IT 성공 케이스 validator=true
- [ ] NFR-01~03 coverage
- [ ] §21 Traceability 14 Concept 행 전부 채움

---

## 17. Architecture Overview (High-Level)

### 17.1 Layers

| Layer | 책임 | 포함 컴포넌트 (후보) |
|-------|------|----------------------|
| **Boundary** | Input/Output Contract, `ErrorResponse`, 고정 메시지 | `PuzzleBoundary`, `InputContractValidator`, `OutputContractValidator` |
| **Control** | Use Case 오케스트레이션, DomainError→Boundary 매핑 | `SolvePuzzleUseCase` |
| **Entity (Domain)** | 순수 규칙·불변식 | `Grid`, VO들, `EmptyCellLocator`, `MissingNumberFinder`, `MagicSquareValidator`, `PuzzleSolver` |

### 17.2 Dependency Rules

**허용:** `boundary → control → entity`

**금지:**

- `entity → control`, `entity → boundary`
- `control → boundary`
- `boundary → entity` **직접** (`PuzzleSolver`/`MagicSquareValidator` 호출 금지)
- Domain이 UI/DB/Web/파일/고정 영문 에러 문구 의존

### 17.3 Request Flow

```
Caller
  → PuzzleBoundary.receive(grid)
      → InputContractValidator
      → SolvePuzzleUseCase.execute(grid)
          → Grid.of → PuzzleSolver.solve → SolutionVector
      → OutputContractValidator
  ← int[6] | ErrorResponse
```

---

## 18. Component Candidates

| Component | Layer | Responsibility | Input | Output | Related FR | Related Test |
|-----------|-------|----------------|-------|--------|------------|--------------|
| `InputContractValidator` | Boundary | BR-01~04 검증 | `int[4][4]` | pass / `ErrorResponse` | FR-01 | U-T01~04 |
| `OutputContractValidator` | Boundary | BR-14~15, 길이 6 | `int[6]`, input grid | pass / `E_OUTPUT_FORMAT` | FR-05 | U-T07 |
| `PuzzleBoundary` | Boundary | S1~S5 오케스트레이션 | `int[4][4]` | `int[6]` \| `ErrorResponse` | FR-01,05 | U-T*, IT-* |
| `SolvePuzzleUseCase` | Control | D1→D2→D4 위임·매핑 | valid grid | `SolutionVector` \| map error | FR-05 | IT-01 |
| `Grid` | Entity | 4×4 스냅샷 | `int[4][4]` | `Grid` | FR-02~05 | D-T16 |
| `EmptyCellLocator` | Entity | BR-05~06 | `Grid` | `EmptySlotPair` | FR-02 | D-T03,10,11 |
| `MissingNumberFinder` | Entity | BR-07~08 | `Grid` | `MissingPair` | FR-03 | D-T05 |
| `MagicSquareValidator` | Entity | BR-09~10 | 완전 `Grid` | `boolean` | FR-04 | D-T04 |
| `PuzzleSolver` | Entity | BR-11~13 | `Grid` | `SolutionVector` \| `DomainError` | FR-05 | D-T01,02,13,14,15 |
| `SolutionVector` | Entity | BR-14~15 내부 검증 | 6 ints | `int[6]` | FR-05 | D-T01 |

*BlankFinder / ResultFormatter 명칭은 각각 `EmptyCellLocator`, `SolutionVector`+`OutputContractValidator`로 대응한다.*

---

## 19. Risks & Ambiguities

| Risk | Impact | Mitigation / Decision |
|------|--------|------------------------|
| 1-index vs 0-index 혼동 | 잘못된 `int[6]` | 출력만 1-index; Boundary 내부 0-index 문서화(§12) |
| row-major 정의 누락 | 빈칸 순서 오류 | BR-05~06, D-T03 필수 |
| small-first vs reverse 픽스처 혼동 | 잘못된 GREEN | Test-ID별 픽스처 라벨 분리(§16.4) |
| 입력 배열 변경 | 호출자 상태 오염 | NFR-05 assert |
| Boundary에 Solver 로직 | Dual-Track 붕괴 | ECB 금지·리뷰 |
| `34` 하드코딩 | 단일 진실 공급원 파괴 | `MagicConstant` VO (NFR-08) |
| Report/4 부재 | Journey·Gherkin 공백 | §22 — Report/04 User Journey 작성 후 PRD 1.1 갱신 |
| Report/02 Data Layer vs PRD O-02 | 범위 혼선 | **본 PRD: DB/Repository Out-of-Scope** |
| Report/03 `User` entity | FR 범위 오염 | **Out-of-Scope O-06** |
| 첫 RED `ModuleNotFoundError` vs import 금지 규칙 | TDD 시작 막힘 | §22 DN-02 |
| README “미구현” vs 부분 구현 | 계획 혼선 | README 동기화(운영) |

---

## 20. Engineering Principles

| 영역 | 원칙 (Normative 요약) |
|------|----------------------|
| **언어·스타일** | Python 3.14, PEP8, Black line-length 88, type hints 필수, public Google docstring |
| **테스트** | pytest, AAA, `test_` 접두사, Test-ID docstring (`D-T01`, `U-T01`) |
| **커버리지** | Domain branch ≥95%, Boundary branch ≥85%, global ≥80% |
| **아키텍처** | ECB, `boundary→control→entity`, Boundary는 UseCase 경유 |
| **TDD** | RED→GREEN→REFACTOR, Track별 분리, 통합은 양 Track GREEN 후 |
| **금지** | `print()`, 매직 넘버·고정 문구 리터럴, bare except, RED 생략, Domain Track mock, assertion 약화, boundary→entity 직접 호출 |
| **경고 접두사** | `TDD WARNING:`, `ECB LAYER WARNING:`, `COVERAGE WARNING:` (AI/리뷰) |
| **권위 문서** | Report/01·02, `.cursor/rules/magicsquare-*.mdc` |

상세 원문: `.cursor/rules/magicsquare-forbidden.mdc`, `magicsquare-tdd-testing.mdc`, `magicsquare-ecb-architecture.mdc`, `magicsquare-python-code-style.mdc`.

---

## 21. Traceability Matrix

| Concept / Invariant | Business Rule | Feature ID | Acceptance Criteria | Test Case Candidate | Component |
|---------------------|---------------|------------|---------------------|---------------------|-----------|
| 4×4 입력 | BR-01 | FR-01 | AC-FR01-1 | U-T01, D-T16, IT-F01 | InputContractValidator |
| 빈칸 2개 | BR-03 | FR-01, FR-02 | AC-FR01-2, AC-FR02-2 | U-T02, D-T10,11, IT-F04 | InputContractValidator, EmptyCellLocator |
| 값 범위 0 또는 1~16 | BR-02 | FR-01 | AC-FR01-3 | U-T03 | InputContractValidator |
| 중복 금지 | BR-04 | FR-01 | AC-FR01-4 | U-T04, D-T12 | InputContractValidator |
| row-major 첫·둘째 빈칸 | BR-05, BR-06 | FR-02 | AC-FR02-1 | D-T03 | EmptyCellLocator |
| 누락 숫자 2개 | BR-07 | FR-03 | AC-FR03-1 | D-T05 | MissingNumberFinder |
| 누락 숫자 오름차순 | BR-08 | FR-03 | AC-FR03-1 | D-T05 | MissingNumberFinder |
| 마방진 상수 34 | BR-10 | FR-04 | AC-FR04-1 | D-T04 | MagicConstant, MagicSquareValidator |
| 행/열/대각선 합 | BR-10 | FR-04 | AC-FR04-1,2 | D-T04, D-T15 | MagicSquareValidator |
| small-first 시도 (A) | BR-11 | FR-05 | AC-FR05-1 | D-T01, IT-01 | PuzzleSolver |
| reverse 시도 (B) | BR-12 | FR-05 | AC-FR05-2 | D-T02, IT-03 | PuzzleSolver |
| A·B 모두 실패 | BR-11,12 + §13 | FR-05 | AC-FR05-3 | D-T13, U-T06, IT-F02 | PuzzleSolver, PuzzleBoundary |
| A·B 모두 성공 시 A 우선 | BR-13 | FR-05 | AC-FR05-4 | D-T14 | PuzzleSolver |
| int[6] 반환 | BR-14 | FR-05 | AC-FR05-5 | U-T05, IT-01 | SolutionVector, OutputContractValidator |
| 1-index 좌표 | BR-14 | FR-05 | AC-FR05-5 | U-T05, U-T07 | OutputContractValidator |
| I-10 신뢰 (해⟹validator) | BR-16 | FR-04,05 | AC-FR04-3 | IT-01 | MagicSquareValidator |
| 입력 검증 시 Domain 미호출 | §13 | FR-01 | AC-FR01-5 | U-T01~04 | PuzzleBoundary |
| 결정성 I-D12 | — | FR-05 | NFR-04 | D-T14 context | PuzzleSolver |
| 고정 에러 메시지 | §13 | FR-01,05 | U-T08 | U-T08 | ErrorMessages, PuzzleBoundary |

---

## 22. Open Questions / Decision Needed

| ID | 주제 | 설명 | 권장 조치 |
|----|------|------|-----------|
| **DN-01** | **Report/4 User Journey 문서 부재** | `Report/4.UserJourney_Epic_to_TechnicalScenario_Report.md` 미존재. §6~8·US·Gherkin은 Report/02에서 파생. | User Journey 보고서 작성 후 PRD v1.1 |
| **DN-02** | **첫 RED vs import 오류** | `magicsquare-tdd-testing.mdc`는 import/문법 오류를 RED로 대체 금지. 빈 모듈 첫 RED 시 `ModuleNotFoundError` 허용 여부. | 팀 규칙 1문장 추가 |
| **DN-03** | **입력 검증 실패 순서** | 복수 위반 시 노출 `E_*` 우선순위(Report/02 미명시). | 우선순위 표 추가 또는 “첫 발견” 고정 |
| **DN-04** | **Report/02 Data Layer** | Repository·JSON은 설계에 있으나 본 PRD §9.2 O-02로 제외. | Epic-2로 분리 시 별도 PRD |
| **DN-05** | **CI coverage gate** | Report/03: 에이전트만으로 커버리지 강제 한계. | pre-commit/CI에서 NFR-01~03 gate |
| **DN-06** | **README 진행 상태** | README는 “구현 미착수”, Report/03은 `User` 구현 완료. | README 동기화(문서 운영) |

---

## 23. Appendix

### 23.1 참고 문서

| 문서 | 경로 (실제) | PRD 역할 |
|------|-------------|----------|
| Report/1 Problem Definition | `Report/01.문제정의_보고서.md` | §2~4 |
| Report/2 Design | `Report/02.DualTrack_CleanArch_TDD_설계.md` | §9~13, §15~18, §21 |
| Report/3 Dev Environment | `Report/03.CursorRules_UserEntity_구현보고서.md` | §20 |
| Report/4 User Journey | **없음** | §6~8, §23.3 — DN-01 |
| Cursor Rules | `.cursor/rules/magicsquare-*.mdc` | §20 |
| Legacy | `.cursorrules` (deprecated pointer) | 링크만 |

### 23.2 Cursor Rules 요약

| 파일 | 핵심 |
|------|------|
| `magicsquare-project.mdc` | 계약, 디렉터리, AI 작업 순서 |
| `magicsquare-tdd-testing.mdc` | Dual-Track, RED/GREEN/REFACTOR, 커버리지 |
| `magicsquare-ecb-architecture.mdc` | 레이어·의존·Mock 정책 |
| `magicsquare-forbidden.mdc` | 금지 패턴 8종 |
| `magicsquare-python-code-style.mdc` | Python 스타일 |

### 23.3 Gherkin Scenario 요약 (Epic-1)

```gherkin
Feature: Solve 4x4 magic square puzzle with two blanks
  As a TDD learner
  I want a deterministic int[6] solution or a fixed error response
  So that contracts and invariants remain testable

  Scenario: Valid puzzle returns six-int solution (Attempt A succeeds)
    Given a valid 4x4 grid with exactly two cells 0
    And non-zero values are unique and in 1..16
    When the boundary receives the grid
    Then the domain solver is invoked exactly once
    And the response is an int array of length 6
    And coordinates in positions 0,1,3,4 are between 1 and 4
    And completing the grid with n1 and n2 yields a valid magic square

  Scenario: Invalid size rejects without domain call
    Given a grid that is not 4x4
    When the boundary receives the grid
    Then the response code is "E_SIZE"
    And the message is "ERROR: Grid must be 4x4."
    And the domain solver is not invoked

  Scenario: No valid completion
    Given a valid 4x4 grid with exactly two zeros
    And attempt A and attempt B are not magic squares
    When the boundary receives the grid
    Then the response code is "E_NO_SOLUTION"
    And the message is "ERROR: No valid magic square completion exists."
```

### 23.4 RED Test-ID 후보 (Report/02)

| Track | IDs |
|-------|-----|
| Domain | D-T01, D-T02, D-T03, D-T04, D-T05, D-T10~D-T16 |
| Boundary | U-T01~U-T08 |
| Integration | IT-01, IT-02, IT-03, IT-F01~IT-F05 |

### 23.5 문서 이력

| 버전 | 일자 | 변경 |
|------|------|------|
| 1.0 | 2026-05-28 | 구현 전 PRD 초안 (Report/01·02·03·mdc 기반; Report/4 부재 DN-01) |
