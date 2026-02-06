"""Configuration management for Finlytics trading system."""
import os
from pathlib import Path
from typing import Literal
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Trading Configuration
    trading_mode: Literal["paper", "live"] = Field(default="paper")
    default_capital: float = Field(default=100000.0)
    max_position_size: float = Field(default=0.1)
    max_portfolio_risk: float = Field(default=0.02)
    
    # API Keys
    alpha_vantage_api_key: str = Field(default="")
    polygon_api_key: str = Field(default="")
    news_api_key: str = Field(default="")
    
    # Database
    database_url: str = Field(default="sqlite+aiosqlite:///./finlytics.db")
    
    # Redis
    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379)
    redis_db: int = Field(default=0)
    
    # Logging
    log_level: str = Field(default="INFO")
    log_file: str = Field(default="logs/finlytics.log")
    
    # Agent Configuration
    market_data_interval: int = Field(default=1)
    analysis_interval: int = Field(default=5)
    signal_interval: int = Field(default=10)
    risk_check_interval: int = Field(default=5)
    
    # Backtesting
    backtest_start_date: str = Field(default="2023-01-01")
    backtest_end_date: str = Field(default="2024-12-31")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
