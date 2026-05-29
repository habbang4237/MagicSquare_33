# MagicSquare 4x4 TDD Practice

## 1. Project Start Declaration

**MagicSquare 4×4 TDD Practice**는 4×4 마방진 퍼즐(빈칸 2개)에 대해 **고정된 입출력 계약**을 만족하는 해를 반환하는 순수 로직 시스템을 **Dual-Track UI + Logic TDD**와 **ECB(Clean Architecture)** 로 구축하는 학습 프로젝트의 **공식 시작 선언**입니다.

현재 단계는 **PRD 기반 TDD 시작 준비 단계**입니다. 요구사항·계약·불변식·Test-ID 추적 구조를 고정한 뒤, 구현 코드 없이 **Test Skeleton 작성 → pytest 실행 → 실패 확인** 순으로 RED에 진입합니다.

**RED**는 “실패하는 테스트를 작성하고, pytest로 **실패 상태를 확인하는 단계**”입니다. 테스트가 통과하면 RED가 아니며, GREEN(최소 구현)은 RED 실패 확인 **이후에만** 시작합니다.

본 README는 구현 전에 **개발 방향·추적 구조·품질 게이트**를 고정하는 문서입니다. 여기에 정의된 Scenario → Acceptance Criteria → RED Test ID → Test Skeleton → Expected RED Failure → GREEN Task Candidate → REFACTOR Candidate 흐름을 따라 코드를 작성합니다.

---

## 2. PRD Summary

| 항목 | 내용 |
|------|------|
| **프로젝트 목적** | 알고리즘 난이도 훈련이 아니라, **계약·불변식·레이어 분리·TDD 추적성**을 하나의 4×4 퍼즐 해결 흐름으로 고정 |
| **학습 목표** | (1) 불변식·비즈니스 규칙 명시화, (2) Boundary/Domain 입출력 계약 고정, (3) Track A(계약)·Track B(불변식) 분리 TDD, (4) RED→GREEN→REFACTOR와 Concept→Test→Component 추적 |
| **마방 상수** | `M = 34` (1~16 완전 배치 시 행·열·주대각·부대각 합) |

### 핵심 도메인 규칙

- 입력은 **4×4 `int` 행렬** (`int[4][4]`)입니다.
- `0`은 **빈칸**이며, 빈칸은 **정확히 2개**입니다.
- 셀 값은 **`0` 또는 `1~16`** 입니다.
- `0`을 제외한 값은 **중복 불가**합니다.
- **1번 빈칸**은 row-major(행 우선) 스캔에서 **처음 발견되는 `0`** 의 1-index 좌표입니다.
- **2번 빈칸**은 row-major 스캔에서 **두 번째 `0`** 의 1-index 좌표입니다.
- **누락 숫자** `m1`, `m2`는 `{1..16} \ 비零 값`에서 유도하며 **`m1 < m2`** 입니다.
- **시도 A (small-first):** 1번 빈칸←`m1`, 2번 빈칸←`m2` → 마방진이면 `[r1,c1,m1,r2,c2,m2]` 반환.
- **시도 B (reverse):** A 실패 시 1번←`m2`, 2번←`m1` → 마방진이면 `[r1,c1,m2,r2,c2,m1]` 반환.
- A·B **모두 실패** 시 `NO_VALID_COMPLETION` → Boundary `E_NO_SOLUTION`.
- A·B **모두 성공** 시 **A 결과 우선** (결정성 I-D12).

### 입력 계약

| 항목 | 규칙 | 위반 코드 |
|------|------|-----------|
| `grid` | 4행×4열 `int[4][4]` | `E_SIZE` |
| `grid[r][c]` | `0` 또는 `1..16` | `E_RANGE` |
| empty count | `count(0) == 2` | `E_EMPTY_COUNT` |
| uniqueness | 비零 값 중복 없음 | `E_DUPLICATE` |
| 내부 인덱스 | Boundary 내부 0-index | — |
| 호출자 배열 | 시스템이 입력 배열 원소를 **변경하지 않음** | — |

### 출력 계약

