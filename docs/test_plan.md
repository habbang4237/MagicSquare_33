# Test Plan — FR-01 Input Size Validation (AC-FR-01-01)

| 항목 | 내용 |
|------|------|
| **문서 ID** | TP-MSQ-FR01-SIZE-001 |
| **버전** | 1.0 |
| **작성 기준일** | 2026-05-29 |
| **앵커 AC** | AC-FR-01-01 (`grid=None` → 크기 검증 실패) |
| **관련 PRD** | FR-01, §12.1 Input Contract, §13 Error Policy, AC-FR01-5 |
| **권위 출처** | `docs/PRD_MagicSquare.md`, `Report/02.DualTrack_CleanArch_TDD_설계.md`, `.cursor/rules/magicsquare-tdd-testing.mdc` |

---

## 1. 목적 및 범위

본 테스트 계획서는 **FR-01 Input Verification** 중 **격자 구조(4×4) 검증(BR-01)** 슬라이스를 대상으로 한다. 앵커 시나리오는 **AC-FR-01-01: `grid=None` 제출 시 크기 위반으로 즉시 거절**이며, Boundary는 Domain 해 결정 진입점을 **호출하지 않아야** 한다(AC-FR01-5).

### 1.1 In-Scope

| 구분 | 대상 | 레이어 | Track |
|------|------|--------|-------|
| 구조·크기 검증 | `InputContractValidator`, `PuzzleBoundary.receive` | Boundary | Track A (UI Contract) |
| Domain 격리 | `SolvePuzzleUseCase.execute` 호출 횟수 | Boundary → Control | Track A (Mock) |
| 고정 에러 계약 | `ErrorResponse.code`, `ErrorResponse.message` | Boundary | Track A |

### 1.2 Out-of-Scope (본 계획서)

| 항목 | 사유 | 후속 Test-ID |
|------|------|--------------|
| **4×4 정상 입력** | AC-FR-01-01(크기 실패) 범위 외; 성공 경로·해 벡터 검증은 FR-05 슬라이스 | U-T05, D-T01~02, IT-01 |
| 빈칸 수·값 범위·중복 검증 | FR-01 후속 AC; 크기 통과 후에만 의미 있음 | U-T02~U-T04 |
| Domain 불변식(I-D*) | Track B 전용; Mock 금지 | D-T01~D-T16 |
| 통합 E2E | Track A·B GREEN 이후 | IT-01, IT-F01 |

> **코드 명칭 정합:** 본 문서의 **AC-FR-01-01**은 PRD **AC-FR01-1**(4×4 구조 검증)의 선행 확장 케이스(`None`)이다. Boundary 노출 코드는 PRD §13 기준 **`E_SIZE`** 이며, Domain 내부 `INVALID_GRID_SIZE`는 Boundary에 노출하지 않는다.

---

## 2. 테스트 환경

| 항목 | 버전 / 도구 |
|------|-------------|
| Python | 3.11+ (프로젝트 `requires-python`: ≥3.12) |
| 테스트 프레임워크 | pytest ≥8.0 |
| 스키마 / DTO | pydantic (`ErrorResponse` 등 Boundary 계약 모델) |
| Mock | `unittest.mock` (`Mock`, `patch`, `MagicMock`) |
| 커버리지 | pytest-cov |
| 스타일 | AAA (Arrange–Act–Assert), `test_` 접두사, Test-ID docstring |

### 2.1 디렉터리·마커

```
tests/
├── boundary/          # Track A — 본 계획서 주 대상
│   └── test_input_contract.py
├── control/           # (후속) UseCase 단위
├── entity/            # Track B — Mock 금지, 본 슬라이스 비포함
└── integration/       # 양 Track GREEN 후
```

| Marker | 용도 |
|--------|------|
| `@pytest.mark.unit` | Boundary/Control 단위 (본 계획서 전체) |
| `@pytest.mark.integration` | Boundary→Control→Entity (본 슬라이스 이후) |

---

## 3. pytest 단위 테스트 범위 및 우선순위

### 3.1 우선순위 매트릭스

