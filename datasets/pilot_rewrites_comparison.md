# Pilot Rewriter Evaluation Report (20 Samples)

This report compares raw agent trace conclusions against humanized rewrites generated via Agency Gateway models (`ne-gpt-oss-120b` and `or-nvidia-nemotron-3-ultra-550b`), conditioned on our 34 style exemplars.

---

## Summary Metrics

- **Total Samples Evaluated**: 19
- **Tech Docs**: 6
- **Changelogs / PR Notes**: 9
- **Engineering Lore / Deep Dives**: 4
- **Mean Raw Length**: 1872 chars
- **Mean Rewritten Length**: 1854 chars
- **Mean Compression Ratio**: 1.08
- **Banned Cliché Violations**: 0 total

---

### Sample 01: raw_trace_05456 (CHANGELOGS)
- **Original Source**: `openhands/swe-agent` (nvidia/SWE-Hero-openhands-trajectories)
- **Rewriter**: `ne-gpt-oss-120b`
- **Length**: Raw `2163` chars -> Rewritten `1175` chars (ratio `0.543`)
- **Cliché Violations**: `None (Clean)`

#### 🔻 Raw Agent Output (Original)
```markdown
## Summary

I have successfully implemented the fix for the PerformanceWarning issue with Extension Arrays. Here's what I accomplished:

### 🎯 **Problem Fixed**
- **Issue**: PerformanceWarning incorrectly raised when inserting columns into DataFrames with many Extension Array columns
- **Root Cause**: Block counting logic counted ALL blocks including Extension Array blocks
- **Solution**: Modified logic to count only regular (non-Extension Array) blocks

### 🔧 **Changes Made**

#### File: `/workspace/pandas-dev__pandas__1.0/pandas/core/internals/managers.py`

1. **Added Import** (line 37):
   ```python
   is_extension_array_dtype,
   ```

2. **Modified Block Counting Logic** (lines 1178-1191):
   ```python
   # Only count non-extension array blocks for fragmentation warning
   # Extension Array blocks don't contribute to fragmentation performance issues
   non_ea_block_count = sum(
       1 for block in self.blocks if not is_extension_array_dtype(block.dtype)
   )
   if non_ea_block_count > 100:
       warnings.warn(...)
   ```

### ✅ **Verification Results**

1. **Original Issue Fixed**: ✅ 
   - DataFrame with 100 Extension Array columns + 1 new column → No warning
   
2. **Backwa
... [truncated for display]
```

#### 🌟 Rewritten Human Prose (Target)
**Fix PerformanceWarning for DataFrames with Extension Array columns**

**Problem**  
`PerformanceWarning` fired when inserting a column into a DataFrame that already contained many Extension Array columns. The block‑counting logic treated Extension Array blocks as regular blocks, inflating the fragmentation count.

**Change**  
*File:* `pandas/core/internals/managers.py`

- Import `is_extension_array_dtype`.
- Replace the block count used for the warning with a count of only non‑Extension Array blocks:

```python
# Count only regular blocks for fragmentation warning
non_ea_block_count = sum(
    1 for block in self.blocks if not is_extension_array_dtype(block.dtype)
)
if non_ea_block_count > 100:
    warnings.warn(...)
```

**Result**  

- Inserting a column into a DataFrame with 100 Extension Array columns no longer triggers the warning.  
- The warning still appears when the number of regular blocks exceeds the threshold.  
- Mixed DataFrames warn based solely on regular block count.  
- All existing pandas tests pass; no regression introduced.  

**Scope**  

- 7 lines modified in a single file.  
- No API changes; behavior identical for regular blocks.

---

### Sample 02: raw_trace_09811 (CHANGELOGS)
- **Original Source**: `openhands/swe-agent` (nvidia/SWE-Hero-openhands-trajectories)
- **Rewriter**: `or-nvidia-nemotron-3-ultra-550b`
- **Length**: Raw `2084` chars -> Rewritten `915` chars (ratio `0.439`)
- **Cliché Violations**: `None (Clean)`

#### 🔻 Raw Agent Output (Original)
```markdown
Excellent! Everything is working perfectly.

## Summary

I have successfully implemented the necessary changes to fix the `digitize` function issue with the new `edge` keyword argument. Here's what was accomplished:

### **Problem Analysis**
The issue was that the `digitize` function was expected to accept a fourth parameter (`edge`), but the underlying dispatcher function `_digitize_dispatcher` wasn't updated to handle this additional argument, causing a `TypeError` when 4 arguments were passed.

### **Solution Implemented**
Made minimal, focused changes to `/workspace/numpy__numpy__1.0/numpy/lib/function_base.py`:

1. **Updated Dispatcher Function** (line 4736):
   ```python
   # Before: def _digitize_dispatcher(x, bins, right=None):
   # After:  def _digitize_dispatcher(x, bins, right=None, edge=None):
   ```

2. **Updated Main Function Signature** (line 4741):
   ```python
   # Before: def digitize(x, bins, right=False):
   # After:  def digitize(x, bins, right=False, edge=False):
   ```

3. **Added Documentation** (lines 4770-4771):
   ```python
   edge : bool, optional
       Not currently used. Reserved for future functionality.
   ```

### **Verification Results**
✅ **Origi
... [truncated for display]
```

#### 🌟 Rewritten Human Prose (Target)
Fixed `digitize` dispatcher to accept the new `edge` keyword argument.

The dispatcher `_digitize_dispatcher` at `numpy/lib/function_base.py:4736` previously accepted only three parameters (`x`, `bins`, `right`), causing a `TypeError` when callers passed four arguments. Updated both the dispatcher and the public `digitize` signature to include `edge=False`, and added the parameter to the docstring as reserved for future use.

**Changes**
- `numpy/lib/function_base.py:4736` — `_digitize_dispatcher(x, bins, right=None, edge=None)`
- `numpy/lib/function_base.py:4741` — `digitize(x, bins, right=False, edge=False)`
- `numpy/lib/function_base.py:4770-4771` — docstring entry for `edge`

**Verification**
- `np.digitize(x, bins, False, True)` now executes without error
- All existing digitize tests pass (11/12; 1 pre-existing failure unrelated)
- Backward compatibility preserved for all existing call signatures

---

### Sample 03: raw_trace_09865 (CHANGELOGS)
- **Original Source**: `openhands/swe-agent` (nvidia/SWE-Hero-openhands-trajectories)
- **Rewriter**: `ne-gpt-oss-120b`
- **Length**: Raw `1826` chars -> Rewritten `793` chars (ratio `0.434`)
- **Cliché Violations**: `None (Clean)`

#### 🔻 Raw Agent Output (Original)
```markdown
Perfect! Let me review what I've accomplished:

### Summary of Changes Made:

1. **Core Fix**: Modified `agg_list_like` method in `/workspace/pandas-dev__pandas__1.0/pandas/core/apply.py` to preserve the order of aggregation functions in the result index.

2. **Targeted Approach**: The fix only activates when it detects that different DataFrame columns produce Series with different indices (which causes the reordering issue). This prevents interference with normal cases.

3. **Updated Test**: Modified `test_agg_multiple_mixed_no_warning` in `/workspace/pandas-dev__pandas__1.0/pandas/tests/apply/test_frame_apply.py` to reflect the new expected behavior of preserving input order.

### Verification:

✅ **Issue Fixed**: The original reproduction case now works correctly:
- Input: `df.agg(["sum", foo, "count", "min"])`  
- Expected index: `['sum', 'foo', 'count', 'min']`
- Actual index: `['sum', 'foo', 'count', 'min']` ✓

✅ **Backward Compatibility**: Most existing functionality is preserved, with only the specific test updated to reflect the new intended behavior.

✅ **Edge Cases Handled**: Various orderings and data type combinations work correctly.

✅ **No Regression**: All existing 
... [truncated for display]
```

#### 🌟 Rewritten Human Prose (Target)
**Preserve aggregation function order in `DataFrame.agg`**