| 항목 | 규칙 |
|------|------|
| 형식 | `int[6] = [r1, c1, n1, r2, c2, n2]` |
| 좌표 | `r*`, `c*`는 **1-index** (`1..4`) |
| 숫자 | `n*`는 `1..16`; `n1`→1번 빈칸, `n2`→2번 빈칸 |
| 길이 | 정확히 **6** |
| 제약 | `(r1,c1)≠(r2,c2)`, `{n1,n2}` = 누락 수 집합, 좌표가 입력 `0` 위치와 일치 |
| 성공 반환 | `int[6]` 단독 (래퍼 없음) |
| 실패 반환 | `ErrorResponse { code, message }` (고정 메시지, UX-3) |

### 성공 기준

1. 유효 퍼즐 입력 시 계약된 `int[6]` 반환.
2. 완성 격자는 **`MagicSquareValidator` 통과(I-D2~I-D7, M=34)와 동치** (I-10).
3. 잘못된 입력은 **Domain `solve` 호출 없이** Boundary에서 즉시 거절 (Track A).
4. §16 Normal·Exception 시나리오 전부 통과, §14 커버리지 충족, Concept→Test→Component 추적 100%.

---

## 3. TDD Development Flow

```
Scenario
  → Acceptance Criteria
  → RED Test ID
  → Test Skeleton
  → Run Test
  → Confirm Failure = RED
  → Minimal Implementation = GREEN
  → Structure Improvement = REFACTOR
```

| 단계 | 의미 |
|------|------|
| **Scenario** | 호출자·레이어 관점에서 관측 가능한 행동을 한 문장으로 정의합니다. |
| **Acceptance Criteria** | Scenario를 **테스트 가능한 검증 문장**으로 분해합니다. |
| **RED Test ID** | AC를 `U-T*`(Boundary) 또는 `D-T*`(Domain)로 고유 식별합니다. |
| **Test Skeleton** | AAA(Arrange-Act-Assert) 구조의 **실패할 테스트 골격**을 작성합니다 (prod 코드 없음). |
| **Run Test** | `pytest`로 대상 Test-ID 테스트를 실행합니다. |
| **Confirm Failure = RED** | **의도한 실패 유형**(ImportError, AssertionError, `ErrorResponse` 코드 불일치 등)이 발생함을 확인합니다. RED는 “실패 확인”까지입니다. |
| **Minimal Implementation = GREEN** | RED 실패를 **통과시키기 위한 최소 구현 작업 후보**만 수행합니다. |
| **Structure Improvement = REFACTOR** | GREEN 확인 **후** 구조 개선 후보만 검토합니다. 공개 계약·`E_*` 메시지·`int[6]` 의미는 변경하지 않습니다. |

---

## 4. Development Methodology

### Dual-Track UI + Logic TDD

| Track | 범위 | Mock 정책 | 테스트 경로 |
|-------|------|-----------|-------------|
| **Track A — Boundary/UI** | 입력·출력 계약, 고정 에러 메시지, Domain 호출 순서 | Domain/Application **Mock 필수** | `tests/boundary/` |
| **Track B — Domain/Logic** | `Grid`, 불변식(I-D*), UC-D4 해 결정 | **Mock 금지** (실제 객체) | `tests/entity/` |

두 트랙은 **독립 RED→GREEN→REFACTOR** 를 유지합니다. 통합 테스트(`tests/integration/`, IT-*)는 **두 트랙 모두 GREEN 이후**에 추가합니다.

### Boundary RED와 Logic RED의 분리

- **Boundary RED:** “계약 위반 시 고정 `ErrorResponse` 반환 + Domain 미호출”을 검증합니다.
- **Logic RED:** “유효 `Grid`에 대해 불변식·해 결정 규칙”을 Mock 없이 검증합니다.
- Boundary 테스트에서 `PuzzleSolver`·`MagicSquareValidator` **직접 호출 금지** — `SolvePuzzleUseCase` 경유.

### ECB 역할 분리

- **Entity:** Board 상태(`Grid`)와 순수 도메인 규칙.
- **Control:** 검증·해 결정 흐름 오케스트레이션.
- **Boundary:** 입력 검증, 출력 형식, 오류 정책 — **Domain Invariant를 직접 구현하지 않음**.

