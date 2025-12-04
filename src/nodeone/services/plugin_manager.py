import importlib.util
import os
import traceback
from types import ModuleType
from typing import Dict, List, Optional
from PyQt6.QtWidgets import QWidget

class PluginSpec:
    def __init__(self, name: str, module: ModuleType, path: str):
        self.name = name
        self.module = module
        self.path = path

    def create_widget(self, event_bus) -> QWidget:
        """Expect plugin module to expose `create_plugin(event_bus)` returning QWidget"""
        if hasattr(self.module, "create_plugin"):
            return self.module.create_plugin(event_bus)
        # fallback: try class `Plugin`
        if hasattr(self.module, "Plugin"):
            cls = getattr(self.module, "Plugin")
            return cls(event_bus)
        raise RuntimeError(
            "Plugin module does not expose a create_plugin/event-compatible interface"
        )

class PluginManager:
    def __init__(self, plugins_dir: str = "plugins") -> None:
        self.plugins_dir = plugins_dir
        self._specs: Dict[str, PluginSpec] = {}

    def discover(self) -> List[str]:
        found = []
        if not os.path.isdir(self.plugins_dir):
            return found
        for entry in os.listdir(self.plugins_dir):
            full = os.path.join(self.plugins_dir, entry)
            # plugin may be a directory with plugin.py, or a single .py file
            if os.path.isdir(full):
                candidate = os.path.join(full, "plugin.py")
                if os.path.isfile(candidate):
                    try:
                        spec = self._load_module_from_path(entry, candidate)
                        self._specs[entry] = PluginSpec(entry, spec, candidate)
                        found.append(entry)
                    except Exception:
                        traceback.print_exc()
            elif entry.endswith(".py"):
                name = entry[:-3]
                try:
                    spec = self._load_module_from_path(name, full)
                    self._specs[name] = PluginSpec(name, spec, full)
                    found.append(name)
                except Exception:
                    traceback.print_exc()
        return found

    def _load_module_from_path(self, name: str, path: str) -> ModuleType:
        spec = importlib.util.spec_from_file_location(
            f"microfrontend.plugins.{name}", path
        )
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load plugin {name} at {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def get_spec(self, name: str) -> Optional[PluginSpec]:
        return self._specs.get(name)

    def list_plugins(self) -> List[str]:
        return list(self._specs.keys())