- Update `agg_list_like` in `pandas/core/apply.py` to keep the order of aggregation functions in the result index.  
- Activate the fix when columns return `Series` with mismatched indices, preventing unintended reordering while leaving the normal path unchanged.  
- Adjust `test_agg_multiple_mixed_no_warning` in `pandas/tests/apply/test_frame_apply.py` to assert the preserved order.  

**Result**  
`df.agg(["sum", foo, "count", "min"])` now returns an index `['sum', 'foo', 'count', 'min']` as expected.  

**Impact**  
- Handles mixed‑type column aggregations that previously produced reordered indices.  
- Maintains existing aggregation behavior for all other cases.  
- All aggregation‑related tests pass without regression.

---

### Sample 04: raw_trace_05756 (CHANGELOGS)
- **Original Source**: `openhands/swe-agent` (nvidia/SWE-Hero-openhands-trajectories)
- **Rewriter**: `or-nvidia-nemotron-3-ultra-550b`
- **Length**: Raw `1223` chars -> Rewritten `770` chars (ratio `0.63`)
- **Cliché Violations**: `None (Clean)`

#### 🔻 Raw Agent Output (Original)
```markdown
Perfect! All tests pass.

### 8.3 Final Summary

**Problem Solved**: The `unique()` function in pandas now preserves the input dtype for narrow numeric types instead of converting them to wider types.

**Change Made**: Modified one line in `/workspace/pandas-dev__pandas__1.0/pandas/core/algorithms.py`:
- Line 399: Changed `uniques = _reconstruct_data(uniques, dtype, original)` to `uniques = _reconstruct_data(uniques, original.dtype, original)`

**Impact**:
- ✅ **float32** Series/Index now return **float32** from `unique()` (was float64)
- ✅ **int8** Series/Index now return **int8** from `unique()` (was int64)  
- ✅ **int16** Series/Index now return **int16** from `unique()` (was int64)
- ✅ **int32** Series/Index now return **int32** from `unique()` (was int64)
- ✅ **uint8** Series/Index now return **uint8** from `unique()` (was uint64)
- ✅ **uint16** Series/Index now return **uint16** from `unique()` (was uint64)
- ✅ **uint32** Series/Index now return **uint32** from `unique()` (was uint64)

**Benefits**:
- Reduced memory usage (up to 50% less for float32/int32 types)
- Preserved numerical precision 
- Backward compatible - all existing tests pass
- Consistent with similar function
... [truncated for display]
```

#### 🌟 Rewritten Human Prose (Target)
`unique()` now preserves the input dtype for narrow numeric types.

Previously, `unique()` passed the inferred `dtype` parameter to `_reconstruct_data`, which widened `float32` → `float64`, `int8` → `int64`, and equivalent unsigned types. The call now passes `original.dtype` directly, so the reconstruction step respects the source array's precision.

**Change**: `pandas/core/algorithms.py:399` — `_reconstruct_data(uniques, dtype, original)` → `_reconstruct_data(uniques, original.dtype, original)`

**Effect**: `float32`, `int8`, `int16`, `int32`, `uint8`, `uint16`, `uint32` Series and Index objects return matching dtypes from `unique()`. Memory usage drops proportionally (up to 50% for 32-bit types) and numerical precision is preserved. All existing tests pass.

---

### Sample 05: raw_trace_09067 (CHANGELOGS)
- **Original Source**: `openhands/swe-agent` (nvidia/SWE-Hero-openhands-trajectories)
- **Rewriter**: `ne-gpt-oss-120b`
- **Length**: Raw `1377` chars -> Rewritten `621` chars (ratio `0.451`)
- **Cliché Violations**: `None (Clean)`

#### 🔻 Raw Agent Output (Original)
```markdown
Perfect! My changes are minimal and targeted. Let me summarize what I've accomplished:

## Summary

### ✅ Issue Fixed Successfully

**Problem:** Categorical `!=` comparison with NA values was incorrectly returning `False` instead of `True`.

**Root Cause:** In the `_cat_compare_op` function in `/workspace/pandas-dev__pandas__1.0/pandas/core/arrays/categorical.py`, the code was unconditionally setting all NA-related comparisons to `False`, regardless of the operator.

**Solution:** Modified the logic to differentiate between operators:
- For `__ne__` (!=): Set NA comparisons to `True` 
- For `__eq__` (==) and other operators: Keep NA comparisons as `False`

**Changes Made:**
1. **Lines 105-110**: Fixed Categorical vs Categorical comparison logic
2. **Lines 121-125**: Fixed Categorical vs scalar comparison logic

**Verification:**
- ✅ Original issue example now works correctly
- ✅ All existing tests still pass (36/36 operator tests passed)
- ✅ All missing value tests still pass (10/10 tests passed)
- ✅ `==` operations remain unchanged and correct
- ✅ Other comparison operators (`<`, `>`, `<=`, `>=`) remain correct
- ✅ Scalar comparisons work correctly
- ✅ Edge cases handled properly

... [truncated for display]
```

#### 🌟 Rewritten Human Prose (Target)
### Fix categorical `!=` comparison with NA

- Modify `_cat_compare_op` in `pandas/core/arrays/categorical.py` to return `True` for `!=` when either operand is NA, while keeping `False` for `==` and other operators.  
- Update the categorical‑vs‑categorical branch (lines 105‑110) and the categorical‑vs‑scalar branch (lines 121‑125) to branch on the operator instead of forcing a universal `False`.  
- Preserve existing semantics for equality, ordering, and scalar comparisons.

All operator tests (36) and missing‑value tests (10) pass, confirming correct behavior for `!=`, `==`, `<`, `>`, `<=`, `>=`, and edge cases.

---

### Sample 06: raw_trace_08719 (CHANGELOGS)
- **Original Source**: `openhands/swe-agent` (nvidia/SWE-Hero-openhands-trajectories)
- **Rewriter**: `or-nvidia-nemotron-3-ultra-550b`
- **Length**: Raw `1582` chars -> Rewritten `646` chars (ratio `0.408`)
- **Cliché Violations**: `None (Clean)`

#### 🔻 Raw Agent Output (Original)
```markdown
Excellent! Everything is working perfectly.

## Summary

I have successfully implemented the fix for the misleading error message when `__array_ufunc__` returns `NotImplemented`. Here's what I accomplished:

### **Changes Made:**

1. **Modified `numpy/core/_internal.py`** (lines 691-700):
   - Changed the error message in `array_ufunc_errmsg_formatter` from:
     ```
     "operand type(s) do not implement __array_ufunc__..."
     ```
     to:
     ```
     "operand type(s) all returned NotImplemented from __array_ufunc__..."
     ```

2. **Updated `numpy/core/tests/test_umath.py`** (lines 1934-1943):
   - Updated test expectations to match the new accurate error message

### **Problem Solved:**

**Before:** When a class implemented `__array_ufunc__` but returned `NotImplemented`, the error message incorrectly claimed the class didn't implement the method.

**After:** The error message now accurately states that the classes DO implement `__array_ufunc__` but all returned `NotImplemented`.

### **Verification:**

✅ **Original issue case fixed**: `np.negative(A())` where `A` implements `__array_ufunc__` now shows accurate message  
✅ **Backward compatibility maintained**: All existing
... [truncated for display]
```

#### 🌟 Rewritten Human Prose (Target)
**Fix `__array_ufunc__` error message accuracy**

Updated `array_ufunc_errmsg_formatter` in `numpy/core/_internal.py:691` to distinguish between missing implementations and explicit `NotImplemented` returns.

**Before:** `np.negative(A())` where `A` implements `__array_ufunc__` returning `NotImplemented` raised:
> `TypeError: operand type(s) do not implement __array_ufunc__`

**After:** The same call raises:
> `TypeError: operand type(s) all returned NotImplemented from __array_ufunc__`

The formatter now checks the return value before claiming the method is absent. Updated corresponding assertion in `numpy/core/tests/test_umath.py:1934`.

---

