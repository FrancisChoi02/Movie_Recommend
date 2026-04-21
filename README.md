# PLAN

## Goal
Build a deterministic and auditable Materiality Analysis engine that:
- reads processed financial metrics from the local financial database,
- applies the documented materiality rules exactly,
- outputs a stable list of material metrics for downstream causality and write-up agents,
- fits the workflow contract used by the multi-agent architecture.

## Why this work exists
The docs make the purpose clear:
- this agent is the first stage in the workflow,
- it must be deterministic,
- it must reuse the prior PoC business logic,
- it must be auditable,
- and it must produce output that downstream agents can trust.

This is not just a YoY calculator. It is a rules engine for deciding which financial metrics are materially important.

## Current baseline
### Existing inputs
- `financials.py`
  - reads processed financial spreads from SQLite,
  - filters by borrower and year range,
  - returns JSON content for downstream use.
- `materiality_assessment_tool.py`
  - fetches metric series,
  - parses YoY values,
  - applies rule logic,
  - outputs material metrics.

### Current issues
1. Margin logic does not match the business rule.
   - Current code uses margin YoY thresholds.
   - Required rule: a margin is material if its numerator metric is material.

2. Ratio logic does not match the business rule.
   - Current code uses ratio thresholds and latest ratio values.
   - Required rule: a ratio is material if one or more of its components are material.

3. The code does not yet expose a clean dependency map.
   - We need explicit links from absolute metrics to margins and ratios.

4. The current output is not yet clearly shaped as a workflow contract.
   - The architecture expects deterministic, structured, versioned payloads.

5. Unit tests are missing.
   - The requirement explicitly asks for Python 3.11 unit tests covering correctness and edge cases.

## Target solution
## 1. Data normalization layer
Create a clean internal representation for financial rows.

Each normalized record should contain:
- borrower name or borrower id,
- metric name,
- metric type,
- statement type,
- period year,
- raw metric value,
- raw YoY value,
- optional currency.

Rules:
- calculations use raw numeric values,
- display formatting is kept separate,
- record ordering must stay deterministic.

## 2. Canonical metric catalog
Define one clear mapping for supported metrics.

The catalog should describe:
- metric type: absolute, margin, ratio,
- whether a metric is always material,
- numerator dependency for margins,
- numerator and denominator dependencies for ratios,
- any formula notes needed for auditability.

Examples:
- `EBITDA Margin % -> EBITDA`
- `Operating Profit Margin % -> Operating Profit`
- `NFD / EBITDA -> Net Funded Debt + EBITDA`
- `TFD / TNW -> Total Ext. Funded Debt + Tangible Net Worth`

## 3. Absolute metric materiality engine
Implement the documented rules exactly.

### Rule A: always material metrics
Mark these as material without needing YoY calculation:
- Revenue
- Total Ext. Funded Debt
- Capital Expenditure

### Rule B: 5-year path
If at least 5 years of valid YoY history are available:
1. calculate or read the first four YoY changes,
2. compute mean and standard deviation from those first four values,
3. compare the latest YoY against the mean,
4. mark material if latest YoY is at least 1 standard deviation away,
5. also apply the absolute threshold rule to capture additional material metrics.

### Rule C: short-history path
If less than 5 years are available:
- mark material if latest YoY >= +10%, or latest YoY <= -10%.

### Special case
- Dividends use `(CY - PY) / PY`, not `/ ABS(PY)`.

## 4. Margin propagation engine
Replace threshold-based margin logic.

Required behavior:
- if the numerator absolute metric is material, the paired margin is material,
- otherwise the margin is not material.

Examples:
- if EBITDA is material, EBITDA Margin % is material,
- if Operating Profit is material, Operating Profit Margin % is material.

Margin YoY may still be stored for reporting, but it must not be the rule that decides materiality.

## 5. Ratio propagation engine
Replace threshold-based ratio logic.

Required behavior:
- a ratio is material if its numerator is material,
- or its denominator is material,
- otherwise it is not material.

Examples:
- if EBITDA is material, then `NFD / EBITDA` and `TFD / EBITDA` are material,
- if Tangible Net Worth is material, then `TFD / TNW` is material.

Ratio YoY is not required for materiality decisions.