### Concept-to-Code Traceability

Scenario → AC → RED Test ID → Test Skeleton → Expected RED Failure → GREEN Task → REFACTOR Candidate → ECB Layer → Code Target을 **§6 Tracking Board**에서 1:1 추적합니다.

### RED → GREEN → REFACTOR 원칙

| Phase | 허용 | 금지 |
|-------|------|------|
| **RED** | 테스트 선행, pytest FAIL 확인 | prod 코드 선행, assertion 완화·skip·xfail |
| **GREEN** | 현재 FAIL 테스트 통과에 필요한 **최소** 코드 | REFACTOR, RED 범위 밖 기능, `print()` 디버그 |
| **REFACTOR** | 구조 개선, 커버리지 유지 | 공개 계약·에러 메시지 변경, 테스트 없이 대량 변경 |

---

## 5. ECB Role Separation

| ECB Layer | Responsibility | Example Component |
| --------- | -------------- | ----------------- |
| **Entity** | 4×4 Board 상태(`Grid`)와 순수 도메인 규칙·불변식(I-D1~I-D12)을 표현한다. UI·DB·Web·파일 시스템·고정 Boundary 에러 문구에 **의존하지 않는다**. | `Grid`, `CellPosition`, `MagicConstant`, `EmptyCellLocator`, `MissingNumberFinder`, `MagicSquareValidator`, `PuzzleSolver`, `SolutionVector`, `DomainError` |
| **Control** | 입력을 `Grid`로 변환하고, 빈칸 탐색→누락 수 계산→A/B 시도→판정 흐름(UC-D4)을 **조정**한다. `DomainError`를 Boundary `ErrorResponse`로 **매핑**한다. 행·열·대각 합 등 순수 규칙을 직접 구현하지 않는다. | `SolvePuzzleUseCase` |
| **Boundary** | 외부 입출력 계약(`int[4][4]`/`int[6]`), 고정 `ErrorResponse`, Domain 호출 **위임**을 담당한다. **Domain Invariant(마방진 판정·해 탐색)를 직접 구현하지 않는다**. | `PuzzleBoundary`, `InputContractValidator`, `OutputContractValidator`, `ErrorMessages` |

**의존 방향:** `boundary → control → entity` (역방향·레이어 우회 금지)

---

## 6. Scenario → AC → RED → GREEN Tracking Board

> **Status 범례:** `Planned` = RED 준비 완료, Test Skeleton·실행 대기  
> **RED 확인 명령 예시:** `pytest tests/boundary/test_input_contract.py::test_u_t01 -v` (Track A) / `pytest tests/entity/test_magic_square_validator.py::test_d_t04_r -v` (Track B)