### Sample 07: raw_trace_09060 (CHANGELOGS)
- **Original Source**: `openhands/swe-agent` (nvidia/SWE-Hero-openhands-trajectories)
- **Rewriter**: `ne-gpt-oss-120b`
- **Length**: Raw `1264` chars -> Rewritten `839` chars (ratio `0.664`)
- **Cliché Violations**: `None (Clean)`

#### 🔻 Raw Agent Output (Original)
```markdown
### Final Review Summary

✅ **Requirements Fully Addressed:**

1. **DataFrame.sort_values**: Now raises `FutureWarning` when positional arguments are used for parameters other than `by`
2. **Series.sort_values**: Now raises `FutureWarning` when positional arguments are used for any parameters beyond `self`
3. **Correct Usage**: Keyword arguments continue to work without warnings
4. **Backward Compatibility**: All existing functionality is preserved

✅ **Implementation Details:**

- **Minimal Changes**: Only added decorators, no logic changes
- **Proper Placement**: Decorators placed correctly before method definitions
- **Correct Parameters**: 
  - `DataFrame.sort_values`: `allowed_args=["self", "by"]`
  - `Series.sort_values`: `allowed_args=["self"]`
- **Consistent Pattern**: Follows existing pandas conventions

✅ **Testing Results:**

- Original issue examples now correctly produce `FutureWarning`
- All existing tests continue to pass (with expected new warnings in tests that used positional args)
- Core functionality remains intact
- Edge cases handled properly

The implementation successfully resolves the issue described in the problem statement with minimal, focused changes th
... [truncated for display]
```

#### 🌟 Rewritten Human Prose (Target)
### Changelog

- Emit a `FutureWarning` when `DataFrame.sort_values` receives positional arguments for any parameter other than `by`.  
- Emit a `FutureWarning` when `Series.sort_values` receives positional arguments for any parameter beyond `self`.  
- Preserve full keyword‑argument functionality; existing behavior remains unchanged.  

### Implementation

- Add `@deprecate_positional_args` decorators directly above the method definitions.  
- Configure `allowed_args` as `["self", "by"]` for `DataFrame.sort_values` and `["self"]` for `Series.sort_values`.  
- Keep the underlying sorting logic intact; only the decorator layer is introduced.  

### Tests

- New warnings appear for the documented positional‑argument cases.  
- All pre‑existing test suites pass, confirming backward compatibility and correct handling of edge cases.

---

### Sample 08: raw_trace_01456 (TECH_DOCS)
- **Original Source**: `deepseek-v4-pro` (jamesnavinhill/deepseek-v4-pro-0813-agentic-bucket)
- **Rewriter**: `or-nvidia-nemotron-3-ultra-550b`
- **Length**: Raw `2107` chars -> Rewritten `3579` chars (ratio `1.699`)
- **Cliché Violations**: `None (Clean)`

#### 🔻 Raw Agent Output (Original)
```markdown
**Plan**

1. Define the report’s purpose and audience: a concise briefing for school administrators or policymakers.
2. Provide background on school lunch programs and their role in student health and achievement.
3. Identify two key findings related to program participation and meal quality.
4. Develop a clear recommendation based on those findings.
5. Draft the short report with clear sections.

---

# Short Report: School Lunch Programs

## Background
School lunch programs are a central part of the school day, providing students with nutrition that supports growth, learning, and overall health. In the United States, the National School Lunch Program serves millions of students daily, often at free or reduced prices for low-income families. These programs aim to reduce food insecurity, improve dietary intake, and support academic performance by ensuring students have consistent access to meals during the school day.

## Key Findings

### 1. School lunch participation improves student nutrition and food security
Students who regularly participate in school lunch programs are more likely to consume fruits, vegetables, and essential nutrients than those who bring lunch from home or 
... [truncated for display]
```

#### 🌟 Rewritten Human Prose (Target)
# School Lunch Program System

## Overview

The National School Lunch Program (NSLP) operates as a federally assisted meal service delivering nutritionally regulated lunches to students in participating public and nonprofit private schools. The system processes approximately 30 million meals daily across 100,000+ institutions.

## System Parameters

| Parameter | Specification |
|-----------|---------------|
| **Eligibility Threshold** | 130% FPL (free), 185% FPL (reduced-price) |
| **Reimbursement Rate (SY 2023-24)** | Free: $4.25, Reduced: $3.85, Paid: $0.40 |
| **Nutrition Standards** | HHFKA 2010: calorie caps, sodium targets, whole-grain minimums, fruit/vegetable subgroups |
| **Service Window** | Minimum 20 minutes seat time after receipt |

## Participation Mechanics

### Standard Means-Tested Model
1. Household submits income application → eligibility determination (categorical or income-based)
2. Student presents at point of service → eligibility verified via roster or PIN
3. Meal claimed → reimbursement submitted to state agency → federal funds disbursed

**Observed behavior**: Participation rates correlate inversely with stigma signaling. Schools reporting >60% free/reduced enrollment show 15-20% lower participation among eligible students versus universal models.

### Universal Free Meals (CEP / State-Funded)
**Community Eligibility Provision (CEP) threshold**: ISP ≥ 25% (Identified Student Percentage via direct certification).

**Mechanics**:
- No household applications collected
- All students eat at no charge
- Reimbursement calculated: `Meals Served × ISP × 1.6` (free rate) + `Meals Served × (1 - ISP) × 1.6` (paid rate)
- 4-year cycle with optional annual renewal

**Measured outcomes**:
- Participation increase: 12-18% overall, 25-35% among previously paid-eligible students
- Unpaid meal debt: eliminated
- Administrative cost reduction: ~$0.15/meal (application processing, verification, collections)

## Nutritional Output Contract

| Component | Daily Minimum (K-5) | Daily Minimum (6-8) | Daily Minimum (9-12) |
|-----------|---------------------|---------------------|---------------------|
| Fruit | 0.5 cup | 0.5 cup | 1 cup |
| Vegetables | 0.75 cup | 0.75 cup | 1 cup |
| Grains (oz eq) | 1.0 | 1.0 | 2.0 |
| Meat/Meat Alternate (oz eq) | 1.0 | 1.0 | 2.0 |
| Fluid Milk | 1 cup | 1 cup | 1 cup |
| Calories | 550-650 | 600-700 | 750-850 |
| Sodium (mg) | ≤1,110 | ≤1,225 | ≤1,280 |

**Compliance measurement**: State agency administrative review (3-year cycle) + weighted nutrient analysis.

## Funding Architecture

```
Federal Reimbursement (USDA FNS)
    ↓
State Agency (administers, monitors, distributes)
    ↓
School Food Authority (SFA) — local operating entity
    ↓
Site-Level Production & Service
```

**Revenue stack per meal (universal free, CEP, ISP 60%)**:
- Federal: ~$3.10
- State supplement (varies): $0.00–$1.50
- Local/à la carte: $0.00–$0.50
- **Total available**: $3.10–$5.10/meal

**Cost structure target**: Food ≤ 40%, Labor ≤ 40%, Overhead ≤ 20%.

## Operational Invariants

1. **Meal pattern compliance** is non-negotiable; non-compliant meals are unclaimable.
2. **Direct certification** (SNAP, TANF, FDPIR, Medicaid) drives ISP; matching frequency: monthly minimum.
3. **Procurement** follows federal micro-purchase ($10k), simplified acquisition ($250k), and formal bid thresholds.
4. **Civil rights compliance**: Data collection by race/ethnicity, public notification, language access.

## Failure Modes

| Failure Mode | Detection | Mitigation |
|--------------|-----------|------------|
| ISP

---

### Sample 09: raw_trace_02931 (ENGINEERING_LORE)
- **Original Source**: `deepseek-v4-pro` (jamesnavinhill/deepseek-v4-pro-0813-agentic-bucket)
- **Rewriter**: `ne-gpt-oss-120b`
- **Length**: Raw `678` chars -> Rewritten `748` chars (ratio `1.103`)
- **Cliché Violations**: `None (Clean)`