## 6. Auditable output model
Each material metric should include:
- borrower name,
- metric name,
- metric type,
- statement type,
- latest YoY change if applicable,
- rule triggered,
- additional context.

`rule_triggered` must be explicit and stable.

Examples:
- `always_material`
- `absolute_sd_threshold`
- `absolute_10pct_threshold`
- `margin_from_numerator`
- `ratio_from_components`

`additional_context` should carry dependency trace when useful.

Examples:
- `numerator=EBITDA`
- `components=Net Funded Debt,EBITDA`

## 7. Workflow contract adapter
Add a serializer that returns a structured payload ready for the orchestrated workflow.

The payload should support fields like:
- `schemaVersion`
- `runId`
- `traceId`
- `asOfDate`
- `currency`
- `material_metrics`

This keeps the calculation engine pure and the transport layer thin.

## 8. Test strategy
Add Python 3.11 unit tests before or alongside the refactor.

### Required test groups
1. Absolute metrics
   - always-material metrics,
   - 5-year SD path,
   - short-history threshold path,
   - no valid YoY path.

2. Margin propagation
   - numerator material => margin material,
   - numerator not material => margin not material.

3. Ratio propagation
   - numerator material => ratio material,
   - denominator material => ratio material,
   - neither material => ratio not material.

4. Formula edge cases
   - negative prior-year dividends,
   - missing values,
   - percentage-string parsing,
   - stable ordering of results.

5. Contract serialization
   - output fields are present,
   - output order is deterministic,
   - rule names are stable.

## File-by-file implementation plan
| Step | File | Change |
|---|---|---|
| 1 | `materiality_assessment_tool.py` | Refactor into normalization, absolute rules, dependency propagation, and serialization units |
| 2 | `financials.py` | Expose raw numeric YoY cleanly for downstream calculation, not only formatted display strings |
| 3 | `tests/test_materiality_assessment.py` | Add rule and edge-case tests |
| 4 | `materiality_executor.py` or equivalent | Add thin workflow-facing adapter for structured contract output |
| 5 | parent README/index files | Update required folder indexes if files are added or changed |
| 6 | file headers | Update 3-line headers on modified code files as required by project instructions |

## Execution order
- [ ] Confirm canonical metric names and dependencies from the processed-financials document.
- [ ] Refactor the internal data model for typed, deterministic financial records.
- [ ] Rework absolute metric evaluation to match the documented business logic.
- [ ] Remove threshold-based margin materiality and replace it with numerator-based propagation.
- [ ] Remove threshold-based ratio materiality and replace it with component-based propagation.
- [ ] Improve output serialization for auditability and workflow integration.
- [ ] Add unit tests for correctness and edge cases.
- [ ] Validate deterministic ordering and stable rule labels.
- [ ] Update headers and README index files.
- [ ] Run review-for-bugs and simplify anything unnecessary.

## Technical decisions
| Decision | Choice | Reason |
|---|---|---|
| Calculation style | Pure deterministic Python | Required by architecture and auditability needs |
| Source of truth | Processed financial records from SQLite / Moody's-derived raw values | Matches requirement and current baseline |
| Margin materiality | Propagate from numerator | Required by business logic |
| Ratio materiality | Propagate from components | Required by business logic |
| YoY formatting | Separate from calculation | Prevents display concerns from polluting rules |
| Output format | Structured schema-friendly JSON payload | Needed for downstream workflow contracts |
| Test scope | Rule-driven unit tests | Required for correctness and regression safety |

## Risks
| Risk | Impact | Mitigation |
|---|---|---|
| Metric names in code do not exactly match the business docs | Wrong propagation behavior | Build a canonical metric map and test exact names |
| Existing DB stores formatted YoY values | Parsing errors or inconsistent comparisons | Normalize all YoY values into raw floats at one entry point |
| Missing helper modules referenced by current code | Refactor may fail or stall | Keep logic self-contained or add the smallest missing pieces explicitly |
| Ratio and margin dependencies are implicit | Hard-to-audit output | Make dependencies explicit in the metric catalog and output context |

## Done criteria
This work is done when:
- the rules in the docs are implemented exactly,
- margins and ratios are derived from metric dependencies instead of ad hoc thresholds,
- outputs are deterministic and auditable,
- unit tests cover the required business cases,
- the result can be wrapped cleanly by the Materiality Analysis Agent in the workflow.

#AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

# Processed Financials Guide

## Conclusion
The `Processed Financials` table is the business rulebook for the materiality engine. You should use it as the source for canonical metric names, metric types, derivation rules, materiality classification, and dependency mapping between absolute metrics, margins, and ratios.

## What this table is

| What it is | What it tells you | Why it matters |
|---|---|---|
| Metric catalog | The official list of supported financial metrics | Prevents wrong names and inconsistent logic |
| Formula map | How each metric is extracted or calculated | Lets you audit derived metrics like EBITDA and Net Funded Debt |
| Data lineage map | Whether a metric is direct, derived, or derived-else-direct | Tells the engine whether to read or calculate a metric |
| Materiality input sheet | Which metrics are always material and which need assessment | Drives the rule engine |
| Dependency graph | Which margins and ratios depend on which base metrics | Needed for propagation logic |

## How to read each column

| Column | Meaning | How to use it |
|---|---|---|
| `SCT Section` | Reporting section such as Income Statement, Balance Sheet, Cash Flow, Ratios | Use as `statement_type` or reporting section |
| `Metric` | Business-facing metric name | Treat this as the canonical metric name |
| `Metric type` | `absolute value`, `margin (%)`, or `ratio` | Maps directly to rule behavior |
| `Moody's OSF field code/formula` | Moody’s source field or formula | Useful for audit and source trace |
| `BvD Codes - Derivation` | How BvD/Orbis can derive the metric | Use when no direct field exists |
| `BvD Code - Direct Extraction` | Direct extraction code | Prefer this when it exists |
| `Simplified` | Plain-English formula | Best column for building the internal metric catalog |
| `Input type` | `Direct Only`, `Derived`, or `Derived else Direct` | Tells the loader/calculator which path to use |
| `To be included in SCT?` | Whether the metric is in scope | Use to filter supported metrics |
| `Materiality` | `Always material` or `Subject to materiality assessment (v3)` | Drives the first rule split |
| `Causality Assessment` | Whether downstream causality is needed | Used after materiality selection |
| `Formula/calc. used by BDO` | Human-readable formula | Use for validation and audit notes |

## What the table means in simple terms

| Metric kind | Example | What to do |
|---|---|---|
| Direct metric | Revenue, Interest Expense, Cash | Read directly from source when available |
| Derived absolute metric | Gross Profit, Tangible Net Worth, Net Funded Debt | Compute from component metrics if needed |
| Margin | EBITDA Margin %, Gross Profit Margin % | Do not decide materiality from its own YoY threshold; inherit from numerator metric |
| Ratio | NFD / EBITDA, TFD / EBITDA, TFD / TNW | Do not decide materiality from standalone thresholds; inherit from numerator or denominator materiality |

## The most important output from this table
The table gives you the dependency graph.

| Dependent metric | Depends on |
|---|---|
| Gross Profit Margin % | Gross Profit + Revenue |
| EBITDA Margin % | EBITDA + Revenue |
| Operating Profit Margin % | Operating Profit (Loss) + Revenue |
| Tangible Net Worth | Net Worth + IFAS |
| Net Funded Debt | Total Ext. Funded Debt + Cash + Mkt Securities |
| Free cashflow | Operating cashflow + Capital Expenditure + Dividends |
| Ext. Gearing (TFD/TNW) | Total Ext. Funded Debt + Tangible Net Worth |
| NFD / EBITDA | Net Funded Debt + EBITDA |
| TFD / EBITDA | Total Ext. Funded Debt + EBITDA |
| NOCF / Interest | Operating cashflow + Interest Expense (Net) |

## Which steps in `PLAN.md` use this table

| Plan step | Uses this table? | How |
|---|---|---|
| Step 1 — Data normalization layer | Yes | The table tells you which fields must be normalized: metric name, metric type, section, value, YoY, currency |
| Step 2 — Canonical metric catalog | Yes, heavily | This is the main source for names, types, formulas, direct/derived status, and dependencies |
| Step 3 — Absolute metric materiality engine | Yes | Use the `Materiality` column to split always-material metrics from rule-based metrics |
| Step 4 — Margin propagation engine | Yes | Use the formulas to map each margin back to its numerator metric |
| Step 5 — Ratio propagation engine | Yes | Use the formulas to map each ratio to its component metrics |
| Step 6 — Auditable output model | Yes | Include dependency trace and formula notes in `additional_context` |
| Step 7 — Workflow contract adapter | Indirectly | The contract payload carries results produced by rules defined from this table |
| Step 8 — Test strategy | Yes | Build tests from the formulas and dependency relationships in the table |

