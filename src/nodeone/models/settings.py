import json
from typing import Any, Dict, List
from pathlib import Path
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class UIConfig(BaseModel):
    theme: str = "light"
    name: str = "NodeOne"
    width: int = 1000
    height: int = 700
    enabled_tabs: List[str] = ["dashboard", "plugins"]
    
class AgentConfig(BaseModel):
    pass

class AppSettings(BaseSettings):
    debug_mode: bool = False
    server_port: int = 8000
    ui: UIConfig = Field(default_factory=UIConfig)
    agents: List[str] = []
    
    model_config = SettingsConfigDict(
        env_nested_delimiter='__',
        extra="ignore",
    )
    
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: Any,
        env_settings: Any,
        dotenv_settings: Any,
        file_secret_settings: Any,
    ) -> tuple[Any, ...]:
        """
        Defines the order of configuration sources (from lowest to highest priority).
        """
        def load_home_config_dict() -> Dict[str, Any]:
            config_path = Path.home() / "config.json"
            if config_path.is_file():
                try:
                    with open(config_path, 'r') as f:
                        return json.load(f)
                except json.JSONDecodeError:
                    print(f"Warning: Could not decode JSON from {config_path}")
            return {}

        json_source_callable = lambda: load_home_config_dict()
        
        return (
            init_settings,
            dotenv_settings,
            json_source_callable,
            env_settings,
            file_secret_settings, # (highest priority)
        )
        
settings = AppSettings()