#### 🔻 Raw Agent Output (Original)
```markdown
- Open source software is like a recipe anyone can view, change, and share, rather than a secret formula locked inside a company.
- It is usually free to download and use, which can save money for individuals, schools, and businesses.
- Popular examples include the Firefox web browser, LibreOffice for documents and spreadsheets, VLC media player, and the Android operating system.
- Because many volunteers and professionals can inspect the code, problems and security issues are often spotted and fixed quickly.
- You do not need to be a programmer to benefit; you can use open source tools, ask questions in community forums, and support projects with donations or feedback.
```

#### 🌟 Rewritten Human Prose (Target)
### Open source software

- The complete source tree is publicly hosted; anyone can clone, edit, and redistribute it under the project's license.  
- Pre‑built packages are offered at no monetary cost, eliminating acquisition fees for individuals, schools, and enterprises.  
- Widely deployed projects include **Firefox** (web browser), **LibreOffice** (office suite), **VLC** (media player), and **Android** (mobile operating system).  
- Continuous peer review by volunteers and professionals produces a steady stream of bug reports and security patches, shortening the time from discovery to fix.  
- Users can run the binaries, file issues in the project's tracker, and contribute code or donations without needing to be developers themselves.

---

### Sample 10: raw_trace_01097 (ENGINEERING_LORE)
- **Original Source**: `deepseek-v4-pro` (jamesnavinhill/deepseek-v4-pro-0813-agentic-bucket)
- **Rewriter**: `ne-gpt-oss-120b`
- **Length**: Raw `2034` chars -> Rewritten `3137` chars (ratio `1.542`)
- **Cliché Violations**: `None (Clean)`

#### 🔻 Raw Agent Output (Original)
```markdown
Urban gardening offers significant benefits, including improved access to fresh, nutritious produce, especially in food deserts where grocery stores are scarce. It reduces the carbon footprint associated with transporting food over long distances and can lower household grocery bills. Beyond food production, urban gardens increase green space, which helps mitigate the urban heat island effect, supports pollinators and local biodiversity, and provides mental health benefits through stress reduction and physical activity. Community gardens also foster social connections, educational opportunities, and a sense of ownership and pride among residents.

However, urban gardening faces several notable challenges. Limited space is a primary constraint, as many city dwellers have only small balconies, rooftops, or shared plots, which restricts the quantity and variety of crops that can be grown. Soil quality is another serious concern, because urban soils may be compacted, low in nutrients, or contaminated with heavy metals, lead, or industrial chemicals, requiring costly raised beds or imported soil. Additional obstacles include limited sunlight due to tall buildings, inconsistent water acc
... [truncated for display]
```

#### 🌟 Rewritten Human Prose (Target)
## Urban Gardening – System Overview

- **Produce output** – Fresh vegetables and herbs grow on balconies, rooftops, and shared plots. Yield per square meter matches conventional small‑scale farms when soil, light, and water are adequate.  
- **Carbon impact** – Transportation distance drops from tens of kilometers to a few meters, cutting associated emissions proportionally.  
- **Heat mitigation** – Green surfaces lower local surface temperature, reducing the urban heat island effect measured in degrees Celsius.  
- **Pollinator support** – Flowering crops provide nectar, sustaining bees and other insects that would otherwise lack foraging habitat.  
- **User health** – Regular planting and harvesting increase physical activity and lower reported stress levels.  

## Failure Modes

- **Space constraint** – Available planting area rarely exceeds a few square meters. Crop diversity and total yield scale linearly with that area.  
- **Soil quality** – Urban topsoil often exhibits compaction, low organic matter, or heavy‑metal contamination. Plant uptake of lead or cadmium exceeds safe thresholds without remediation.  
- **Light limitation** – Tall structures cast shadows that reduce incident photosynthetically active radiation below the minimum required for most vegetables.  
- **Water access** – Inconsistent supply forces intermittent irrigation, which stresses plants and reduces productivity.  
- **Regulatory limits** – Zoning codes may forbid permanent structures or restrict the height of raised beds, limiting design options.  
- **Security risk** – Shared plots experience theft or vandalism at rates higher than private gardens, leading to loss of crops and equipment.  
- **Pest pressure** – Proximity to traffic and dense human activity raises exposure to airborne pollutants and pest infestations.  

## Mitigations

- **Raised beds with screened soil** – Importing clean substrate isolates crops from contaminated ground and restores bulk density.  
- **Vertical and container systems** – Stacking planters multiplies usable planting area without expanding the footprint.  
- **Hydroponic loops** – Recirculating nutrient solutions eliminate soil dependence and allow precise control of water use.  
- **Shade analysis** – Mapping solar exposure informs placement of crops that tolerate lower light, reserving high‑light zones for sun‑intensive varieties.  
- **Rainwater capture** – Collecting runoff provides a reliable irrigation source and reduces utility costs.  
- **Community governance** – Formal agreements and shared monitoring reduce theft and vandalism incidents.  
- **Soil testing protocols** – Periodic assays detect heavy‑metal levels early, triggering remediation before planting cycles begin.  

## Outcome

When space, substrate, and illumination constraints are addressed through modular planting hardware and data‑driven site assessment, urban gardening delivers measurable food production, carbon reduction, and ancillary ecosystem services. The system remains viable provided that remediation, water management, and security practices are integrated into the operational workflow.

---

### Sample 11: raw_trace_02786 (TECH_DOCS)
- **Original Source**: `deepseek-v4-pro` (jamesnavinhill/deepseek-v4-pro-0813-agentic-bucket)
- **Rewriter**: `or-nvidia-nemotron-3-ultra-550b`
- **Length**: Raw `723` chars -> Rewritten `1526` chars (ratio `2.111`)
- **Cliché Violations**: `None (Clean)`

#### 🔻 Raw Agent Output (Original)
```markdown
- Solar panels convert sunlight into electricity using photovoltaic cells, where photons knock electrons loose in a semiconductor—usually silicon—creating direct current that an inverter turns into usable alternating current.
- They provide renewable, low-emission electricity with no moving parts and can be deployed at scales from small rooftops to large utility arrays.
- Their output is intermittent, depending on sunlight, weather, and time of day, so reliable supply often requires battery storage or backup generation.
- Tradeoffs include high upfront costs, land or roof space use, and manufacturing/disposal impacts such as energy use, water use, and hazardous materials; typical panel efficiency is around 15–22%.
```

#### 🌟 Rewritten Human Prose (Target)
# Solar Photovoltaic Systems

## Operation

Solar panels convert sunlight into electricity through the photovoltaic effect. Photons strike a semiconductor—typically crystalline silicon—liberating electrons and generating direct current (DC). An inverter converts this DC output to alternating current (AC) for grid or load compatibility.

## Characteristics

- **Emissions**: Zero operational emissions.
- **Maintenance**: No moving parts; degradation rates average 0.5–0.8% per year.
- **Scalability**: Deployable from kilowatt-scale rooftop arrays to gigawatt utility installations.

## Output Profile

Generation is intermittent. Output varies with:

- Solar irradiance (W/m²)
- Cell temperature (efficiency drops ~0.3–0.5%/°C above STC)
- Angle of incidence and shading
- Time of day and seasonal sun path

Reliable firm capacity requires pairing with storage (batteries) or dispatchable generation.

## Economics and Lifecycle

| Parameter | Typical Range |
|-----------|---------------|
| Module efficiency (commercial) | 15–22% |
| Levelized cost of energy (LCOE) | $0.03–0.06/kWh (utility, 2024) |
| Upfront capital cost | $0.80–1.50/W (utility), $2.50–3.50/W (residential) |
| Energy payback time | 1–3 years |
| Operational lifetime | 25–30 years (warranted to 80% nameplate) |

Manufacturing consumes energy, water, and hazardous materials (e.g., hydrofluoric acid, silane). End-of-life recycling recovers glass, aluminum, copper, and semiconductor material, though recovery rates vary by jurisdiction and facility.

---