| Status | Scenario ID | Scenario Summary | Acceptance Criteria | RED Test ID | Test Skeleton Candidate | Expected RED Failure | GREEN Task Candidate | REFACTOR Candidate | ECB Layer | Code Target |
| ------ | ----------- | ---------------- | ------------------- | ----------- | ----------------------- | -------------------- | -------------------- | ------------------ | --------- | ----------- |
| Planned | SC-B01 | **None 입력** — 호출자가 `grid=None`을 제출한다 | AC-B01-1: `None` 입력 시 `ErrorResponse` 반환. AC-B01-2: `code=E_SIZE`. AC-B01-3: Domain `solve` **0회** 호출 | U-T00 | `tests/boundary/test_input_contract.py::test_u_t00_none_grid` — Arrange: `grid=None`; Act: `PuzzleBoundary.receive(grid)`; Assert: `ErrorResponse.code=="E_SIZE"`, Mock solve 호출 0 | `ModuleNotFoundError` / `ImportError` (Boundary 미구현) 또는 `AttributeError`; GREEN 전에는 `E_SIZE` 미반환 | `InputContractValidator`에 `None`/비배열 거부 분기 추가 → `E_SIZE` 반환; Domain 호출 경로 차단 | `InvalidInputGuard` VO로 null·타입 검증 공통화 | Boundary | `InputContractValidator`, `PuzzleBoundary` |
| Planned | SC-B02 | **4×4가 아닌 입력** — 3×3 등 크기 불일치 | AC-B02-1: 3×4 격자 제출 시 `code=E_SIZE`, message=`ERROR: Grid must be 4x4.` AC-B02-2: Domain `solve` 0회 | U-T01 | `tests/boundary/test_input_contract.py::test_u_t01_invalid_size` — Arrange: 3×4 `grid`; Act/Assert: `E_SIZE`, message byte-equal, Mock 0회 | ImportError 또는 AssertionError (`E_SIZE` 미반환) | 행·열 수 검사 최소 구현 → `E_SIZE` + 고정 메시지 | `GridSize` VO로 4×4 상수 단일화 | Boundary | `InputContractValidator` |
| Planned | SC-B03 | **빈칸 개수 오류** — `0`이 1개 또는 3개 | AC-B03-1: 빈칸 1개 시 `E_EMPTY_COUNT`. AC-B03-2: message 고정. AC-B03-3: Domain 미호출 | U-T02 | `tests/boundary/test_input_contract.py::test_u_t02_empty_count` — Arrange: 4×4, `count(0)==1`; Assert: `E_EMPTY_COUNT`, Mock 0회 | AssertionError (`E_EMPTY_COUNT` 미반환) | `count(0)` 검사 → `E_EMPTY_COUNT` | 빈칸 카운트를 `EmptyCountRule` 헬퍼로 추출 | Boundary | `InputContractValidator` |
| Planned | SC-B04 | **값 범위 오류** — `-1`, `17` 등 | AC-B04-1: 범위 밖 값 시 `E_RANGE`. AC-B04-2: message=`ERROR: Cell value must be 0 or between 1 and 16.` AC-B04-3: Domain 미호출 | U-T03 | `tests/boundary/test_input_contract.py::test_u_t03_invalid_range` — Arrange: 한 셀 `17`; Assert: `E_RANGE`, Mock 0회 | AssertionError | 셀 값 `{0}∪[1,16]` 검사 → `E_RANGE` | `CellValue` 경계 검증과 Boundary 검사 역할 분리 문서화 | Boundary | `InputContractValidator` |
| Planned | SC-B05 | **중복 숫자 오류** — 비零 값 중복 | AC-B05-1: 두 셀 동일 비零 값 시 `E_DUPLICATE`. AC-B05-2: message 고정. AC-B05-3: Domain 미호출 | U-T04 | `tests/boundary/test_input_contract.py::test_u_t04_duplicate` — Arrange: `5` 중복; Assert: `E_DUPLICATE`, Mock 0회 | AssertionError | 비零 집합 크기 검사 → `E_DUPLICATE` | 중복 검사를 `UniquenessRule`로 분리 | Boundary | `InputContractValidator` |
| Planned | SC-D01 | **빈칸 좌표 row-major 탐색** | AC-D01-1: (2,3),(3,1)에 `0`인 격자에서 1번=(2,3), 2번=(3,1) (1-index). AC-D01-2: `EmptySlotPair` 순서 고정 | D-T03 | `tests/entity/test_empty_cell_locator.py::test_d_t03_row_major_order` — Arrange: I-D8·I-D9 만족 격자; Act: `EmptyCellLocator.locate(grid)`; Assert: `(2,3)`, `(3,1)` | ImportError / `EmptyCellLocator` 미존재 또는 좌표 불일치 AssertionError | row-major 이중 루프로 첫·둘째 `0` 탐색 → `EmptySlotPair` 반환 | `CellPosition` VO로 1-index 캡슐화 | Entity | `EmptyCellLocator`, `EmptySlotPair` |
| Planned | SC-D02 | **누락 숫자 오름차순 탐색** | AC-D02-1: 14개 비零에서 `{1..16}\values` 크기 2. AC-D02-2: `m1 < m2` 보장. AC-D02-3: 기대 `(m1,m2)` 일치 | D-T05 | `tests/entity/test_missing_number_finder.py::test_d_t05_missing_pair_sorted` — Arrange: 고정 14칸 픽스처; Assert: `MissingPair(m1,m2)`, `m1<m2` | ImportError 또는 `(m1,m2)` 불일치 | 집합 차·정렬 → `MissingPair(m1,m2)` | `MissingPair` frozen VO + 팩토리 | Entity | `MissingNumberFinder`, `MissingPair` |
| Planned | SC-D03 | **모든 행 합 34 검증** | AC-D03-1: 완전 격자 4행 각 합 = `M(34)`이면 해당 검사 통과. AC-D03-2: 한 행이라도 ≠34이면 `false` | D-T04-R | `tests/entity/test_magic_square_validator.py::test_d_t04_row_sums` — Arrange: 행 합만 깨진/유효 완성 격자; Assert: `isValid` true/false | ImportError 또는 행 합 검사 미구현 AssertionError | 4행 합 == `MagicConstant.M` 비교 최소 구현 | `LineSumChecker` 추출 (행 전용 → 전체 선) | Entity | `MagicSquareValidator` |
| Planned | SC-D04 | **모든 열 합 34 검증** | AC-D04-1: 완전 격자 4열 각 합 = 34이면 통과. AC-D04-2: 한 열이라도 ≠34이면 `false` | D-T04-C | `tests/entity/test_magic_square_validator.py::test_d_t04_col_sums` — Arrange: 열 합 깨진/유효 격자; Assert: `isValid` | AssertionError (열 합 미검사) | 4열 합 == M 검사 추가 | 행·열 공통 `sum_line` 유틸 | Entity | `MagicSquareValidator` |
| Planned | SC-D05 | **두 대각선 합 34 검증** | AC-D05-1: 주대각·부대각 합 각각 34. AC-D05-2: 대각 하나라도 ≠34이면 `false` | D-T04-D | `tests/entity/test_magic_square_validator.py::test_d_t04_diagonal_sums` — Arrange: 대각 깨진/유효 격자; Assert: `isValid` | AssertionError | 주대각 `(0,0)~(3,3)`, 부대각 `(0,3)~(3,0)` 합 검사 | `DiagonalSumChecker` 분리 | Entity | `MagicSquareValidator` |
| Planned | SC-D06 | **small-first 성공** — 시도 A만 마방진 | AC-D06-1: A 배치 후 `isValid==true`. AC-D06-2: 반환 `[r1,c1,m1,r2,c2,m2]`. AC-D06-3: I-D11 좌표 일치 | D-T01 | `tests/entity/test_puzzle_solver.py::test_d_t01_small_first_success` — Arrange: A-only 유효 퍼즐; Act: `PuzzleSolver.solve(grid)`; Assert: 벡터·validator true | ImportError / `NO_VALID_COMPLETION` 또는 벡터 불일치 | UC-D4 A 경로: `m1→slot1`, `m2→slot2` → validator → `SolutionVector` | `AttemptStrategy.A` / `AttemptStrategy.B` enum 분리 | Entity | `PuzzleSolver` |
| Planned | SC-D07 | **small-first 실패 후 reverse 성공** | AC-D07-1: A `false`, B `true`. AC-D07-2: 반환 `[r1,c1,m2,r2,c2,m1]` | D-T02 | `tests/entity/test_puzzle_solver.py::test_d_t02_reverse_only_success` — Arrange: B-only 픽스처; Assert: reverse 벡터 | AssertionError (A 결과 반환 또는 실패) | A 실패 시 B 시도 분기 → reverse 벡터 | 시도 A/B를 `CompletionAttempt` 객체로 캡슐화 | Entity | `PuzzleSolver` |
| Planned | SC-D08 | **두 조합 모두 실패** | AC-D08-1: A·B 모두 `isValid==false`. AC-D08-2: `DomainError(NO_VALID_COMPLETION)`. AC-D08-3: Boundary 매핑 `E_NO_SOLUTION` (Track A U-T06) | D-T13 | `tests/entity/test_puzzle_solver.py::test_d_t13_no_valid_completion` — Arrange: A·B 모두 무효 퍼즐; Assert: `NO_VALID_COMPLETION` | AssertionError 또는 예외 타입 불일치 | A·B 모두 false → `DomainError` raise | Control `SolvePuzzleUseCase`에서 Domain→Boundary 에러 매핑 | Entity (+ Control 매핑) | `PuzzleSolver`, `SolvePuzzleUseCase` |
| Planned | SC-B06 | **결과 배열 길이 6** | AC-B06-1: 유효 입력 성공 시 `len(result)==6`. AC-B06-2: Domain `solve` 정확히 1회 호출 | U-T05 | `tests/boundary/test_output_contract.py::test_u_t05_result_length_six` — Arrange: 유효 grid + Mock `[1,2,3,4,5,6]`; Assert: len==6, Mock 1회 | ImportError / len≠6 AssertionError | Boundary 성공 경로에서 `int[6]` 그대로 반환 | `SolutionVector.toArray()`와 Boundary 반환 계약 정렬 | Boundary | `PuzzleBoundary`, `OutputContractValidator` |
| Planned | SC-B07 | **반환 좌표 1-index** | AC-B07-1: `r1,c1,r2,c2 ∈ [1,4]`. AC-B07-2: 0-index 좌표(`0` 또는 `5`) 반환 시 `E_OUTPUT_FORMAT`. AC-B07-3: Mock 잘못된 벡터로 출력 검증 | U-T07 | `tests/boundary/test_output_contract.py::test_u_t07_one_index_coordinates` — Arrange: Mock `r1=0`; Assert: `E_OUTPUT_FORMAT` | AssertionError (`E_OUTPUT_FORMAT` 미반환) | `OutputContractValidator`: 좌표 1..4, 값 1..16, 길이 6 검사 | 출력 검증 규칙을 `OutputContractRules` 테이블로 상수화 | Boundary | `OutputContractValidator` |

