"""
Service Layer Package
Exports the singleton Facade instance for application-wide use
"""

from app.services.facade import HBnBFacade

# Singleton instance of the Facade
# This ensures a single source of truth for all business operations
facade = HBnBFacade()