| Priority | Test-ID | 시나리오 요약 | 검증 컴포넌트 | AC |
|----------|---------|---------------|---------------|-----|
| **P0** | U-T00 | `grid=None` | `PuzzleBoundary`, `InputContractValidator` | AC-FR-01-01, AC-FR01-5 |
| **P0** | U-T01a | `grid=[]` (행 0) | `InputContractValidator` | AC-FR01-1 |
| **P0** | U-T01b | `grid=[[]]*4` (열 0) | `InputContractValidator` | AC-FR01-1 |
| **P1** | U-T01c | 3×4 격자 | `InputContractValidator` | AC-FR01-1 |
| **P1** | U-T01d | 4×3 격자 | `InputContractValidator` | AC-FR01-1 |
| **P1** | U-T01e | 5×5 격자 | `InputContractValidator` | AC-FR01-1 |
| **P2** | U-T08-size | `E_SIZE` 메시지 byte-equal 회귀 | `ErrorMessages`, `PuzzleBoundary` | §13 UX-3 |

### 3.2 실행 순서 (Dual-Track RED 권장)

1. **RED:** P0 U-T00 → P0 U-T01a/b → P1 U-T01c~e (각각 독립 FAIL 확인)
2. **GREEN:** `InputContractValidator`에 null·타입·행/열 수 검사 최소 구현
3. **GREEN:** `PuzzleBoundary`가 검증 실패 시 UseCase 위임 차단
4. **REFACTOR:** `GridSize` VO / `InvalidInputGuard` 추출 (공개 계약·메시지 불변)

### 3.3 테스트 레벨 분리

| 레벨 | 파일 | Act 대상 | Assert 초점 |
|------|------|----------|-------------|
| **L1 — Validator 단위** | `test_input_contract.py` | `InputContractValidator.validate(grid)` | `ErrorResponse` 또는 `ValidationResult` |
| **L2 — Boundary 통합(단위)** | `test_input_contract.py` | `PuzzleBoundary.receive(grid)` | `ErrorResponse` + UseCase Mock 0회 |

L1은 순수 검증 로직 branch 커버리지, L2는 **Domain 진입점 격리(AC-FR01-5)** 를 담당한다.

---

## 4. 경계값 케이스 목록

모든 케이스의 **기대 Boundary 응답**은 동일하다.

```json
{
  "code": "E_SIZE",
  "message": "ERROR: Grid must be 4x4."
}
```

| ID | 입력 (`grid`) | 위반 유형 | 행 수 | 열 수 (각 행) | Test-ID | Priority |
|----|---------------|-----------|-------|---------------|---------|----------|
| BV-01 | `None` | null / 미제공 | — | — | U-T00 | P0 |
| BV-02 | `[]` | 빈 리스트 (행 0) | 0 | — | U-T01a | P0 |
| BV-03 | `[[]] * 4` | 행 4, 열 0 (공유 빈 행 참조) | 4 | 0 | U-T01b | P0 |
| BV-04 | 3×4 (`[[1]*4]*3`) | 행 부족 | 3 | 4 | U-T01c | P1 |
| BV-05 | 4×3 (`[[1]*3]*4`) | 열 부족 | 4 | 3 | U-T01d | P1 |
| BV-06 | 5×5 (`[[1]*5]*5`) | 행·열 초과 | 5 | 5 | U-T01e | P1 |

### 4.1 명시적 제외

| ID | 입력 | 제외 사유 |
|----|------|-----------|
| **EX-01** | 4×4 정상 퍼즐 (빈칸 2개, 값 유효) | AC-FR-01-01 **범위 외**. 크기 검증 **통과** 케이스이므로 본 슬라이스 테스트 세트에 **포함하지 않음**. FR-05 / U-T05에서 별도 검증. |

### 4.2 검증 체크리스트 (케이스 공통)

- [ ] 반환 타입이 `ErrorResponse`(pydantic)이며 예외가 Caller에 전파되지 않음
- [ ] `response.code == "E_SIZE"`
- [ ] `response.message == "ERROR: Grid must be 4x4."` (UX-3 byte-equal)
- [ ] `SolvePuzzleUseCase.execute` Mock 호출 **0회** (L2 테스트)
- [ ] 입력 `grid` 객체/참조가 Act 전후로 변형되지 않음 (NFR-05, `None` 제외)

---

## 5. 예외·특이 케이스 목록

