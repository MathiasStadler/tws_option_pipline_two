"""
Configuration management using pydantic-settings.
Loads from config.yaml, environment variables (TWS_*), and CLI args.
"""

from pathlib import Path
from typing import Optional, Dict, Any
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml


class IBKRConfig(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 7496
    readonly_port: int = 4002
    client_id_base: int = 1000
    market_data_type: int = 4
    connection_timeout: int = 15
    readonly: bool = True


class SpreadConfig(BaseSettings):
    default_width: int = 5
    default_max_margin: float = 1000.0
    default_min_credit: float = 0.80
    take_profit_pct: float = 0.30
    stop_loss_pct: float = 2.00


class FiltersConfig(BaseSettings):
    delta_min: float = -0.50
    delta_max: float = -0.10
    bid_min: float = 0.80
    max_dte: int = 45
    min_dte: int = 7
    require_5_point_strikes: bool = True


class LimitsConfig(BaseSettings):
    max_positions_per_symbol: int = 3
    max_total_margin_pct: float = 0.80
    max_open_orders: int = 20


class ScanningConfig(BaseSettings):
    max_strikes_per_chain: int = 5
    greeks_batch_sleep: float = 3.0
    mark_price_sleep: float = 2.0


class OrdersConfig(BaseSettings):
    default_type: str = "LMT"
    default_quantity: int = 1
    tif: str = "DAY"
    oca_type: int = 1
    sl_limit_buffer: float = 0.05


class OutputConfig(BaseSettings):
    directory: str = "./output"
    csv_prefix: str = "multi_symbol_top5"
    html_report: bool = True
    console_summary: bool = True


class LoggingConfig(BaseSettings):
    level: str = "WARNING"
    format: str = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    suppress_ib_insync: bool = True


class SymbolConfig(BaseSettings):
    exchange: str = "SMART"
    currency: str = "USD"
    trading_class: Optional[str] = None


class Settings(BaseSettings):
    ibkr: IBKRConfig = Field(default_factory=IBKRConfig)
    spread: SpreadConfig = Field(default_factory=SpreadConfig)
    filters: FiltersConfig = Field(default_factory=FiltersConfig)
    limits: LimitsConfig = Field(default_factory=LimitsConfig)
    scanning: ScanningConfig = Field(default_factory=ScanningConfig)
    orders: OrdersConfig = Field(default_factory=OrdersConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    symbols: Dict[str, SymbolConfig] = Field(default_factory=dict)

    # Runtime overrides (set via CLI, not from config file)
    dry_run: bool = False
    verbose: bool = False
    manual_mode: bool = False
    bracket_mode: bool = False
    order_type: Optional[str] = None
    bid_min: Optional[float] = None
    spread_mode: bool = False
    spread_width: Optional[int] = None
    max_margin: Optional[float] = None
    min_credit: Optional[float] = None
    delta_min: Optional[float] = None
    delta_max: Optional[float] = None
    num_chains: int = 0
    month_indices: list = Field(default_factory=list)
    exchange: Optional[str] = None
    currency: Optional[str] = None
    output_dir: Optional[str] = None

    model_config = SettingsConfigDict(
        env_prefix="TWS_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    @classmethod
    def from_yaml(cls, path: str = "config.yaml") -> "Settings":
        """Load settings from YAML file, then apply env vars."""
        yaml_path = Path(path)
        data = {}
        if yaml_path.exists():
            with open(yaml_path, "r") as f:
                data = yaml.safe_load(f) or {}
        return cls(**data)

    def get_symbol_config(self, symbol: str) -> SymbolConfig:
        """Get symbol config with fallback to defaults."""
        sym = symbol.upper()
        if sym in self.symbols:
            return self.symbols[sym]
        return SymbolConfig(exchange="SMART", currency="USD")

    def apply_cli_overrides(self, **kwargs) -> None:
        """Apply CLI argument overrides to settings."""
        for key, value in kwargs.items():
            if value is not None and hasattr(self, key):
                setattr(self, key, value)

        # Nested overrides
        if self.order_type:
            self.orders.default_type = self.order_type
        if self.bid_min is not None:
            self.filters.bid_min = self.bid_min
        if self.spread_width is not None:
            self.spread.default_width = self.spread_width
        if self.max_margin is not None:
            self.spread.default_max_margin = self.max_margin
        if self.min_credit is not None:
            self.spread.default_min_credit = self.min_credit
        if self.delta_min is not None:
            self.filters.delta_min = self.delta_min
        if self.delta_max is not None:
            self.filters.delta_max = self.delta_max
        if self.output_dir:
            self.output.directory = self.output_dir


@lru_cache
def get_settings(config_path: str = "config.yaml") -> Settings:
    """Cached settings loader."""
    return Settings.from_yaml(config_path)


def reset_settings_cache():
    """Clear cache for testing."""
    get_settings.cache_clear()