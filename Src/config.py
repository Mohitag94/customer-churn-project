"""
Shared configuration and path constants for the customer churn project.
"""

# load required packages...
from pathlib import Path


class Columns:
    """
    Key column names in the churn dataset.
    """

    PRIMARY_KEY: str = "CustomerID"
    TARGET: str = "Churn"


class Paths:
    """
    Resolves the project root relative to this file's location, then derives
    every other path from it as pathlib.Path objects.
    """

    # project's root directory
    ROOT_DIR: Path = Path(__file__).resolve().parent.parent

    # data
    DATA_DIR: Path = ROOT_DIR / "Data"
    RAW_DIR: Path = DATA_DIR / "Raw"
    RAW_CSV: Path = RAW_DIR / "train.csv"
    DB_FILE: Path = DATA_DIR / "customer_churn.duckdb"

    # sql
    SQL_DIR: Path = ROOT_DIR / "Sql"
    SCHEMA_FILE: Path = SQL_DIR / "00_schema.sql"

    # model
    MODELS_DIR: Path = ROOT_DIR / "Models"

    # output
    OUTPUTS_DIR: Path = ROOT_DIR / "Outputs"
    SQL_AGGREGATES_DIR: Path = OUTPUTS_DIR / "sql_aggregates"

    @classmethod
    def ensure_dirs(cls) -> None:
        """
        Create any output directories that don't exist yet (safe to call repeatedly).
        """
        for path in [cls.MODELS_DIR, cls.OUTPUTS_DIR, cls.SQL_AGGREGATES_DIR]:
            path.mkdir(parents=True, exist_ok=True)