## How to use this table in code

| Task | What to build |
|---|---|
| Build canonical metric config | One Python mapping keyed by canonical metric name |
| Build always-material set | Example: `{"Revenue", "Total Ext. Funded Debt"}` based on confirmed business rules |
| Build margin dependency map | Example: `"EBITDA Margin %": "EBITDA"` |
| Build ratio dependency map | Example: `"NFD / EBITDA": ["Net Funded Debt", "EBITDA"]` |
| Build derivation notes | Store formula text for audit output |
| Build input strategy | Label each metric as `direct`, `derived`, or `direct_else_derived` |

## Suggested internal data shape

| Key | Example value |
|---|---|
| `metric_name` | `EBITDA Margin %` |
| `metric_type` | `margin` |
| `statement_type` | `Income Statement` |
| `input_type` | `derived_else_direct` |
| `always_material` | `False` |
| `numerator_metric` | `EBITDA` |
| `component_metrics` | `["EBITDA", "Revenue"]` |
| `formula_note` | `(EBITDA/Revenue) * 100` |

## How this connects to the current code

| File | Current role | What should change |
|---|---|---|
| `financials.py` | Reads rows from `Processed_Financials` and returns JSON | Keep it as the raw data access layer, but expose raw numeric YoY cleanly instead of only formatted percent strings |
| `materiality_assessment_tool.py` | Evaluates materiality | Should use canonical metric definitions driven by this table |
| `materiality_assessment_tool.py` margin logic | Uses margin thresholds | Replace with numerator-based propagation |
| `materiality_assessment_tool.py` ratio logic | Uses ratio thresholds and latest values | Replace with component-based propagation |

## Practical usage flow

| Phase | Input from this table | Output |
|---|---|---|
| Load | Canonical metric names and types | Clean normalized records |
| Evaluate absolutes | Always-material flag and YoY-eligible absolute metrics | Material absolute metrics |
| Propagate margins | Margin to numerator mapping | Material margins |
| Propagate ratios | Ratio to component mapping | Material ratios |
| Serialize | Formula and dependency notes | Auditable output for downstream agents |

## Simple example

| Metric | Table says | Engine should do |
|---|---|---|
| Revenue | Absolute, always material | Mark material immediately |
| EBITDA | Absolute, subject to assessment | Apply YoY rules |
| EBITDA Margin % | Margin = EBITDA / Revenue | If EBITDA is material, mark this margin material |
| NFD / EBITDA | Ratio = Net Funded Debt / EBITDA | If either Net Funded Debt or EBITDA is material, mark this ratio material |

## Short answer

| Question | Answer |
|---|---|
| How can I use this table? | Use it as the authoritative metric catalog, dependency map, and audit formula sheet |
| What does it explain? | It explains metric meaning, source, derivation, inclusion, and materiality handling |
| Which plan steps use it? | Mainly Steps 1 to 6, especially Steps 2 to 5 |
| How do I utilize it? | Convert it into a canonical Python config that drives normalization, materiality, propagation, and audit output |

#BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB



# Metric Derivation Guide

## Conclusion
Yes, you should treat `direct`, `derived`, and `derived_else_direct` differently. The safe approach is: **normalize names first, load all direct values you can trust, then derive the remaining metrics from canonical component metrics in a deterministic order**. `component_metrics` tells you which already-normalized metrics are needed to build a derived metric, and `formula_note` tells you the exact business formula you must apply. The `Formula/calc. used by BDO` column is useful as an audit and dependency-reference column, but it should not be the runtime source for canonical mapping or formula execution.

## What the `(B41)`, `(B7)`, `(B13)` tags mean

| Tag style | What it refers to | Example |
|---|---|---|
| `(B2)` | The metric listed on row 2 of the processed-financials table | `Revenue (B2)` means the `Revenue` row |
| `(B7)` | Another row reference inside the same sheet | `Operating Profit (B7)` means use the metric defined on row 7 |
| `(B13)` | A dependency pointer, not a source-system code | `Total Ext. Funded Debt (B13)` points to the row where that metric is defined |

