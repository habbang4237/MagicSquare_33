# MagicSquare_xx — 결함 목록 (Defect List)

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare 4×4, Dual-Track ECB TDD |
| **현재 슬라이스** | AC-FR-01-01 (FR-01 크기 검증) |
| **권위 테스트** | `tests/boundary/test_input_contract_ac_fr_01_01.py` |
| **최종 갱신** | 2026-05-29 |
| **기준 실행** | `python -m pytest tests/boundary/test_input_contract_ac_fr_01_01.py tests/entity/test_user.py -v --tb=short` |

## 심각도 정의

| Severity | 의미 |
|----------|------|
| **Critical** | Input 검증 실패 시 크래시, 또는 계약 위반 시 `SolvePuzzleUseCase` 호출 |
| **Major** | `code`/`message`가 테스트·슬라이스 계약 또는 PRD §13과 불일치 |
| **Minor** | 반환 타입·도구 설정 등 부수적 불일치 (기능 핵심은 통과 가능) |
| **Info** | 의도된 RED(미구현), 문서·도구 설정, 추적용 스펙 갭 |

## 상태 범례

| Status | 설명 |
|--------|------|
| **Open** | 미수정 |
| **Resolved** | 수정·검증 완료 |

---

## Open 결함

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 | Status |
|----|----------|-------|-----------|--------|--------|-----------|-----------|--------|
| DEF-001 | Info | AC-FR-01-01 | `Set-Location` 프로젝트 루트 → `python -m pytest tests/boundary/test_input_contract_ac_fr_01_01.py -v` | 8 tests collected; `grid=None` 시 `ErrorResponse(code="INVALID_SIZE", message="Grid must be 4x4.")`; `execute`/`resolve` 0회 | `ModuleNotFoundError: No module named 'boundary'` (collection ERROR, `test_input_contract_ac_fr_01_01.py:9`) | `src/boundary/` 패키지 미구현 (`error_response`, `input_contract_validator`, `puzzle_boundary` 없음) | `src/boundary/` 최소 GREEN 스켈레톤 추가; `InputContractValidator`·`PuzzleBoundary.receive`에서 크기 실패만 처리 | Open |
| DEF-002 | Info | — | `python -m pytest tests/entity/ --cov=src/entity --cov-report=term-missing` | entity 레이어 커버리지 리포트 생성 | `CoverageWarning: Module src/entity was never imported`; `No data was collected` | `--cov` 대상이 실제 import 경로(`entity.*`)와 불일치 (`src/entity` 디렉터리 ≠ 패키지명) | 문서·로컬 명령을 `--cov=entity` 또는 `--cov=src/entity`(파일 경로)로 통일; `docs/test_plan.md` §8 예시 준수 | Open |
| DEF-003 | Major | AC-FR-01-01 | 테스트·PRD §13·`docs/test_plan.md` §2.2 대조 | 단일 고정 계약 (코드·메시지 1쌍) | 테스트: `INVALID_SIZE` / `Grid must be 4x4.` — PRD §13·test_plan: `E_SIZE` / `ERROR: Grid must be 4x4.` | 슬라이스 테스트와 normative PRD 간 명칭·UX-3 문구 이중 정의 | **(A)** 본 슬라이스 GREEN은 테스트 계약 우선 구현 후 **(B)** 별도 RED로 PRD 정합 또는 테스트/PRD 중 하나를 권위로 확정 | Open |
| DEF-004 | Info | AC-FR-01-01 | DEF-001과 동일 pytest 실행; traceback `test_input_contract_ac_fr_01_01.py:12` | `SolvePuzzleUseCase` import 가능 (Mock `spec`용) | `ModuleNotFoundError: No module named 'control'` (boundary 수집 실패로 12행까지 미도달이나, 동일 루트 원인) | `src/control/solve_puzzle_use_case.py` 미구현 | `SolvePuzzleUseCase` 최소 스텁(`execute`, `resolve` 시그니처만); Domain 로직·resolve 본구현 금지 | Open |

> **Note:** DEF-001·DEF-004는 동일 GREEN 배치로 함께 해소 가능. 수집 단계에서는 boundary import가 먼저 실패한다.

---

## Resolved 결함

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 | Status |
|----|----------|-------|-----------|--------|--------|-----------|-----------|--------|
| DEF-R01 | Minor | — | `from magicsquare.entity.user import User` 또는 `--cov=magicsquare.entity` | `entity` 패키지 import·커버리지 | `ModuleNotFoundError` / 경로 불일치 | `src/magicsquare/entity` 중첩 구조와 테스트 import 불일치 | `src/entity/` 평탄화 및 전역 import `entity.*`로 변경 (2026-05-29) | Resolved |

---

## 슬라이스 범위 외 (선제 구현 금지)

다음은 AC-FR-01-01 GREEN 시 **결함으로 기록하지 않음** (Out-of-Scope):

- AC-FR-01-02~05 (`INVALID_EMPTY_COUNT`, `INVALID_RANGE`, `INVALID_DUPLICATE` 등)
- `PuzzleSolver`, `MagicSquareValidator`, entity/control 본격 구현
- `grid=None` 이외 성공 경로의 `execute` 반환값 검증

---

## 회귀 확인 체크리스트

DEF-001·DEF-004 해소 후:

```powershell
Set-Location "c:\Users\usejen_id\Desktop\커서ai교육\dev\MagicSquare_xx"
python -m pytest tests/boundary/test_input_contract_ac_fr_01_01.py -v --tb=short
python -m pytest tests/entity/test_user.py -v --tb=short
```

| 확인 항목 | 명령/기준 |
|-----------|-----------|
| Boundary AC-FR-01-01 | 8 passed |
| Entity (기존 GREEN) | 13 passed |
| UseCase 미호출 | `test_none_grid_resolve_zero_calls` 통과 |
| 커버리지 (entity) | `python -m pytest tests/entity/ --cov=entity --cov-report=term-missing` |

---

## 변경 이력

| 날짜 | 변경 |
|------|------|
| 2026-05-29 | 초안 작성 (DEF-001~004 Open, DEF-R01 Resolved) |