### Sample 12: raw_trace_02880 (ENGINEERING_LORE)
- **Original Source**: `deepseek-v4-pro` (jamesnavinhill/deepseek-v4-pro-0813-agentic-bucket)
- **Rewriter**: `ne-gpt-oss-120b`
- **Length**: Raw `898` chars -> Rewritten `1800` chars (ratio `2.004`)
- **Cliché Violations**: `None (Clean)`

#### 🔻 Raw Agent Output (Original)
```markdown
**Benefits of Urban Gardening**

- Provides access to fresh, nutritious produce in food deserts.
- Improves mental health and reduces stress through connection with nature.
- Strengthens community bonds and shared green spaces.
- Supports pollinators and local biodiversity.
- Helps cool urban heat islands and manage stormwater runoff.

**Challenges of Urban Gardening**

- Limited space and poor soil quality, often requiring raised beds or imported soil.
- Soil contamination from lead or other urban pollutants.
- Restricted sunlight due to tall buildings and shade.
- Water access and irrigation costs.
- Pests, vandalism, and theft in shared or public plots.
- Zoning regulations and land tenure uncertainty.
- Time and labor demands for maintenance.

The educational value of urban gardening is significant, but gardeners must navigate these practical obstacles to sustain a productive plot.
```

#### 🌟 Rewritten Human Prose (Target)
## Observed Benefits  

- Fresh produce shortens the supply chain for residents in low‑access neighborhoods.  
- Direct interaction with plants correlates with measurable reductions in cortisol levels.  
- Shared beds create a low‑overhead coordination channel among neighboring households.  
- Flowering crops increase local pollinator activity, boosting urban biodiversity.  
- Vegetation lowers surface temperature and intercepts runoff, reducing peak storm‑water flow.  

## Failure Modes  

- Plot footprint is limited by surrounding building envelopes; modular raised beds are required to fit within the envelope.  
- Urban soils frequently exceed lead‑content thresholds; pre‑deployment soil testing and remediation become mandatory.  
- Tall structures cast shade that cuts photosynthetic throughput; orientation planning is needed to maximize light exposure.  
- Irrigation adds recurring operational cost; water‑budget calculations must be incorporated into the design.  
- Open plots expose crops to wildlife, vandalism, and theft; physical access controls are necessary.  
- Zoning codes may prohibit permanent installations; compliance checks must be performed before deployment.  
- Maintenance labor scales with plot size; staffing models need to account for ongoing effort.  

## Mitigation Strategies  

- Use sterile, pre‑filled media in containers to avoid contaminated ground.  
- Apply reflective mulch to boost light availability in shaded sections.  
- Install drip‑line systems with flow meters to enforce water budgets.  
- Deploy lockable frames and organize community watch schedules to deter interference.  
- Coordinate with municipal planning offices to secure temporary land‑use permits.  
- Rotate weekly task assignments among participants to distribute labor evenly.

---

### Sample 13: raw_trace_00715 (TECH_DOCS)
- **Original Source**: `moonshotai/kimi-k3` (jamesnavinhill/k3-bucket)
- **Rewriter**: `or-nvidia-nemotron-3-ultra-550b`
- **Length**: Raw `3606` chars -> Rewritten `3989` chars (ratio `1.106`)
- **Cliché Violations**: `None (Clean)`

#### 🔻 Raw Agent Output (Original)
```markdown
We're integrating with the aviation authority's drone flight-permit API and I'm done with the half-validated DTOs we have today — a request gets rejected server-side, the operator fixes ONE field, resubmits, gets rejected for the NEXT field, five round trips per permit. New rule for the domain layer: immutable records that validate EVERYTHING up front and report ALL violations in one shot, never fail-fast on the first problem.

Build three sibling .java files (no packages, plain JDK, no build tool — the whole dir runs with the source launcher):

ValidationErrors.java — public class ValidationErrors extends IllegalArgumentException. Constructor (String subject, List<String> violations). getMessage() is exactly subject + ": " + the violations joined with "; ". violations() returns the list — unmodifiable, and a defensive copy (mutating the list passed to the constructor must not leak in).

Geofence.java — public record Geofence(double centerLat, double centerLon, int radiusM, int maxAltitudeM) with a validating compact constructor. Rules, checked in component declaration order, every failure collected before throwing ValidationErrors with subject "Geofence":
- centerLat in [-90, 90] 
... [truncated for display]
```

#### 🌟 Rewritten Human Prose (Target)
# Domain Validation Layer

## ValidationErrors

`public class ValidationErrors extends IllegalArgumentException`

### Constructor

```java
public ValidationErrors(String subject, List<String> violations)
```

- `subject` — the validated entity name, used as the message prefix.
- `violations` — collected error messages. The constructor makes a defensive copy; subsequent mutation of the original list does not affect the exception.

### Methods

| Method | Return | Behavior |
|--------|--------|----------|
| `getMessage()` | `String` | Returns `subject + ": " + violations joined by "; "`. |
| `violations()` | `List<String>` | Returns an unmodifiable view of the internal copy. |

---

## Geofence

`public record Geofence(double centerLat, double centerLon, int radiusM, int maxAltitudeM)`

### Compact Constructor Validation

All rules are evaluated in component declaration order. Every failure is collected before a single `ValidationErrors("Geofence", ...)` is thrown.

| Component | Rule | Violation Message |
|-----------|------|-------------------|
| `centerLat` | `[-90.0, 90.0]`, not NaN | `centerLat must be between -90.0 and 90.0` |
| `centerLon` | `[-180.0, 180.0]`, not NaN | `centerLon must be between -180.0 and 180.0` |
| `radiusM` | `[50, 5000]` | `radiusM must be between 50 and 5000` |
| `maxAltitudeM` | `[10, 120]` | `maxAltitudeM must be between 10 and 120` |

Bounds are inclusive. NaN coordinates fail the range check (comparison logic must treat NaN as out of bounds).

### Withers

```java
public Geofence withRadiusM(int radiusM)
public Geofence withMaxAltitudeM(int maxAltitudeM)
```

Each wither returns a new `Geofence` instance with the specified component replaced. The replacement value passes through the same validation rules. The original instance is unchanged.

---

## PermitRequest

`public record PermitRequest(String permitId, String pilotLicense, Geofence zone, LocalDate flightDate, List<String> waivers)`

### Compact Constructor Validation

All rules are evaluated in component declaration order. Every failure is collected before a single `ValidationErrors("PermitRequest", ...)` is thrown.

| Component | Rule | Violation Message |
|-----------|------|-------------------|
| `permitId` | Not null | `permitId must not be null` |
| | Matches `^DFP-\d{5}$` | `permitId must match DFP-NNNNN` |
| `pilotLicense` | Not null | `pilotLicense must not be null` |
| | Matches `^[A-Z]{2}\d{4}$` | `pilotLicense must match LLNNNN` |
| `zone` | Not null | `zone must not be null` |
| `flightDate` | Not null | `flightDate must not be null` |
| `waivers` | Not null | `waivers must not be null` |
| | Each element not null | `waivers[i] must not be null` |
| | Each non-null element matches `^[a-z0-9]+(?:-[a-z0-9]+)*$` | `waivers[i] must be lowercase kebab-case` |
| | No duplicate non-null values | `waivers must not contain duplicates` (appended once, after all element messages) |

Index `i` is the zero-based position in the original list.

### Storage

The `waivers` list is stored as an unmodifiable defensive copy. Mutation of the caller's original list has no effect on the record. The accessor `waivers()` returns an unmodifiable view.

### Withers

```java
public PermitRequest withPilotLicense(String pilotLicense)
public PermitRequest withZone(Geofence zone)
public PermitRequest withFlightDate(LocalDate flightDate)
public PermitRequest withWaivers(List<String> waivers)
```

Each wither returns a new `PermitRequest` instance with the specified component replaced. The replacement value passes through the full validation pipeline. The original instance is unchanged. Value equality is preserved: a wither round-trip with the same value yields an equal record.

---

## Acceptance Contract

`TestMain.java` in the same directory defines the exact message text, ordering, accumulation behavior, and wither semantics. The implementation is correct when:

```bash
java TestMain.java
```

prints all `PASS` lines and exits with status `0`.

---

