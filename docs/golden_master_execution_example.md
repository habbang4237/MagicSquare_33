# GM-2 실행 결과 예시

## 전체 Golden Master 스위트

```bash
pytest -m golden_master -v
```

### 성공 시 (GREEN)

```
============================= test session starts =============================
platform win32 -- Python 3.14.0, pytest-8.4.2, pluggy-1.6.0
collected 11 items

tests/golden_master/test_golden_master_magic_square.py::test_gm_tc_01_normal_success PASSED
tests/golden_master/test_golden_master_magic_square.py::test_gm_tc_02_reverse_success PASSED
tests/golden_master/test_golden_master_magic_square.py::test_gm_tc_03_invalid_blank_count PASSED
tests/golden_master/test_golden_master_magic_square.py::test_gm_tc_04_duplicate_number PASSED
tests/golden_master/test_golden_master_magic_square.py::test_gm_tc_05_no_valid_magic_square PASSED
tests/golden_master/test_golden_master_magic_square.py::TestGoldenMasterMagicSquareInputs::test_gm_tc_01_grid_locked PASSED
tests/golden_master/test_golden_master_magic_square.py::TestGoldenMasterMagicSquareInputs::test_gm_tc_02_grid_locked PASSED
tests/golden_master/test_golden_master_magic_square.py::TestGoldenMasterMagicSquareInputs::test_gm_tc_03_grid_has_zero_blanks PASSED
tests/golden_master/test_golden_master_magic_square.py::TestGoldenMasterMagicSquareInputs::test_gm_tc_04_grid_has_duplicate_five PASSED
tests/golden_master/test_golden_master_magic_square.py::TestGoldenMasterMagicSquareInputs::test_gm_tc_05_grid_has_two_blanks PASSED
tests/golden_master/test_gm01_golden_master.py::test_gm01_golden_master_boundary_output PASSED

============================== 11 passed in 0.08s ==============================
```

## 단일 Test-Case 실행

```bash
pytest tests/golden_master/test_golden_master_magic_square.py::test_gm_tc_01_normal_success -v
```

## 기준 파일 갱신 (approve)

```bash
pytest -m golden_master --approve-golden-master -v
```

또는:

```bash
python scripts/generate_golden_master.py
```

## 실패 시 출력 예시 (unified diff)

솔버 출력이 `tests/golden_master_expected.txt`와 다를 때:

```
FAILED tests/golden_master/test_golden_master_magic_square.py::test_gm_tc_01_normal_success
AssertionError: GM-TC-01 Golden Master mismatch. Run with --approve-golden-master to update.
--- GM-TC-01 (expected)
+++ GM-TC-01 (actual)
@@ -5,4 +5,4 @@
 9 7 0 12
 4 14 15 0
 Output:
-[3, 3, 6, 4, 4, 1]
+[3, 3, 1, 4, 4, 6]
```

## 검증 항목 요약

| Test-Case | Golden block | Contract 검증 |
|-----------|--------------|---------------|
| GM-TC-01 | `Output: int[6]` | row-major, 1-index, attempt A (small-first) |
| GM-TC-02 | `Output: int[6]` | row-major, 1-index, attempt B (reverse fallback) |
| GM-TC-03 | `Error: E_EMPTY_COUNT` | ErrorResponse code + fixed message |
| GM-TC-04 | `Error: E_DUPLICATE` | ErrorResponse code + fixed message |
| GM-TC-05 | `Error: E_NO_SOLUTION` | ErrorResponse code + fixed message |

## 기준 파일 위치

`tests/golden_master_expected.txt`

블록 헤더 형식: `[GM-TC-01]` … `[GM-TC-05]`
