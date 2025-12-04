import pytest
from nodeone.services.manager import ManagerService

def test_register_and_start_local_agent(qtbot):
    m = ManagerService()
    assert "local" in m.agents
    m.start_agent("local")
    import time
    time.sleep(0.2)
    m.stop_agent("local")