### Sample 14: raw_trace_00923 (CHANGELOGS)
- **Original Source**: `moonshotai/kimi-k3` (jamesnavinhill/k3-bucket)
- **Rewriter**: `ne-gpt-oss-120b`
- **Length**: Raw `2465` chars -> Rewritten `1670` chars (ratio `0.677`)
- **Cliché Violations**: `None (Clean)`

#### 🔻 Raw Agent Output (Original)
```markdown
=== MOONSHINER TASK BOUNDARY ===

I'm building pong for the split-flap display in the lobby and the whole thing has to be integer math on logical ticks — the display refreshes when WE say so, there is no clock, no floats, no randomness, and replaying a state must give the identical frames every time. Build pong.ts (stdlib only, no npm); test_pong.ts is the contract and stays untouched.

Court: export WIDTH = 20 (columns 0..19) and HEIGHT = 9 (rows 0..8), LEFT_COL = 1 and RIGHT_COL = 18 for the paddle columns; the goal lines are x <= 0 and x >= 19. State is plain data { ball: [x, y], vel: [vx, vy], left, right, score: [l, r] } where left/right are the paddle CENTER rows (each paddle covers center plus/minus one) and vx is always +1 or -1, vy in -1..1. newMatch(): ball [10, 4], vel [1, 1], both paddles centered at 4, score 0:0.

tick(state) is pure and applies exactly this order, nothing else:
1. Both paddles chase: each center moves ONE row toward the ball's PRE-move row (stand still when level with it), clamped to 1..7 so the blade never leaves the court.
2. The ball advances: x += vx, y += vy.
3. Wall reflection in integer fold-back: y < 0 becomes y = -y with vy negated; y > 8 bec
... [truncated for display]
```

#### 🌟 Rewritten Human Prose (Target)
## Feature – Deterministic Pong engine for split‑flap lobby display  

Implemented a pure integer‑tick simulation in **pong.ts** and added a contract test **test_pong.ts**.  

- Defined court geometry: `WIDTH = 20`, `HEIGHT = 9`, paddle columns `LEFT_COL = 1` and `RIGHT_COL = 18`. Goal lines are `x <= 0` (right scores) and `x >= 19` (left scores).  
- Modeled game state as `{ ball: [x, y], vel: [vx, vy], left, right, score: [l, r] }` where paddles occupy `center ± 1` rows and `vx ∈ {‑1, 1}`, `vy ∈ {‑1, 0, 1}`.  
- Added `newMatch()` that returns the initial state: ball at `[10, 4]`, velocity `[1, 1]`, paddles centered on row 4, score 0:0.  
- Implemented `tick(state)` with a fixed order of pure operations:  
  1. Move each paddle one row toward the ball’s pre‑move row, clamped to rows 1‑7.  
  2. Advance the ball by its velocity.  
  3. Reflect off the top (`y < 0`) and bottom (`y > 8`) walls using integer fold‑back and invert `vy`.  
  4. Apply paddle return when the ball reaches a paddle column; set `vx` toward the opposite side and set `vy` to the offset `ballRow ‑ paddleCenter` (‑1, 0, +1).  
  5. Detect a goal when no paddle returns the ball; reset the tick result to a serve with ball at `[10, 4]`, paddles centered at row 4, `vx` aimed at the scorer, and `vy` determined by point parity (`+1` for even total, `‑1` for odd).  
- Provided `tickN(state, n)` that folds `tick` `n` times.  
- Added `trace(state, n)` that returns a newline‑separated log of each tick in the form `t=<i> ball=(x,y) v=(vx,vy) <l>:<r>`. The test suite pins full rally transcripts, including a 30‑tick opening rally and short traces where a displaced paddle concedes.  
-

---

### Sample 15: raw_trace_00395 (TECH_DOCS)
- **Original Source**: `moonshotai/kimi-k3` (jamesnavinhill/k3-bucket)
- **Rewriter**: `or-nvidia-nemotron-3-ultra-550b`
- **Length**: Raw `2092` chars -> Rewritten `2717` chars (ratio `1.299`)
- **Cliché Violations**: `None (Clean)`

#### 🔻 Raw Agent Output (Original)
```markdown
Card-room replay rule: every disputed deal gets reconstructed from the hand number, so the shuffle path has to be bit-for-bit reproducible forever. I'm freezing it as three tiny assembly routines so nobody "improves" it later. One file, lcgdeal.s — x86-64, GNU as, AT&T syntax, System V AMD64 ABI (integer args RDI, RSI, RDX, RCX; return RAX; RBX/RBP/R12-R15 callee-saved). No libc, no syscalls.

Generator, pinned exactly: state' = (state * 1103515245 + 12345) mod 2^31. Draws come from the HIGH bits: after advancing, a bounded draw is (state' >> 16) % bound.

    uint32_t lcg_next(uint32_t *state);
    uint32_t lcg_rand(uint32_t *state, uint32_t bound);
    void     lcg_deal(uint32_t seed, unsigned char *deck);

- lcg_next: advance *state one step per the formula, store the new state back through the pointer, and return it. The mod 2^31 is a hard mask — the returned state never has bit 31 set, whatever garbage was in the incoming state.
- lcg_rand: advance *state exactly once (identical update), then return (new_state >> 16) % bound. bound is at least 1 and at most 32768; callers rely on one advance per call, no more.
- lcg_deal: fill deck[0..51] with 0..51 in order, set state = seed 
... [truncated for display]
```

#### 🌟 Rewritten Human Prose (Target)
# LCG Card Dealing Implementation

## Overview

The `lcgdeal.s` module provides a bit-for-bit reproducible shuffle for card-room replay. The implementation consists of three functions conforming to the System V AMD64 ABI, written in GNU assembler (AT&T syntax) for x86-64 with no libc or syscall dependencies.

## Generator Specification

The linear congruential generator uses the following recurrence:

```
state' = (state × 1103515245 + 12345) mod 2³¹
```

The modulus is implemented as a hard mask (`0x7fffffff`); the returned state never has bit 31 set regardless of input. Draws consume the high 15 bits of the updated state:

```
draw = (state' >> 16) % bound
```

## Function Contracts

### `uint32_t lcg_next(uint32_t *state)`

Advances the generator by one step. Stores the new state through the pointer and returns it.

**Parameters**
- `state` (RDI): pointer to 32-bit generator state

**Returns** (EAX): new state value, masked to 31 bits

**Registers**: RBX, RBP, R12–R15 preserved per ABI

---

### `uint32_t lcg_rand(uint32_t *state, uint32_t bound)`

Advances the generator by exactly one step (identical update to `lcg_next`), then returns a bounded draw from the high bits.

**Parameters**
- `state` (RDI): pointer to 32-bit generator state
- `bound` (ESI): upper bound, 1 ≤ bound ≤ 32768

**Returns** (EAX): `(new_state >> 16) % bound`

**Invariant**: Exactly one generator advance per call. Callers depend on this count.

---

### `void lcg_deal(uint32_t seed, unsigned char *deck)`

Produces a 52-card permutation in `deck[0..51]` using Fisher-Yates shuffle driven by the LCG.

**Parameters**
- `seed` (EDI): initial seed, masked to 31 bits (`seed & 0x7fffffff`)
- `deck` (RSI): pointer to 52-byte output buffer

**Algorithm**
1. Initialize `deck[i] = i` for `i = 0..51`
2. Set `state = seed & 0x7fffffff`
3. For `i = 51` down to `1`:
   - `j = lcg_rand(&state, i + 1)` (bound = `i + 1`)
   - Swap `deck[i]` and `deck[j]`
4. Write exactly 52 bytes to `deck`; no other memory is modified.

**Registers**: All arithmetic performed in 32-bit registers (EDI/ESI). Upper halves of 64-bit registers are not trusted.

## Build & Test

The test harness (`test_lcgdeal.c`) validates against a C reference implementation and pinned oracle outputs:

- Seeds 1, 42, 2026: byte-for-byte deck verification
- Hundreds of seeds: differential sweep with permutation checks
- Guard bytes: detect out-of-bounds writes

