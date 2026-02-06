"""Database manager for SQLAlchemy operations."""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.models.database import Base
from src.core.config import settings
from src.core.logger import log


class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self):
        self.engine = None
        self.session_factory = None
        
    async def initialize(self):
        """Initialize database connection and create tables."""
        log.info(f"Initializing database: {settings.database_url}")
        
        self.engine = create_async_engine(
            settings.database_url,
            echo=False,
            future=True
        )
        
        self.session_factory = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        # Create tables
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        log.info("Database initialized successfully")
    
    async def close(self):
        """Close database connections."""
        if self.engine:
            await self.engine.dispose()
            log.info("Database connections closed")
    
    def get_session(self) -> AsyncSession:
        """Get a new database session."""
        return self.session_factory()
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()


# Global database manager instance
db_manager = DatabaseManager()
