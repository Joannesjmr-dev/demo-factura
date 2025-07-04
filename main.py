from app.configuracion import ConfiguracionApp
from app.gui_fix_v5 import InterfazNotas
from app.database_v2 import DatabaseManager

def main():
    config = ConfiguracionApp()
    db_config = config.get("database", "host"), config.get("database", "database"), config.get("database", "user"), config.get("database", "password")
    app = InterfazNotas()
    app.db = DatabaseManager(*db_config)
    app.run()

if __name__ == "__main__":
    main()