Short answer: these are **cross-row references inside the BDO spreadsheet logic**, like spreadsheet cell-style labels for metric rows. They help a human trace formulas such as `Net Funded Debt (B15) / EBITDA (B5)` back to earlier metric definitions.

## Should the `Formula/calc. used by BDO` column be used in the process?

| Use case | Use it? | Why |
|---|---|---|
| Human audit / explanation | Yes | It is the clearest business-facing explanation of how BDO thinks about the metric |
| Dependency validation | Yes | The `(Bxx)` references help verify numerator and component links |
| Building `formula_note` | Yes | It is a good source for storing readable audit text |
| Runtime canonical mapping | No | Canonical mapping should be driven by exact metric names and an explicit alias dictionary |
| Runtime numeric calculation | No, not directly | The strings are human-readable, not a safe executable formula language |
| Primary dependency source | No | Prefer a structured metric catalog with explicit `component_metrics` and dependency fields |

So the right role is:
- use `Formula/calc. used by BDO` as an **audit/reference column**,
- use `Metric`, `Simplified`, `Input type`, and the explicit catalog you build from them as the **runtime source of truth**.

## Core rule

| Input type | Meaning | What to do |
|---|---|---|
| `direct` | The source should provide the metric directly | Read the direct value after name normalization |
| `derived` | The metric should be calculated from other metrics | Compute it from canonical component metrics |
| `derived_else_direct` | Prefer direct value if a trusted direct field exists, otherwise derive it | Try canonical direct extraction first, then fall back to formula-based calculation |

## The correct processing order

| Step | Action | Why |
|---|---|---|
| 1 | Normalize all raw source metric names into canonical names | Prevent duplicate or inconsistent identities |
| 2 | Load all trusted direct metrics into a canonical metric store | Gives you the base inputs for derivation |
| 3 | Resolve `derived_else_direct` metrics using direct value first if present | Matches the business rule in the table |
| 4 | Compute pure `derived` metrics from component metrics | These have no trusted direct source |
| 5 | Compute margins and ratios from already-resolved base metrics | These depend on the absolute metrics being available first |
| 6 | Mark missing metrics as unavailable if required components are missing | Prevents fake values and silent guessing |

## How to perform canonical mapping

| Step | Action | Output |
|---|---|---|
| 1 | Read raw rows from DB with original metric names preserved | Raw records |
| 2 | Trim whitespace and normalize harmless formatting only | Stable raw names |
| 3 | Check whether the raw name exactly matches a canonical metric in the catalog | Canonical metric immediately if exact match succeeds |
| 4 | If not exact, look up the raw name in an explicit alias dictionary | Canonical metric if approved alias exists |
| 5 | If one raw name could map to multiple metrics, reject it | Unresolved metric requiring review |
| 6 | If no exact match and no approved alias exist, reject it | Unresolved metric requiring review |
| 7 | Store both `source_metric_name` and `metric_name` | Auditable normalized record |

## Canonical mapping rules from `PLAN.md`

| Rule | Meaning |
|---|---|
| Exact names first | Prefer the official metric names from the processed-financials table |
| Explicit alias map only | Do not use fuzzy matching, substring matching, or nearest-name guessing |
| Separate mapping from derivation | Name normalization happens before any direct/derived decision |
| Canonical names drive dependencies | `component_metrics` must use the exact canonical names |
| Reject ambiguity | If the name is not clearly mapped, do not calculate with it |

## Example canonical mapping table

| Raw source name | Canonical metric name | Why this is safe |
|---|---|---|
| `Revenue` | `Revenue` | Exact match |
| `Turnover` | `Revenue` | Approved alias |
| `Operating Revenue` | `Revenue` | Approved alias |
| `Sales` | `Revenue` | Approved alias |
| `Interest Paid` | `Interest Expense (Net)` | Only if business validation confirms equivalence |
| `EBIT` | unresolved | Could mean a nearby but not identical metric |

## Should you get all direct metrics first?

| Answer | Reason |
|---|---|
| Yes | Most derived metrics depend on direct or already-resolved absolute metrics |
| Yes | It makes the pipeline deterministic and auditable |
| Yes | It avoids recalculating a metric when a trusted direct source already exists |