---

## 7. RED Start Checklist

RED 착수 전 아래 항목을 모두 확인합니다.

- [ ] 모든 Scenario가 정의되었는가?
- [ ] 모든 Acceptance Criteria가 **테스트 가능한 문장**인가?
- [ ] 모든 Scenario에 RED Test ID가 부여되었는가?
- [ ] 모든 RED Test ID에 Test Skeleton **후보**가 있는가?
- [ ] 각 RED 항목에 **Expected RED Failure**가 명시되었는가?
- [ ] 각 RED 실패에 대응하는 **GREEN Task 후보**가 있는가?
- [ ] Boundary RED(`U-T*`)와 Logic RED(`D-T*`)가 **분리**되었는가?
- [ ] ECB Layer가 명확히 지정되었는가?
- [ ] **아직 구현 코드를 작성하지 않았는가?**
- [ ] **아직 테스트 코드를 작성하지 않았는가?**
- [ ] **아직 REFACTOR를 수행하지 않았는가?**

---

## RED 단계 To-Do 리스트

> 이 체크리스트는 test_plan.md 기반으로 생성되었습니다.
> 각 항목은 RED(실패 테스트 작성) 완료 시 체크합니다.

### Golden Master 회귀 안전장치

> Refactoring 시작 전 구축. GREEN 완료 후 즉시 적용.