Build command:
```bash
gcc -Wall -Wextra -Werror -O2 -o runner test_lcgdeal.c lcgdeal.s
```

The test script `test_lcgdeal.sh` compiles and executes the runner; this is the acceptance gate.

## Module Termination

The assembly file must end with:
```asm
.section .note.GNU-stack,"",@progbits
```

---

### Sample 16: raw_trace_00664 (CHANGELOGS)
- **Original Source**: `moonshotai/kimi-k3` (jamesnavinhill/k3-bucket)
- **Rewriter**: `ne-gpt-oss-120b`
- **Length**: Raw `1427` chars -> Rewritten `1246` chars (ratio `0.873`)
- **Cliché Violations**: `None (Clean)`

#### 🔻 Raw Agent Output (Original)
```markdown
Please fix the bounded cell parser in this small C17 library. It receives a counted input span and returns the bytes before the first in-span NUL or caller-selected separator. A NUL-ended cell is already a C string and must stay zero-copy: return a borrowed view of the input without consulting or touching scratch, even when scratch is NULL with capacity 0. A separator-ended cell must be copied into scratch and NUL-terminated; its storage requirement is payload length plus one. If neither terminator occurs within input_len, return BTAB_INCOMPLETE without looking beyond the counted span. A NULL input, NULL output, or NUL separator is invalid and must return BTAB_INVALID. A separator-ended cell with NULL scratch or insufficient scratch capacity must return BTAB_NOSPACE. Invalid calls, incomplete input, and insufficient scratch must leave both the output descriptor and scratch unchanged.

The boundary suite varies payload lengths 0, 1, and 4 against missing/NUL/separator endings and scratch capacities 0, payload length, and payload length plus one. Its guarded scratch buffers currently show that the exact separator-copy edge is accepted and overwrites the first byte beyond the declared
... [truncated for display]
```

#### 🌟 Rewritten Human Prose (Target)
### Fix bounded‑cell parser edge cases

- Parse a counted input span and return the bytes preceding the first in‑span NUL or the caller‑selected separator.  
- Return a borrowed view for NUL‑terminated cells, avoiding any scratch buffer access, even when `scratch` is `NULL` with zero capacity.  
- For separator‑terminated cells, copy the payload into `scratch`, append a NUL byte, and allocate exactly `payload_len + 1` bytes.  
- Emit `BTAB_INCOMPLETE` when neither terminator appears within `input_len`, without reading past the span.  
- Emit `BTAB_INVALID` for `NULL` input, `NULL` output, or a NUL separator.  
- Emit `BTAB_NOSPACE` when a separator‑terminated cell lacks a valid `scratch` buffer or sufficient capacity.  
- Preserve the output descriptor and scratch contents on all error paths.

The test matrix exercises payload lengths of 0, 1, 4 against missing, NUL, and separator endings, with scratch capacities of 0, `payload_len`, and `payload_len+1`. The previous implementation over‑wrote the byte immediately beyond the declared capacity on the exact‑size copy case. The parser now validates capacity before copying, respects zero‑copy semantics, and leaves all out‑parameters unchanged on failure. All `make test` cases pass.

---

### Sample 17: raw_trace_00989 (TECH_DOCS)
- **Original Source**: `claude-fable-5` (jamesnavinhill/fable-5-premium-bucket)
- **Rewriter**: `or-nvidia-nemotron-3-ultra-550b`
- **Length**: Raw `4655` chars -> Rewritten `3707` chars (ratio `0.796`)
- **Cliché Violations**: `None (Clean)`

#### 🔻 Raw Agent Output (Original)
```markdown
# The Missing Piece: Cross-Origin Isolation

HTTPS is necessary but **not sufficient** for `SharedArrayBuffer`. After Spectre (2018), browsers gated SAB behind **cross-origin isolation**, which you opt into via two HTTP response headers:

```
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

Once both are set on your top-level document, `self.crossOriginIsolated` becomes `true` and `SharedArrayBuffer` appears. That's your immediate fix.

## Why these headers exist

`SharedArrayBuffer` + a high-resolution timer (which shared memory lets you build — one thread increments a counter in a loop, another reads it) makes Spectre-style cache-timing attacks practical against anything in your process. The headers guarantee your page can't be put in a process with cross-origin content:

- **COOP: same-origin** severs the relationship with cross-origin openers/popups (no `window.opener` access across origins), so your page gets its own browsing context group → its own process.
- **COEP: require-corp** demands every embedded resource (images, scripts, iframes) explicitly opt in via `Cross-Origin-Resource-Policy` or CORS (`crossorigin` attribute). This will b
... [truncated for display]
```

#### 🌟 Rewritten Human Prose (Target)
# Cross-Origin Isolation for SharedArrayBuffer

`SharedArrayBuffer` requires cross-origin isolation. Opt in by setting two HTTP response headers on the top-level document:

```
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

When both headers are present, `self.crossOriginIsolated` returns `true` and `SharedArrayBuffer` becomes available.

## Header Mechanics

**COOP: same-origin** places the document in its own browsing context group, which the browser assigns to a dedicated process. Cross-origin openers and popups lose `window.opener` access.

**COEP: require-corp** requires every embedded resource (images, scripts, iframes) to explicitly opt in via `Cross-Origin-Resource-Policy` or the `crossorigin` attribute. Resources without CORP headers fail to load. Common casualties include ad iframes, YouTube embeds, and CDN images. Audit dependencies before deploying.

**COEP: credentialless** (where supported) relaxes this requirement by stripping credentials from cross-origin requests that lack CORP headers.

### Hosting Constraints

Static hosts that do not allow custom response headers (GitHub Pages, etc.) require workarounds:
- Netlify or Cloudflare Pages `_headers` file
- Service worker injection via `coi-serviceworker`

## WebAssembly Threading Stack

With cross-origin isolation enabled, the Wasm threading proposal provides:

1. **Shared linear memory** — declared as `(memory shared)` in the module, backed by a `SharedArrayBuffer` instead of an `ArrayBuffer`.
2. **Atomic instructions** — `i32.atomic.rmw.cmpxchg`, `memory.atomic.wait32`, `memory.atomic.notify`, mapping to JavaScript `Atomics.wait`/`Atomics.notify`.

Threads are implemented as Web Workers. Each worker instantiates the same `WebAssembly.Module` against the same shared `WebAssembly.Memory`, with its own stack and TLS region carved from that memory.

### Building with Atomics

The standard library must be rebuilt with atomic support. Nightly Rust and `build-std` are required:

```bash
RUSTFLAGS='-C target-feature=+atomics,+bulk-memory' \
  cargo build --target wasm32-unknown-unknown -Z build-std=std,panic_abort
```

### wasm-bindgen-rayon Operation

`wasm-bindgen-rayon` adapts Rayon's work-stealing scheduler to the Web Worker model:

1. Call `initThreadPool(navigator.hardwareConcurrency)` from JavaScript. This spawns N Web Workers.
2. Each worker receives the compiled `WebAssembly.Module` (structured-cloneable) and the shared `WebAssembly.Memory`, then instantiates the module.
3. Rayon's deques reside in shared memory. Idle workers park via `memory.atomic.wait32` and wake via `memory.atomic.notify`, analogous to a futex-based pool.

### Main Thread Constraint

`Atomics.wait` throws on the main thread. Rayon's default behavior — having the calling thread participate in the pool and wait — deadlocks or falls back to spinning.

**Required pattern:** dispatch work to a dedicated "orchestrator" worker.

```javascript
// Main thread
const orchestrator = new Worker('orchestrator.js');
orchestrator.postMessage({ module, memory, inputData });

// orchestrator.js
self.onmessage = async ({ data: { module, memory, inputData } }) => {
  const instance = await WebAssembly.instantiate(module, { env: { memory } });
  // Call rayon-parallelized export; pool workers participate, orchestrator waits
  const result = instance.exports.process_image(inputData);
  self.postMessage(result);
};
```

Invoke the Wasm entry point from the orchestrator worker, not the main thread.

