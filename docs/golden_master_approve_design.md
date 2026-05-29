# Golden Master Approve Pattern — GM-1 Design

## 목적

Magic Square Solver의 **실제 Boundary 출력**을 기준선(baseline)으로 고정하고, 회귀 시 `actual`과 `expected`를 비교한다. 불일치 시 unified diff를 출력한 뒤 테스트를 FAIL 한다.

## 범위

| 항목 | 내용 |
|------|------|
| Test-ID | GM-1 (full doc) / GM-2 (per TC) |
| 블록 헤더 | `[GM-TC-01]` … `[GM-TC-05]` |
| 진입점 | `PuzzleBoundary.receive` → `SolvePuzzleUseCase` (Mock 없음) |
| 캡처 대상 | `list[int]` 성공 또는 `ErrorResponse.code` 실패 |
| 기준 파일 | `tests/golden_master_expected.txt` (버전 관리 필수) |

## 시나리오 (5종)

| 블록 이름 | 의미 | 입력 앵커 |
|-----------|------|-----------|
| `normal_success` | attempt A 성공 | PRD 예시 격자 |
| `reverse_success` | attempt B 성공 | Report/02·D-T02 / Control `PUZZLE_GRID` |
| `invalid_blank_count` | 빈칸 수 ≠ 2 | U-T02a (0개 빈칸) |
| `duplicate_number` | 비零 중복 | PRD `duplicate_five` |
| `no_valid_solution` | A·B 모두 실패 | D-T13 `no_completion` |

## 기준 파일 구조

```
[scenario_name]
Input:
<4 rows, space-separated integers>
Output:
[r1, c1, n1, r2, c2, n2]
```

오류 시:

```
[scenario_name]
Input:
...
Error:
E_<CODE>
```

- 성공: `Output:` 뒤에 Python `list` 리터럴 문자열 (`str(list[int])`).
- 실패: `Error:` 뒤에 Boundary 노출 **코드만** (메시지는 UX-3 byte-equal 테스트 U-T08에서 별도 검증).
- 블록 구분: 빈 줄 1개.
- 인코딩: UTF-8, 줄바꿈 LF.

## Approve 패턴

```
┌─────────────────┐
│  pytest GM-1    │
└────────┬────────┘
         │
         ▼
  golden_master_expected.txt 존재?
         │
    ┌────┴────┐
   No        Yes
    │          │
    ▼          ▼
 현재 출력    actual vs expected
 기준 생성    비교
    │          │
    │     ┌────┴────┐
    │    일치      불일치
    │     │          │
    ▼     ▼          ▼
  PASS  PASS    unified diff + FAIL
```

### 모드

| 명령 | 동작 |
|------|------|
| `pytest tests/golden_master/test_gm01_golden_master.py` | 비교 모드 (기본) |
| `pytest ... --approve-golden-master` | 현재 출력으로 기준 파일 **덮어쓰기** |
| `python scripts/generate_golden_master.py` | 생성 스크립트 (항상 approve) |

**규칙**

1. 기준 파일 **없음** → 첫 실행 시 현재 출력을 자동 생성 후 PASS.
2. 기준 파일 **있음** → byte-equal 비교.
3. **불일치** → `difflib.unified_diff` 출력 후 `AssertionError`.
4. 의도적 출력 변경 시에만 `--approve-golden-master` 또는 생성 스크립트로 갱신.

## 모듈 배치

```
tests/
├── golden_master_expected.txt      # 버전 관리 대상 baseline
├── golden_master/
│   ├── scenarios.py              # 입력 시나리오 고정
│   ├── capture.py                # Boundary 실행 + 직렬화
│   ├── approve.py                # compare / approve
│   └── test_gm01_golden_master.py
scripts/
└── generate_golden_master.py       # CLI 생성기
```

## ECB / TDD 정합

- Boundary → Control만 호출 (Entity 직접 호출 없음).
- Golden Master는 **통합 회귀**이므로 `tests/golden_master/`에 두고 `@pytest.mark.integration` 적용.
- 단위 계약(U-T02~U-T04) RED/GREEN과 병행; GM-1은 E2E 스냅샷으로 보완.

## 운영 체크리스트

- [ ] 솔버·매핑 변경 후 `pytest tests/golden_master/` GREEN 확인
- [ ] 의도적 변경 시 diff 검토 후 approve
- [ ] `git add tests/golden_master_expected.txt` 로 baseline 커밋
