"""Initialize the local SQLite schema used for financial analysis storage."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def get_repo_root() -> Path:
    """Return the repository root from the utils directory."""
    return Path(__file__).resolve().parents[1]


def get_schema_path() -> Path:
    """Return the SQLite schema file path."""
    return Path(__file__).resolve().with_name("sql_create_tables_schema_sqlite.sql")


def build_default_database_url() -> str:
    """Build the default SQLite database URL at the repository root."""
    database_path = get_repo_root() / "local_financial_analysis.db"
    return f"sqlite:///{database_path.as_posix()}"


def create_sqlite_engine(database_url: str | None = None) -> Engine:
    """Create a SQLAlchemy engine for the configured SQLite database."""
    resolved_database_url = database_url or build_default_database_url()
    if not resolved_database_url.startswith("sqlite:///"):
        raise ValueError("setup_sqlite.py only supports sqlite:/// database URLs.")
    return create_engine(resolved_database_url, future=True)


def read_schema(schema_path: Path | None = None) -> str:
    """Read the SQL schema file from disk."""
    resolved_schema_path = schema_path or get_schema_path()
    return resolved_schema_path.read_text(encoding="utf-8")


def apply_sqlite_schema(engine: Engine, schema_path: Path | None = None) -> None:
    """Apply the SQLite schema script through a SQLAlchemy-managed connection."""
    schema_sql = read_schema(schema_path)
    with engine.begin() as connection:
        driver_connection = connection.connection.driver_connection
        if not isinstance(driver_connection, sqlite3.Connection):
            raise TypeError("Expected a sqlite3 driver connection when applying the SQLite schema.")
        driver_connection.executescript(schema_sql)


def initialize_database(database_url: str | None = None, schema_path: Path | None = None) -> Engine:
    """Create an engine and ensure the SQLite schema exists."""
    engine = create_sqlite_engine(database_url)
    apply_sqlite_schema(engine, schema_path)
    return engine


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for database initialization."""
    parser = argparse.ArgumentParser(description="Initialize the local financial analysis SQLite database.")
    parser.add_argument(
        "--database-url",
        default=None,
        help="SQLAlchemy database URL. Defaults to a SQLite file at the repository root.",
    )
    return parser.parse_args()


def main() -> None:
    """Initialize the configured SQLite database and print the target URL."""
    args = parse_args()
    database_url = args.database_url or build_default_database_url()
    initialize_database(database_url=database_url)
    print(f"Initialized database schema at {database_url}")


if __name__ == "__main__":
    main()

setup_sqlite
############################


"""Insert Moody's financial line items into the local SQLite database."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any
from uuid import NAMESPACE_URL, uuid5

from setup_sqlite import initialize_database
from sqlalchemy import text

SECTION_NORMALIZER_RE = re.compile(r"[^a-z0-9]+")
UNIT_MAP = {
    "K": "thousand",
    "M": "million",
    "B": "billion",
    "T": "trillion",
    "%": "percent",
    "x": "multiple",
}


def get_repo_root() -> Path:
    """Return the repository root from the src/sql directory."""
    return Path(__file__).resolve().parents[2]


def get_moodys_helper_path() -> Path:
    """Return the folder containing the Moody's Smart API helper scripts."""
    return get_repo_root() / "docs" / "development" / "moodys"


def add_moodys_helper_path() -> None:
    """Add the Moody's helper directory to sys.path for local script imports."""
    helper_path = str(get_moodys_helper_path())
    if helper_path not in sys.path:
        sys.path.insert(0, helper_path)


def import_moodys_api_helpers() -> tuple[Any, Any]:
    """Import the Moody's entity lookup and structured financial helper functions."""
    add_moodys_helper_path()
    from smart_apis import find_entity, get_structured_financial

    return find_entity, get_structured_financial


def normalize_identifier(value: str) -> str:
    """Normalize identifiers for case-insensitive comparisons."""
    return value.strip().lower()


def iter_dicts(payload: Any) -> list[dict[str, Any]]:
    """Collect every dictionary nested inside an arbitrary payload."""
    found: list[dict[str, Any]] = []
    if isinstance(payload, dict):
        found.append(payload)
        for item in payload.values():
            found.extend(iter_dicts(item))
        return found
    if isinstance(payload, list):
        for item in payload:
            found.extend(iter_dicts(item))
    return found