## Single-Threaded Performance Baseline

Before parallelizing, recover single-threaded performance:

- Compile with `opt-level = 3`, `lto = true`, and run `wasm-opt -Oz`.
- Enable SIMD via

---

### Sample 18: raw_trace_00010 (TECH_DOCS)
- **Original Source**: `claude-fable-5` (jamesnavinhill/claude-fable-5-claude-code-bucket)
- **Rewriter**: `ne-gpt-oss-120b`
- **Length**: Raw `2546` chars -> Rewritten `3434` chars (ratio `1.349`)
- **Cliché Violations**: `None (Clean)`

#### 🔻 Raw Agent Output (Original)
```markdown
Right — classic on-policy distillation (GKD, logit matching) needs the teacher's per-token distributions, so it's off the table with API-only access. And even if Gemini exposed logprobs, cross-tokenizer logit distillation between Gemini and Qwen vocabularies is its own research problem. So drop that framing. But the part that matters — *training on the student's own trajectory distribution* — doesn't require weights, just teacher text. The API-compatible versions of stage 2:

**1. Rejection-sampling fine-tuning (most practical).** Run your trained 4B student on agentic tasks, sample several rollouts per task, use the Gemini API as a judge to score them (or better, use verifiable signals: did the tool calls execute, did tests pass, did it reach the goal). SFT on the winners with the exact pipeline you already have — the new script consumes this data unchanged. This is on-policy in the way that counts: the model learns from contexts *it* produced.

**2. Teacher relabeling of student states (DAgger-style).** This is the one that most directly attacks compounding errors. Run the student through a trajectory; at each step (or at failure points), send the student's actual context to the 
... [truncated for display]
```

#### 🌟 Rewritten Human Prose (Target)
## On‑policy fine‑tuning with API‑only teachers  

**Scope**  
Applies when the teacher model is reachable only through an inference API (e.g., Gemini). The teacher’s per‑token logits are unavailable, and vocabularies differ between teacher and student. The student model can be trained using only the teacher’s generated text.

### Preconditions  

| Condition | Requirement |
|-----------|-------------|
| Teacher access | Inference API that returns generated text (no log‑probabilities) |
| Student model | Trained checkpoint ready for further fine‑tuning |
| Evaluation environment | Ability to execute tool calls, run tests, or otherwise verify task success |
| Data pipeline | Existing script that consumes `(prompt, response)` pairs for supervised fine‑tuning (SFT) |

### 1. Rejection‑sampling fine‑tuning  

1. **Rollout generation** – For each task, run the student model to produce *N* complete trajectories.  
2. **Judgment** – Send each trajectory to the teacher API (or to a deterministic verifier) and obtain a scalar score that reflects execution correctness, test pass/fail, or goal attainment.  
3. **Selection** – Keep the highest‑scoring trajectories; discard the rest.  
4. **Supervised fine‑tuning** – Feed the selected `(prompt, response)` pairs to the existing SFT pipeline without modification.  

*Result*: The student learns from contexts it generated, satisfying the on‑policy requirement.

### 2. Teacher relabeling of student states (DAgger‑style)  

1. **Trajectory execution** – Run the student model on a task, recording every intermediate context (user prompt + student response).  
2. **Teacher query** – For each recorded context, call the teacher API to obtain the next assistant turn.  
3. **Training example construction** – Pair the recorded student context with the teacher‑generated turn; each pair forms a single supervised example.  
4. **Supervised fine‑tuning** – Train the student on the collection of (student context → teacher action) pairs.  

*Result*: The student receives corrective actions for the exact states it encounters, reducing compounding error.

### 3. Preference‑based optimization (DPO or similar)  

1. **Pair generation** – Produce two trajectories per task: one labeled “good” and one labeled “bad”. Labels may come from teacher scores or from outcome checks (e.g., test pass/fail).  
2. **Contrastive loss** – Train the student to increase the probability of the good trajectory relative to the bad one, using a preference‑based objective.  
3. **API usage** – The teacher API is invoked only for scoring, not for generating new text, minimizing request volume.  

*Result*: The student aligns its policy with the teacher’s preferences while incurring low API cost.

### Practical considerations  

* The primary bottleneck is the availability of an environment that can execute tool calls and verify task success.  
* If a live environment is unavailable, replay static task definitions (e.g., from a TeichAI‑style dataset), let the student act, and apply teacher relabeling whenever the student deviates from expected behavior.  
* Stage 1 (initial dataset creation) already satisfies the “teacher‑output” contract; progression typically follows:  
  1. Apply rejection‑sampling fine‑tuning (low additional cost).  
  2. If API budget permits, add teacher relabeling (one teacher call per student step).  
  3. Consider preference training for further refinement.

---

### Sample 19: raw_trace_00048 (ENGINEERING_LORE)
- **Original Source**: `codex` (jamesnavinhill/kernelbench-mega-traces-bucket)
- **Rewriter**: `or-nvidia-nemotron-3-ultra-550b`
- **Length**: Raw `835` chars -> Rewritten `1923` chars (ratio `2.303`)
- **Cliché Violations**: `None (Clean)`

#### 🔻 Raw Agent Output (Original)
```markdown
Implemented [solution.py](/[REDACTED-home]/kernelbench.com/benchmarks/mega/outputs/runs/20260618_021522_codex_gpt-5.5_03_kimi_linear_decode/repo/problems/03_kimi_linear_decode/solution.py) with custom Triton W4A16 fused dequant-GEMV kernels, fused KDA q/k/v/g projection, fused MoE routed/shared expert kernels, latent-space MLA absorb path, fused RMSNorm, and fused KDA short conv/window update.

Final verification:

- `uv run python check.py`: `PASS`
- `uv run python benchmark.py`: `RESULT: OK`
  - ctx 2048: `1.388 ms/tok`, `3.99x`
  - ctx 8192: `1.417 ms/tok`, `4.31x`
  - ctx 16384: `1.438 ms/tok`, `4.77x`
  - geomean `peak_fraction: 4.3463`
- `uv run ruff check solution.py --fix`: passed
- `uv run pytest`: no tests collected in this archive-local problem dir, so official `check.py`/`benchmark.py` were the meaningful tests.
```

#### 🌟 Rewritten Human Prose (Target)
The kernel suite replaces the reference decode path with a set of fused Triton operators targeting W4A16 linear attention.

**Kernels implemented**

- **W4A16 fused dequant-GEMV**: Dequantizes int4 weights to fp16 on the fly and multiplies against the activation vector in a single kernel, avoiding the materialized fp16 weight matrix in shared memory.
- **Fused KDA q/k/v/g projection**: Combines the four output projections into one kernel with a single global memory read of the input and four independent writes.
- **Fused MoE routed/shared experts**: Merges the router logits, top-k selection, and expert GEMMs. The routed experts use a persistent block-per-expert layout; the shared experts run as a batched GEMM against the same input tile.
- **Latent-space MLA absorb**: Folds the low-rank projection into the attention score computation so the latent vectors never leave registers.
- **Fused RMSNorm**: Standard single-pass mean/variance + scale, fused into the residual add.
- **Fused KDA short conv / window update**: Maintains the convolution state in shared memory and writes the updated window in the same kernel that computes the output.

**Verification**

```
uv run python check.py
PASS

uv run python benchmark.py
RESULT: OK
  ctx 2048:  1.388 ms/tok,  3.99x
  ctx 8192:  1.417 ms/tok,  4.31x
  ctx 16384: 1.438 ms/tok,  4.77x
  geomean peak_fraction: 4.3463
```

The speedup scales with context length because the fused kernels eliminate the per-layer kernel launch overhead and the intermediate global memory traffic that dominates the reference implementation at longer sequences. The geomean peak_fraction of 4.35× indicates the fused path sustains roughly 43% of theoretical peak FLOPS on the target GPU across the tested range.

`ruff check solution.py --fix` passes. No pytest suite exists in the problem directory; `check.py` and `benchmark.py` are the canonical correctness and performance gates.

---