| ID | 카테고리 | 입력 / 조건 | 기대 동작 | Test-ID | 비고 |
|----|----------|-------------|-----------|---------|------|
| EC-01 | 타입 오류 | `grid=123` (int) | `E_SIZE`, Domain 0회 | U-T01f | `None` 다음 선행 가드 |
| EC-02 | 타입 오류 | `grid="not a grid"` (str) | `E_SIZE`, Domain 0회 | U-T01g | iterable 아님 |
| EC-03 | 혼합 행 길이 | `[[1,2,3,4], [1,2,3], [1,2,3,4], [1,2,3,4]]` | `E_SIZE`, Domain 0회 | U-T01h | 행별 열 수 불일치 |
| EC-04 | 비-list 행 | `[[1,2,3,4], (1,2,3,4), ...]` | `E_SIZE`, Domain 0회 | U-T01i | 행 원소가 list 아님 |
| EC-05 | shallow copy 함정 | `[[]]*4` 후 `grid[0].append(1)` | 여전히 `E_SIZE` (열≠4) | U-T01b-reg | `[[]]*4` 구조 변형 시에도 크기 규칙 유지 |
| EC-06 | 결정성 | BV-01~06 동일 입력 2회 실행 | 동일 `ErrorResponse` | NFR-04 | I-D12 계약 준수 |
| EC-07 | 다중 위반 | 3×4 + 셀값 17 | **첫 위반** `E_SIZE` | DN-03 | 구현이 “첫 발견” 정책이면 크기 우선 |

---

## 6. Domain 해 결정 진입점 호출 횟수 검증 전략

### 6.1 격리 대상 (Mock/Spy 포인트)

ECB 규칙상 Boundary는 Entity를 직접 호출하지 않는다. **Mock 대상은 Control 계층 진입점**이다.

| Mock 대상 | 레이어 | 역할 |
|-----------|--------|------|
| `SolvePuzzleUseCase.execute` | Control | Domain 오케스트레이션 진입점 (**1차 Mock**) |
| `PuzzleSolver.solve` | Entity | Domain 알고리즘 (**Boundary 테스트에서 Mock 금지·직접 patch 금지**) |

> Boundary 테스트(L2)에서는 **`SolvePuzzleUseCase`만 Mock**한다. `PuzzleSolver` 직접 patch는 ECB 레이어 우회이므로 사용하지 않는다.

### 6.2 Mock 패턴 (Track A — `unittest.mock`)

**패턴 A — 생성자 주입 (권장)**

```python
# Arrange
mock_use_case = Mock(spec=SolvePuzzleUseCase)
boundary = PuzzleBoundary(use_case=mock_use_case)

# Act
result = boundary.receive(grid=None)

# Assert
mock_use_case.execute.assert_not_called()
assert result.code == "E_SIZE"
```

**패턴 B — `patch` (기존 Boundary가 내부에서 UseCase를 생성하는 경우)**

```python
with patch(
    "boundary.puzzle_boundary.SolvePuzzleUseCase"
) as MockUseCaseClass:
    mock_instance = MockUseCaseClass.return_value
    result = PuzzleBoundary().receive(grid=None)
    mock_instance.execute.assert_not_called()
```

### 6.3 Spy vs Mock 선택 기준

| 기법 | 사용 시점 | 본 슬라이스 |
|------|-----------|-------------|
| **Mock** (`Mock(spec=...)`) | Domain **미호출** 검증 (AC-FR01-5) | **필수** — `assert_not_called()` |
| **Spy** (`wraps=`) | 성공 경로에서 **정확히 1회** 호출 검증 | 본 슬라이스 **미사용** (U-T05 범위) |
| **Autospec** | 인터페이스 drift 방지 | `spec=SolvePuzzleUseCase` 권장 |

### 6.4 실패 시 진단 기준

| 관측 | 원인 추정 | 조치 |
|------|-----------|------|
| `execute` 1회 호출 | Boundary가 검증 전 UseCase 위임 | `InputContractValidator` 선행 호출 순서 수정 |
| `AttributeError` on receive | Boundary 미구현 (RED 정상) | GREEN: `PuzzleBoundary.receive` 스켈레톤 |
| `TypeError` instead of `ErrorResponse` | null 가드 누락 | `None`/비-list 거부 분기 추가 |

