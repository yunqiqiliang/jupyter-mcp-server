"""Application configuration settings."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    host: str = "localhost"
    port: int = 5432
    database: str = "jupyter_mcp"
    username: str = "postgres"
    password: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        """Create configuration from environment variables."""
        return cls(
            host=os.getenv('DB_HOST', cls.host),
            port=int(os.getenv('DB_PORT', cls.port)),
            database=os.getenv('DB_NAME', cls.database),
            username=os.getenv('DB_USER', cls.username),
            password=os.getenv('DB_PASSWORD')
        )


@dataclass
class AppConfig:
    """Application configuration settings."""
    debug: bool = False
    max_connections: int = 100
    timeout: int = 30
    log_level: str = "INFO"
    
    @classmethod
    def from_env(cls) -> 'AppConfig':
        """Create configuration from environment variables."""
        return cls(
            debug=os.getenv('DEBUG', '').lower() in ('true', '1', 'yes'),
            max_connections=int(os.getenv('MAX_CONNECTIONS', cls.max_connections)),
            timeout=int(os.getenv('TIMEOUT', cls.timeout)),
            log_level=os.getenv('LOG_LEVEL', cls.log_level)
        )