**기준 파일 생성**

- [x] GM-01: `golden_master_expected.txt` 생성
- [x] GM-02: 정상/역순/오류 시나리오 추가
- [x] GM-03: `git add tests/golden_master_expected.txt`

**테스트 코드**

- [x] GM-04: `test_golden_master_magic_square` 작성
- [x] GM-05: approve 패턴 적용
- [x] GM-06: Golden Master 테스트 PASS 확인

**회귀 보호**

- [x] GM-07: row-major 규칙 보호
- [x] GM-08: 1-index 출력 보호
- [x] GM-09: reverse 조합 fallback 보호
- [x] GM-10: Error Contract 보호

```bash
pytest -m golden_master -v
pytest -m golden_master --approve-golden-master -v   # 기준 갱신
```

기준 파일: `tests/golden_master_expected.txt` · 설계: [docs/golden_master_approve_design.md](docs/golden_master_approve_design.md)

### Track A — UI / Boundary 테스트
- [ ] TC-A-01: grid=None 입력 → 실패 결과 반환 (Happy Path of Failure)
- [ ] TC-A-02: code가 정확히 "INVALID_SIZE" 문자열인지 검증
- [ ] TC-A-03: message가 "Grid must be 4x4." 와 문자 단위 동일한지 검증
- [ ] TC-A-04: grid=None 시 Domain 진입점 0회 호출 (mock/spy 검증)
- [ ] TC-A-05: grid=[] 빈 리스트 → 실패 결과 반환
- [ ] TC-A-06: grid=3×4 크기 불일치 → 실패 결과 반환
- [ ] TC-A-07: 반환 객체 타입이 지정 실패 결과 구조체인지 검증