---

## 7. 커버리지 목표

PRD §14 NFR 및 `.cursor/rules/magicsquare-tdd-testing.mdc` 기준.

| 대상 | Metric | Gate | 측정 범위 (본 슬라이스) |
|------|--------|------|---------------------------|
| **Boundary** | branch | **≥ 85%** | `InputContractValidator`, `PuzzleBoundary` 크기 검증 분기 |
| **Domain (Entity)** | branch | **≥ 95%** | 본 슬라이스 **해당 없음** (크기 실패 시 Domain 미진입) |
| **전역** | line / branch | **≥ 80%** | `src/` 전체 (CI gate) |

### 7.1 본 슬라이스 Boundary branch 커버 대상

| 분기 | 트리거 입력 |
|------|-------------|
| `grid is None` | BV-01 |
| `not isinstance(grid, list)` | EC-01, EC-02 |
| `len(grid) != 4` | BV-02, BV-04, BV-06 |
| `any(len(row) != 4 for row in grid)` | BV-03, BV-05, EC-03 |
| `row`가 list가 아님 | EC-04 |
| 검증 통과 → UseCase 위임 | **본 계획서 제외** (EX-01) |

Domain 95%+ gate는 Track B GREEN(U-T05 이후 D-T*) 단계에서 별도 측정한다.

---

## 8. pytest-cov 측정 전략

### 8.1 설치

```bash
pip install pytest-cov
```

또는 dev 의존성 일괄 설치:

```bash
pip install -e ".[dev]"
pip install pytest-cov pydantic
```

### 8.2 기본 측정 (전역)

```bash
pytest --cov=src --cov-report=term-missing
```

### 8.3 Boundary 슬라이스 집중 측정

```bash
pytest tests/boundary/test_input_contract.py \
  --cov=boundary \
  --cov-report=term-missing \
  --cov-branch \
  -m unit
```

### 8.4 Gate 실패 시 상세 HTML 리포트

```bash
pytest tests/boundary/ \
  --cov=boundary \
  --cov-branch \
  --cov-report=html:htmlcov/boundary \
  --cov-fail-under=85
```

### 8.5 CI 권장 설정 (`pyproject.toml` 추가 예)

```toml
[tool.coverage.run]
source = ["src"]
branch = true

[tool.coverage.report]
fail_under = 80
show_missing = true

[tool.coverage.paths]
source = ["src"]
```

| Report | 용도 |
|--------|------|
| `term-missing` | 로컬 RED/GREEN 루프 — 미커버 라인 즉시 확인 |
| `html` | REFACTOR — branch 분기 누락 시각화 |
| `--cov-fail-under` | CI gate (Boundary 85, Domain 95는 path별 별도 job 권장) |

---

## 9. Traceability

| Concept | Business Rule | FR | AC | Test-ID | Component |
|---------|---------------|-----|-----|---------|-----------|
| 4×4 입력 구조 | BR-01 | FR-01 | AC-FR-01-01, AC-FR01-1 | U-T00, U-T01a~e | `InputContractValidator` |
| Domain 미호출 | §13 | FR-01 | AC-FR01-5 | U-T00, U-T01a~e | `PuzzleBoundary` |
| 고정 E_SIZE 메시지 | §13 UX-3 | FR-01 | U-T08 | U-T08-size | `ErrorMessages` |

---

## 10. Release Verification Checklist (본 슬라이스)

- [ ] BV-01~06 전부 `E_SIZE` + message byte-equal
- [ ] L2 테스트 전 케이스 `SolvePuzzleUseCase.execute` 0회
- [ ] EX-01 (4×4 정상)이 **본 테스트 파일에 없음** 확인
- [ ] Boundary branch coverage ≥ 85% (`--cov-branch`)
- [ ] Domain Track 테스트에 `unittest.mock` 미사용 (entity/)
- [ ] REFACTOR 후 U-T08-size 메시지 회귀 없음

---

## 11. 문서 이력

| 버전 | 일자 | 변경 |
|------|------|------|
| 1.0 | 2026-05-29 | AC-FR-01-01 (`grid=None`) 앵커 FR-01 크기 검증 슬라이스 초안 |
