PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS financial_line_item (
    borrower_id TEXT NOT NULL,
    line_item_id TEXT PRIMARY KEY,
    company TEXT NOT NULL,
    period_year TEXT NOT NULL,
    template_section TEXT NOT NULL,
    line_item_name TEXT NOT NULL,
    line_item_type TEXT NOT NULL CHECK (line_item_type IN ('absolute', 'ratio', 'margin')),
    value REAL NOT NULL,
    unit TEXT,
    currency TEXT,
    is_derived INTEGER NOT NULL CHECK (is_derived IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_financial_line_item_borrower_period
    ON financial_line_item (borrower_id, period_year);

CREATE INDEX IF NOT EXISTS ix_financial_line_item_section_name
    ON financial_line_item (template_section, line_item_name);

CREATE TABLE IF NOT EXISTS financial_ratio (
    borrower_id TEXT NOT NULL,
    period_year TEXT NOT NULL,
    ratio_id TEXT PRIMARY KEY,
    ratio_name TEXT NOT NULL,
    formula TEXT NOT NULL,
    value REAL NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_financial_ratio_borrower_period
    ON financial_ratio (borrower_id, period_year);

CREATE TABLE IF NOT EXISTS processed_financials (
    borrower_id TEXT NOT NULL,
    company TEXT NOT NULL,
    borrower_region TEXT NOT NULL CHECK (borrower_region IN ('us', 'nonus')),
    statement_type TEXT NOT NULL,
    workflow_id TEXT NOT NULL,
    execution_id TEXT NOT NULL,
    period_year TEXT NOT NULL,
    source_metric_name TEXT,
    metric_name TEXT NOT NULL,
    metric_type TEXT NOT NULL CHECK (metric_type IN ('absolute', 'ratio', 'margin')),
    input_type TEXT NOT NULL CHECK (input_type IN ('direct', 'derived', 'derived_else_direct')),
    metric_value REAL NOT NULL,
    currency TEXT,
    unit TEXT,
    is_consolidated INTEGER NOT NULL CHECK (is_consolidated IN (0, 1)),
    yoy_change REAL,
    resolution_method TEXT NOT NULL CHECK (resolution_method IN ('direct', 'derived')),
    component_metrics TEXT,
    formula_note TEXT,
    numerator_metric TEXT,
    denominator_metric TEXT,
    source_field_code TEXT,
    direct_extraction_code TEXT,
    derivation_code TEXT,
    ratio_id TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (borrower_id, workflow_id, execution_id, period_year, metric_name, metric_type),
    FOREIGN KEY (ratio_id) REFERENCES financial_ratio (ratio_id)
);

CREATE INDEX IF NOT EXISTS ix_processed_financials_borrower_period
    ON processed_financials (borrower_id, period_year);

CREATE INDEX IF NOT EXISTS ix_processed_financials_execution
    ON processed_financials (workflow_id, execution_id);

CREATE INDEX IF NOT EXISTS ix_processed_financials_metric_lookup
    ON processed_financials (borrower_id, workflow_id, execution_id, period_year, metric_name);

CREATE INDEX IF NOT EXISTS ix_processed_financials_source_metric
    ON processed_financials (source_metric_name);

CREATE TABLE IF NOT EXISTS processed_financial_component_audit (
    borrower_id TEXT NOT NULL,
    workflow_id TEXT NOT NULL,
    execution_id TEXT NOT NULL,
    period_year TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_type TEXT NOT NULL CHECK (metric_type IN ('absolute', 'ratio', 'margin')),
    component_metric_name TEXT NOT NULL,
    component_source_metric_name TEXT,
    component_statement_type TEXT,
    source_system TEXT NOT NULL CHECK (source_system IN ('processed_financials', 'derived')),
    source_table_or_file TEXT,
    source_field_code TEXT,
    direct_extraction_code TEXT,
    derivation_code TEXT,
    resolution_method TEXT CHECK (resolution_method IN ('direct', 'derived')),
    component_value REAL,
    is_null INTEGER NOT NULL CHECK (is_null IN (0, 1)),
    status TEXT NOT NULL CHECK (status IN ('resolved', 'missing_metric', 'null_value', 'upstream_failed')),
    audit_note TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (
        borrower_id,
        workflow_id,
        execution_id,
        period_year,
        metric_name,
        metric_type,
        component_metric_name
    )
);

CREATE INDEX IF NOT EXISTS ix_component_audit_metric_lookup
    ON processed_financial_component_audit (
        borrower_id,
        workflow_id,
        execution_id,
        period_year,
        metric_name,
        metric_type
    );

CREATE INDEX IF NOT EXISTS ix_component_audit_status
    ON processed_financial_component_audit (status);



schema
########
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS financial_line_item (
    borrower_id TEXT NOT NULL,
    line_item_id TEXT PRIMARY KEY,
    company TEXT NOT NULL,
    period_year TEXT NOT NULL,
    template_section TEXT NOT NULL,
    line_item_name TEXT NOT NULL,
    line_item_type TEXT NOT NULL CHECK (line_item_type IN ('absolute', 'ratio', 'margin')),
    value REAL NOT NULL,
    unit TEXT,
    currency TEXT,
    is_derived INTEGER NOT NULL CHECK (is_derived IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_financial_line_item_borrower_period
    ON financial_line_item (borrower_id, period_year);

CREATE INDEX IF NOT EXISTS ix_financial_line_item_section_name
    ON financial_line_item (template_section, line_item_name);

CREATE TABLE IF NOT EXISTS financial_ratio (
    borrower_id TEXT NOT NULL,
    period_year TEXT NOT NULL,
    ratio_id TEXT PRIMARY KEY,
    ratio_name TEXT NOT NULL,
    formula TEXT NOT NULL,
    value REAL NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_financial_ratio_borrower_period
    ON financial_ratio (borrower_id, period_year);

CREATE TABLE IF NOT EXISTS processed_financials (
    borrower_id TEXT NOT NULL,
    company TEXT NOT NULL,
    borrower_region TEXT NOT NULL CHECK (borrower_region IN ('us', 'nonus')),
    statement_type TEXT NOT NULL,
    workflow_id TEXT NOT NULL,
    execution_id TEXT NOT NULL,
    period_year TEXT NOT NULL,
    source_metric_name TEXT,
    metric_name TEXT NOT NULL,
    metric_type TEXT NOT NULL CHECK (metric_type IN ('absolute', 'ratio', 'margin')),
    input_type TEXT NOT NULL CHECK (input_type IN ('direct', 'derived', 'derived_else_direct')),
    metric_value REAL NOT NULL,
    currency TEXT,
    unit TEXT,
    is_consolidated INTEGER NOT NULL CHECK (is_consolidated IN (0, 1)),
    yoy_change REAL,
    resolution_method TEXT NOT NULL CHECK (resolution_method IN ('direct', 'derived')),
    component_metrics TEXT,
    formula_note TEXT,
    numerator_metric TEXT,
    denominator_metric TEXT,
    source_field_code TEXT,
    direct_extraction_code TEXT,
    derivation_code TEXT,
    ratio_id TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (borrower_id, workflow_id, execution_id, period_year, metric_name, metric_type),
    FOREIGN KEY (ratio_id) REFERENCES financial_ratio (ratio_id)
);

CREATE INDEX IF NOT EXISTS ix_processed_financials_borrower_period
    ON processed_financials (borrower_id, period_year);

CREATE INDEX IF NOT EXISTS ix_processed_financials_execution
    ON processed_financials (workflow_id, execution_id);

CREATE INDEX IF NOT EXISTS ix_processed_financials_metric_lookup
    ON processed_financials (borrower_id, workflow_id, execution_id, period_year, metric_name);

CREATE INDEX IF NOT EXISTS ix_processed_financials_source_metric
    ON processed_financials (source_metric_name);

CREATE TABLE IF NOT EXISTS processed_financial_component_audit (
    borrower_id TEXT NOT NULL,
    workflow_id TEXT NOT NULL,
    execution_id TEXT NOT NULL,
    period_year TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_type TEXT NOT NULL CHECK (metric_type IN ('absolute', 'ratio', 'margin')),
    component_metric_name TEXT NOT NULL,
    component_source_metric_name TEXT,
    component_statement_type TEXT,
    source_system TEXT NOT NULL CHECK (source_system IN ('processed_financials', 'derived')),
    source_table_or_file TEXT,
    source_field_code TEXT,
    direct_extraction_code TEXT,
    derivation_code TEXT,
    resolution_method TEXT CHECK (resolution_method IN ('direct', 'derived')),
    component_value REAL,
    is_null INTEGER NOT NULL CHECK (is_null IN (0, 1)),
    status TEXT NOT NULL CHECK (status IN ('resolved', 'missing_metric', 'null_value', 'upstream_failed')),
    audit_note TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (
        borrower_id,
        workflow_id,
        execution_id,
        period_year,
        metric_name,
        metric_type,
        component_metric_name
    )
);

CREATE INDEX IF NOT EXISTS ix_component_audit_metric_lookup
    ON processed_financial_component_audit (
        borrower_id,
        workflow_id,
        execution_id,
        period_year,
        metric_name,
        metric_type
    );

CREATE INDEX IF NOT EXISTS ix_component_audit_status
    ON processed_financial_component_audit (status);