### Track B — Domain / Logic 테스트
- [ ] TC-B-01: resolve()가 None grid를 직접 받지 않음을 격리 검증
- [ ] TC-B-02: Boundary가 None 분기를 처리 후 resolve() 미호출 확인
- [ ] TC-B-03: resolve() mock이 호출됐을 경우 테스트 실패 처리
- [ ] TC-B-04: AC-FR-01-02~05 범위의 케이스는 이 커밋에 포함하지 않음 확인

### 커버리지 목표
- [ ] Domain Logic: 95%+ (pip install pytest-cov)
- [ ] Boundary Layer: 85%+
- [ ] 전체 TOTAL: 90%+

### 결함 목록 연결
- [x] defect_list.md 생성 및 발견 결함 기록
- [ ] 모든 결함 수정 후 회귀 테스트 통과 확인 ([defect_list.md](defect_list.md) Open: DEF-001~004)

---

## 8. Project Layout

소스는 `src/` 아래 ECB 레이어 패키지로 분리합니다 (`pythonpath = ["src"]`).

```
src/
├── boundary/   # 입출력 계약, ErrorResponse, 검증기
├── control/    # Use Case, 오케스트레이션
├── entity/     # Grid, VO, Domain Services
└── data/       # (선택) MatrixRepository
tests/
├── boundary/   # UI Track (Domain Mock)
├── control/
├── entity/     # Domain Track (Mock 금지)
└── integration/
```

**import 예:** `from entity.user import User`, `from boundary.puzzle_boundary import PuzzleBoundary`

**커버리지 예:**

```bash
python -m pytest tests/entity/ --cov=entity --cov-report=term-missing
python -m pytest tests/boundary/ --cov=boundary --cov-branch --cov-report=term-missing
```

---

## 9. Quality Gates

| Gate | 기준 | 검증 |
|------|------|------|
| Domain Logic coverage | **branch ≥ 95%** (`EmptyCellLocator`, `MissingNumberFinder`, `MagicSquareValidator`, `PuzzleSolver`) | pytest-cov |
| Boundary Validation coverage | **branch ≥ 85%** (입력·출력·에러 매핑 분기) | pytest-cov |
| 전역 coverage | line/branch **≥ 80%** | pytest-cov |
| 테스트 프레임워크 | **pytest** (`pyproject.toml`: `testpaths=["tests"]`, `pythonpath=["src"]`) | CI / 로컬 |
| 테스트 구조 | **AAA** (Arrange-Act-Assert) | 코드 리뷰 |
| 테스트 약화 | assertion 삭제·완화·`skip`·`xfail`로 통과 **금지** | PR / `.mdc` forbidden |
| 디버그 출력 | `print()` 및 stdout/stderr 디버그 **금지** | capsys / 리뷰 |
| Magic number | `34`, `4`, `16`, 고정 에러 문구 리터럴 산재 **금지** — `MagicConstant`, `GridSize`, `ErrorMessages` 등 | 코드 리뷰 |
| 타입·스타일 | **type hints 필수**, **PEP8**, Black line-length 88 | ruff/black |
| 계약 불변 | **입력/출력 계약 변경 금지** (변경 시 Major + Traceability 전체 갱신, REG-2) | PRD §12, §21 |
| ECB | `boundary → control → entity` 위반 **금지** | `.cursor/rules/magicsquare-ecb-architecture.mdc` |
| 에러 메시지 | UX-3 **바이트 일치** (U-T08 회귀) | Boundary 테스트 |

---

## 10. Reference Documents

