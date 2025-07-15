from app.configuracion import ConfiguracionApp
from app.gui_fix_v5 import InterfazNotas
from app.database_v2 import DatabaseManager

def _create_database_manager(config_app: ConfiguracionApp) -> DatabaseManager:
    """
    Creates and configures a DatabaseManager instance based on application configuration.
    This function encapsulates the logic for extracting database credentials and
    instantiating the DatabaseManager, adhering to the Single Responsibility Principle.
    """
    db_host = config_app.get("database", "host")
    db_name = config_app.get("database", "database")
    db_user = config_app.get("database", "user")
    db_password = config_app.get("database", "password")
    return DatabaseManager(db_host, db_name, db_user, db_password)

def main():
    """
    Main entry point for the application.
    Orchestrates configuration loading, database setup, and GUI initialization.
    This function acts as the 'Composition Root' of the application,
    wiring together all the necessary components.
    """
    # 1. Load application configuration
    config_app = ConfiguracionApp()

    # 2. Initialize database manager
    # The database manager is created independently, promoting modularity.
    database_manager = _create_database_manager(config_app)

    # 3. Initialize GUI and inject dependencies
    # The GUI application is instantiated, and its dependency (database_manager)
    # is explicitly injected. While direct attribute assignment is used here
    # due to external class constraints, this makes the dependency clear.
    gui_app = InterfazNotas()
    gui_app.db = database_manager

    # 4. Run the application
    gui_app.run()

if __name__ == "__main__":
    main()