Short version: **direct metrics form the base layer**. Build that base first, then derive upward.

## What `component_metrics` does

`component_metrics` is the dependency list for a derived metric.

| Derived metric | `component_metrics` | Meaning |
|---|---|---|
| Gross Profit | `["Revenue", "Cost of Sales"]` | You need both values before you can compute it |
| EBITDA | `["Gross Profit", "Other Operating Expenses", "Depreciation"]` | The formula depends on these inputs |
| Net Funded Debt | `["Total Ext. Funded Debt", "Cash + Mkt Securities"]` | Subtract cash from debt |
| Free cashflow | `["Operating cashflow", "Capital Expenditure", "Dividends"]` | Add all components with source sign conventions |
| NFD / EBITDA | `["Net Funded Debt", "EBITDA"]` | Ratio depends on both resolved absolute metrics |

Use `component_metrics` to decide:
1. whether you have enough inputs to calculate the metric,
2. what must be computed first,
3. what to record in audit output.

## What `formula_note` does

`formula_note` is the exact calculation rule.

| Field | Purpose |
|---|---|
| `component_metrics` | Declares dependencies |
| `formula_note` | Declares how to combine them |

Example:

| Metric | `component_metrics` | `formula_note` |
|---|---|---|
| Gross Profit | `["Revenue", "Cost of Sales"]` | `Revenue - Cost of Sales` |
| EBITDA Margin % | `["EBITDA", "Revenue"]` | `(EBITDA / Revenue) * 100` |
| TFD / TNW | `["Total Ext. Funded Debt", "Tangible Net Worth"]` | `Total Ext. Funded Debt / Tangible Net Worth` |

So the rule is simple:
- `component_metrics` says **what inputs are required**,
- `formula_note` says **how to compute the result**.

## Recommended resolution strategy

| Case | Resolution rule |
|---|---|
| `direct` metric exists with canonical name | Use it |
| `derived_else_direct` metric exists directly with trusted canonical mapping | Use direct value |
| `derived_else_direct` metric not available directly | Derive from `component_metrics` using `formula_note` |
| `derived` metric | Always derive |
| required component missing | Mark unresolved, do not guess |

## Best internal model

| Field | Meaning |
|---|---|
| `metric_name` | Canonical business name |
| `input_type` | `direct`, `derived`, or `derived_else_direct` |
| `component_metrics` | Canonical dependencies |
| `formula_note` | Exact formula to use |
| `source_metric_name` | Original raw metric name from DB or source |
| `resolution_method` | `direct` or `derived` |
| `resolution_trace` | Why this value was accepted or computed |

## Example resolution flow

### Example 1: `derived_else_direct`

| Metric | Input type | Resolution |
|---|---|---|
| Gross Profit | `derived_else_direct` | If direct `Gross Profit` exists after canonical mapping, use it. Otherwise compute `Revenue - Cost of Sales`. |

### Example 2: pure `derived`

| Metric | Input type | Resolution |
|---|---|---|
| Net Funded Debt | `derived` | Compute `Total Ext. Funded Debt - Cash + Mkt Securities` based on the documented formula meaning `TFD - Cash` |

### Example 3: ratio

| Metric | Input type | Resolution |
|---|---|---|
| NFD / EBITDA | `derived` | First resolve `Net Funded Debt` and `EBITDA`, then divide |

## Important implementation rule
You should separate **name normalization** from **metric derivation**.

| Layer | Responsibility |
|---|---|
| Name normalization | Convert raw source names into canonical metric names |
| Metric resolution | Decide direct vs derived |
| Formula engine | Compute values using canonical dependencies |
| Audit layer | Record which method was used and why |

Do not mix fuzzy name matching into the derivation engine.

## What if the direct metric names are ambiguous?
This is the dangerous part. If the source metric name is only similar, you should **not guess at runtime**. Instead, build an explicit alias map.

| Bad approach | Why it is bad |
|---|---|
| Fuzzy match by string similarity | Can silently map the wrong metric |
| Contains-word matching | Breaks on similar finance labels |
| Picking the closest raw name automatically | Not auditable |

## Safe approach for ambiguous direct names

| Step | Action |
|---|---|
| 1 | Create a canonical alias dictionary |
| 2 | Map raw source names to one canonical metric name only |
| 3 | If a raw name maps to multiple meanings, reject it and flag it |
| 4 | Only allow derivation after canonical mapping is complete |