| 문서 | 역할 |
|------|------|
| [docs/PRD_MagicSquare.md](docs/PRD_MagicSquare.md) | **Normative PRD** — FR·BR·입출력 계약·에러 정책·Dual-Track·Test Plan·커버리지·Traceability 1차 기준 |
| [Report/01.문제정의_보고서.md](Report/01.문제정의_보고서.md) | Why Chain·진짜 문제 정의·학습 맥락 — “완성”이 아닌 “규칙·계약·검증” 관점 확립 |
| [Report/02.DualTrack_CleanArch_TDD_설계.md](Report/02.DualTrack_CleanArch_TDD_설계.md) | ECB 설계·I-D* Invariant·UC-D*·U-T*/D-T* Test-ID·UI/Domain 계약·통합 시나리오 |
| [Report/03.CursorRules_UserEntity_구현보고서.md](Report/03.CursorRules_UserEntity_구현보고서.md) | 개발 환경·Cursor Rules·pytest 설정·ECB Entity Track 실습(`User` 보조) — 본 퍼즐 FR 범위 외 참고 |
| [Report/04.ProjectRules_MDC_Migration_구현보고서.md](Report/04.ProjectRules_MDC_Migration_구현보고서.md) | `.cursor/rules/*.mdc` 분리·프로젝트 규칙 마이그레이션 기록 |
| [Report/07.README_TDD_시작_구현보고서.md](Report/07.README_TDD_시작_구현보고서.md) | README TDD 시작 가이드 작성·적용·Tracking Board 고정 기록 |
| [Report/08.QA_Defect_Structure_구현보고서.md](Report/08.QA_Defect_Structure_구현보고서.md) | 커버리지 진단·`src/` 구조 평탄화·AC-FR-01-01 QA·`defect_list.md` |
| `.cursorrules` | **Deprecated** — 규칙은 `.cursor/rules/*.mdc`로 이전됨을 안내 |
| `.cursor/rules/magicsquare-project.mdc` | 프로젝트 고정 계약·디렉터리·AI 작업 순서·경고 블록 정책 |
| `.cursor/rules/magicsquare-tdd-testing.mdc` | Dual-Track RED/GREEN/REFACTOR·pytest·AAA·커버리지·Mock 정책 |
| `.cursor/rules/magicsquare-ecb-architecture.mdc` | ECB 레이어 책임·의존 방향·Boundary→Control→Entity |
| `.cursor/rules/magicsquare-python-code-style.mdc` | Python 3.12+·type hints·PEP8·Black |
| `.cursor/rules/magicsquare-forbidden.mdc` | `print()`·magic number·광포 catch·RED 없는 prod·테스트 약화·레이어 우회 금지 |

---

## 11. Current Project Status

| 항목 | 상태 |
|------|------|
| **현재 단계** | PRD 기반 TDD 시작 준비 |
| **구현** | MagicSquare 퍼즐 핵심(`Grid`, `PuzzleSolver`, Boundary 등) **아직 미착수** |
| **테스트** | §6 Tracking Board의 U-T*/D-T* Test Skeleton **아직 미작성** |
| **REFACTOR** | **미수행** (GREEN 이후 후보만 §6에 기록) |
| **다음 단계** | ① §6에서 Track A(`U-T00`~`U-T07`) 또는 Track B(`D-T03`~`D-T05`) Test Skeleton 작성 → ② `pytest` 실행 → ③ **Expected RED Failure 확인(RED)** → ④ 해당 GREEN Task Candidate로 최소 구현 |

**RED 시작 권장 순서 (병렬 가능):**

```
Track A: U-T00 → U-T01 → U-T02 → U-T03 → U-T04  (Boundary 입력 계약)
Track B: D-T04-R → D-T04-C → D-T04-D → D-T03 → D-T05 → D-T01 → D-T02 → D-T13
통합:    Track A·B GREEN 후 U-T05, U-T07, IT-01
```

---

> **선언:** 본 README 작성 시점 기준, MagicSquare 4×4 퍼즐의 **prod 코드·test 코드는 의도적으로 비어 있습니다.**  
> 첫 커밋 대상은 §6 Tracking Board의 **Test Skeleton**이며, pytest **FAIL 확인 = RED**가 완료된 뒤에만 §6의 GREEN Task Candidate를 구현합니다.