def extract_entity_id(find_entity_response: dict[str, Any], orbis_id: str) -> str:
    """Extract the best matching Moody's entity ID from a findEntity response."""
    normalized_orbis_id = normalize_identifier(orbis_id)

    for item in iter_dicts(find_entity_response):
        candidate_orbis_id = item.get("orbisId") or item.get("orbis_id")
        candidate_entity_id = item.get("entityId") or item.get("entity_id")
        if isinstance(candidate_orbis_id, str) and isinstance(candidate_entity_id, str):
            if normalize_identifier(candidate_orbis_id) == normalized_orbis_id:
                return candidate_entity_id

    for item in iter_dicts(find_entity_response):
        candidate_entity_id = item.get("entityId") or item.get("entity_id")
        if isinstance(candidate_entity_id, str) and candidate_entity_id.strip():
            return candidate_entity_id

    raise ValueError("Unable to resolve a Moody's entity ID from the findEntity response.")


def extract_company_name(find_entity_response: dict[str, Any]) -> str | None:
    """Extract the best available company name from a findEntity response."""
    candidate_keys = ("displayName", "entityName", "name", "companyName")

    for item in iter_dicts(find_entity_response):
        for key in candidate_keys:
            candidate_name = item.get(key)
            if isinstance(candidate_name, str) and candidate_name.strip():
                return candidate_name.strip()

    return None


def resolve_entity_id(entity_id: str | None, orbis_id: str | None) -> str:
    """Resolve the canonical Moody's entity ID from either direct input or an Orbis ID."""
    if entity_id:
        return entity_id.strip()
    if not orbis_id:
        raise ValueError("Either entity_id or orbis_id must be provided.")

    find_entity, _ = import_moodys_api_helpers()
    find_entity_response = find_entity(orbis_id_or_name=orbis_id)
    return extract_entity_id(find_entity_response=find_entity_response, orbis_id=orbis_id)


def resolve_company_name(structured_financials: dict[str, Any], fallback_company: str | None = None) -> str:
    """Resolve the company name from structured financials or an earlier lookup."""
    company = structured_financials.get("company")
    if isinstance(company, str) and company.strip():
        return company.strip()
    if fallback_company and fallback_company.strip():
        return fallback_company.strip()
    raise ValueError("Unable to resolve company name from Moody's data.")


def normalize_section_name(section_name: str) -> str:
    """Normalize Moody's section names to lowercase snake case."""
    normalized = SECTION_NORMALIZER_RE.sub("_", section_name.strip().lower()).strip("_")
    return normalized or "unknown"


def build_line_item_id(
    borrower_id: str,
    period_year: str,
    template_section: str,
    line_item_name: str,
    line_item_type: str,
    currency: str | None,
    unit: str | None,
) -> str:
    """Build a stable UUID for a financial line item row."""
    identity = "|".join(
        [
            borrower_id,
            period_year,
            template_section,
            line_item_name,
            line_item_type,
            currency or "",
            unit or "",
        ]
    )
    return str(uuid5(NAMESPACE_URL, identity))


def normalize_cell_value(parsed_cell: dict[str, Any] | None) -> tuple[float, str | None, str, bool] | None:
    """Convert Moody's parsed cell metadata into storage-ready values."""
    if not parsed_cell:
        return None

    raw_value = parsed_cell.get("value")
    if not isinstance(raw_value, (int, float)):
        return None

    parsed_type = parsed_cell.get("type")
    parsed_unit = parsed_cell.get("unit")

    if parsed_type == "percentage":
        return float(raw_value), UNIT_MAP["%"], "margin", True
    if parsed_type == "multiple":
        return float(raw_value), UNIT_MAP["x"], "ratio", True
    if parsed_type in ("amount", "number"):
        normalized_unit = UNIT_MAP.get(parsed_unit, "units") if isinstance(parsed_unit, str) else "units"
        return float(raw_value), normalized_unit, "absolute", False

    return None


