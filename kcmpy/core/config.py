"""Configuration management for KCM applications."""
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """Configuration manager with JSON persistence."""

    def __init__(self, app_name: str = "kcm_app", config_dir: Optional[str] = None):
        """
        Initialize config manager.
        
        Args:
            app_name: Application name for config file
            config_dir: Custom config directory (default: ~/.kcm/)
        """
        self.app_name = app_name
        
        # Determine config directory
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            home = Path.home()
            self.config_dir = home / ".kcm"
        
        # Create config directory if not exists
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Config file path
        self.config_file = self.config_dir / f"{app_name}.json"
        
        # Default config
        self.data: Dict[str, Any] = {}
        
        # Load existing config
        self.load()

    def load(self) -> bool:
        """
        Load config from file.
        
        Returns:
            True if loaded successfully, False otherwise
        """
        if not self.config_file.exists():
            return False
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            return True
        except (json.JSONDecodeError, IOError):
            return False

    def save(self) -> bool:
        """
        Save config to file.
        
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get config value.
        
        Args:
            key: Config key (supports dot notation: "section.key")
            default: Default value if key not found
        
        Returns:
            Config value or default
        """
        keys = key.split('.')
        value = self.data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value

    def set(self, key: str, value: Any) -> None:
        """
        Set config value.
        
        Args:
            key: Config key (supports dot notation: "section.key")
            value: Value to set
        """
        keys = key.split('.')
        data = self.data
        
        # Navigate to nested dict
        for k in keys[:-1]:
            if k not in data:
                data[k] = {}
            data = data[k]
        
        # Set value
        data[keys[-1]] = value

    def delete(self, key: str) -> bool:
        """
        Delete config value.
        
        Args:
            key: Config key (supports dot notation: "section.key")
        
        Returns:
            True if deleted, False if not found
        """
        keys = key.split('.')
        data = self.data
        
        # Navigate to parent dict
        for k in keys[:-1]:
            if k not in data:
                return False
            data = data[k]
        
        # Delete key
        if keys[-1] in data:
            del data[keys[-1]]
            return True
        
        return False

    def clear(self) -> None:
        """Clear all config data."""
        self.data = {}

    def get_all(self) -> Dict[str, Any]:
        """Get all config data."""
        return self.data.copy()

    def update(self, data: Dict[str, Any]) -> None:
        """
        Update config with dict.
        
        Args:
            data: Dictionary to merge into config
        """
        self._deep_update(self.data, data)

    def _deep_update(self, target: dict, source: dict) -> None:
        """Deep update dictionary."""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value

    def __repr__(self) -> str:
        return f"Config(app_name='{self.app_name}', file='{self.config_file}')"