Example alias map:

| Raw source name | Canonical metric name |
|---|---|
| `Turnover` | `Revenue` |
| `Operating Revenue` | `Revenue` |
| `Sales` | `Revenue` |
| `Interest Paid` | `Interest Expense (Net)` only if business validation confirms equivalence |

## Rule for ambiguous names

| Situation | What to do |
|---|---|
| Exact canonical name exists | Use it |
| Known approved alias exists | Map it to canonical name |
| Similar name but no approved alias | Reject it as unresolved |
| One raw name could mean two different canonical metrics | Reject and escalate |

## Why exact canonical mapping matters
Because `component_metrics` depends on exact canonical names.

Example:
- if `component_metrics = ["Revenue", "Cost of Sales"]`
- but your DB stores `Turnover` and `COGS`
- then you must normalize them first into `Revenue` and `Cost of Sales`
- otherwise the derivation engine cannot work safely.

## Recommended pipeline

| Phase | Input | Output |
|---|---|---|
| Raw ingestion | DB/source rows | Raw normalized rows with original names preserved |
| Canonical mapping | Raw metric names + alias dictionary | Canonical metric names |
| Direct resolution | Canonical rows | Base direct metric store |
| Derived resolution | Base store + metric catalog | Calculated derived metrics |
| Margin/ratio resolution | Resolved absolute metrics | Calculated margins and ratios |
| Audit serialization | Resolved metrics + traces | Final output with method and dependencies |

## Recommended decision tree

| Question | Action |
|---|---|
| Is the metric canonical and direct? | Use direct value |
| Is the metric canonical and `derived_else_direct` with direct value present? | Use direct value |
| Is the metric canonical and `derived_else_direct` without direct value? | Derive it |
| Is the metric canonical and `derived`? | Derive it |
| Are component metrics missing? | Mark unresolved |
| Is the raw direct metric name only similar but not approved? | Reject and flag |

## Simple concrete examples

| Metric | Raw source availability | Correct behavior |
|---|---|---|
| Revenue | Source has `Turnover` | Use only if alias map says `Turnover -> Revenue` |
| Gross Profit | Source has no direct field | Derive from Revenue and Cost of Sales |
| EBITDA | Source has direct EBITDA field | For `derived_else_direct`, use direct field if approved |
| EBITDA Margin % | Source has direct margin but EBITDA is also available | If your business rule prefers resolved numerator propagation, use resolved logic consistently; do not mix threshold heuristics |
| NFD / EBITDA | Source has no direct ratio field | Compute after NFD and EBITDA are resolved |

## Practical design recommendation

| Recommendation | Why |
|---|---|
| Build a canonical metric registry | Central place for names, formulas, and dependencies |
| Build an alias registry separate from formulas | Keeps naming problems out of calculation logic |
| Resolve direct metrics first | Creates a stable base layer |
| Resolve derived absolute metrics second | Supports downstream ratio and margin logic |
| Resolve margins and ratios last | They depend on resolved absolutes |
| Keep an audit trail per metric | You need to explain whether a value came from direct extraction or derivation |

## Final answer

| Question | Answer |
|---|---|
| What do the `(Bxx)` tags mean? | They are row-reference labels inside the BDO spreadsheet logic, pointing to other metric rows in the same table |
| Should `Formula/calc. used by BDO` be used in the whole process? | Use it for audit notes, validation, and dependency checking, but not as the runtime formula engine or canonical mapping source |
| How do I get the correct value for `derived`? | Compute it from canonical `component_metrics` using `formula_note` |
| How do I get the correct value for `derived_else_direct`? | Use trusted direct value if present after canonical mapping; otherwise derive it |
| How are `component_metrics` and `formula_note` involved? | `component_metrics` defines dependencies; `formula_note` defines calculation logic |
| How do we perform canonical mapping? | Exact canonical name first, then explicit alias map, reject ambiguity, and only derive after mapping is complete |
| Should I get all direct metrics first? | Yes, that is the safest and cleanest order |
| What if direct metric names are ambiguous? | Do not guess. Normalize through an explicit alias map, and reject unresolved names |

#CCCCCCCCCCCCCCCCCCCCCCCCC