def build_financial_line_items(structured_financials: dict[str, Any], borrower_id: str, company: str) -> list[dict[str, Any]]:
    """Transform structured Moody's financials into financial_line_item rows."""
    sections = structured_financials.get("sections")
    if not isinstance(sections, dict):
        raise ValueError("Expected structured financial payload to contain a 'sections' dictionary.")

    line_items: list[dict[str, Any]] = []

    for section_name, account_map in sections.items():
        if not isinstance(section_name, str) or not isinstance(account_map, dict):
            continue

        template_section = normalize_section_name(section_name)

        for line_item_name, rows in account_map.items():
            if not isinstance(line_item_name, str) or not isinstance(rows, list):
                continue

            for row in rows:
                if not isinstance(row, dict):
                    continue

                currency = row.get("currency")
                normalized_currency = currency if isinstance(currency, str) and currency.strip() else None
                values = row.get("values")
                if not isinstance(values, dict):
                    continue

                for period_year, parsed_cell in values.items():
                    if not isinstance(period_year, str):
                        continue

                    normalized_cell = normalize_cell_value(parsed_cell if isinstance(parsed_cell, dict) else None)
                    if normalized_cell is None:
                        continue

                    value, unit, line_item_type, is_derived = normalized_cell
                    line_items.append(
                        {
                            "borrower_id": borrower_id,
                            "line_item_id": build_line_item_id(
                                borrower_id=borrower_id,
                                period_year=period_year,
                                template_section=template_section,
                                line_item_name=line_item_name,
                                line_item_type=line_item_type,
                                currency=normalized_currency,
                                unit=unit,
                            ),
                            "company": company,
                            "period_year": period_year,
                            "template_section": template_section,
                            "line_item_name": line_item_name,
                            "line_item_type": line_item_type,
                            "value": value,
                            "unit": unit,
                            "currency": normalized_currency,
                            "is_derived": int(is_derived),
                        }
                    )

    return line_items


def upsert_financial_line_items(database_url: str | None, line_items: list[dict[str, Any]]) -> int:
    """Insert or update financial line items in the configured database."""
    if not line_items:
        return 0

    engine = initialize_database(database_url=database_url)
    statement = text(
        """
        INSERT INTO financial_line_item (
            borrower_id,
            line_item_id,
            company,
            period_year,
            template_section,
            line_item_name,
            line_item_type,
            value,
            unit,
            currency,
            is_derived
        )
        VALUES (
            :borrower_id,
            :line_item_id,
            :company,
            :period_year,
            :template_section,
            :line_item_name,
            :line_item_type,
            :value,
            :unit,
            :currency,
            :is_derived
        )
        ON CONFLICT(line_item_id) DO UPDATE SET
            borrower_id = excluded.borrower_id,
            company = excluded.company,
            period_year = excluded.period_year,
            template_section = excluded.template_section,
            line_item_name = excluded.line_item_name,
            line_item_type = excluded.line_item_type,
            value = excluded.value,
            unit = excluded.unit,
            currency = excluded.currency,
            is_derived = excluded.is_derived
        """
    )

    with engine.begin() as connection:
        connection.execute(statement, line_items)

    return len(line_items)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the Moody's financial import script."""
    parser = argparse.ArgumentParser(description="Insert Moody's financial line items into SQLite.")
    identifier_group = parser.add_mutually_exclusive_group(required=True)
    identifier_group.add_argument("--entity-id", default=None, help="Canonical Moody's entity ID to load.")
    identifier_group.add_argument("--orbis-id", default=None, help="Orbis ID to resolve through Moody's findEntity.")
    parser.add_argument(
        "--period",
        action="append",
        dest="periods",
        default=None,
        help="Optional reporting period filter. Repeat the flag for multiple periods.",
    )
    parser.add_argument(
        "--database-url",
        default=None,
        help="SQLAlchemy database URL. Defaults to a SQLite file at the repository root.",
    )
    return parser.parse_args()


def main() -> None:
    """Resolve a Moody's entity, fetch financials, and upsert line items."""
    args = parse_args()
    fallback_company: str | None = None
    entity_id = args.entity_id.strip() if args.entity_id else None

    if entity_id is None:
        find_entity, _ = import_moodys_api_helpers()
        find_entity_response = find_entity(orbis_id_or_name=args.orbis_id)
        entity_id = extract_entity_id(find_entity_response=find_entity_response, orbis_id=args.orbis_id)
        fallback_company = extract_company_name(find_entity_response)

    _, get_structured_financial = import_moodys_api_helpers()
    structured_financials = get_structured_financial(entity_id=entity_id, periods=args.periods)
    company = resolve_company_name(structured_financials=structured_financials, fallback_company=fallback_company)
    line_items = build_financial_line_items(structured_financials=structured_financials, borrower_id=entity_id, company=company)
    inserted_count = upsert_financial_line_items(database_url=args.database_url, line_items=line_items)

    print(f"Inserted or updated {inserted_count} financial line items for borrower_id={entity_id}, company={company}")


if __name__ == "__main__":
    main()

sqlinsert
##########

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
