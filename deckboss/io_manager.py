"""I/O manager — routing input/output across channels."""
import os

class IOManager:
    """Manages input/output channels: terminal, Telegram, Discord, LAN API."""
    
    def __init__(self, config: dict):
        self.config = config
        self.io_config = config.get("io", {})
        self.channels = []
        self._setup_channels()
    
    def _setup_channels(self):
        """Initialize configured I/O channels."""
        # Terminal is always available
        self.channels.append({"type": "terminal", "active": True})
        
        # LAN API
        for ch in self.io_config.get("secondary", []):
            if ch.get("type") == "lan_api":
                self.channels.append({"type": "lan_api", "port": ch.get("port", 8080)})
    
    def get_primary(self) -> str:
        return self.io_config.get("primary", "terminal")
    
    def has_channel(self, channel_type: str) -> bool:
        return any(ch["type"] == channel_type for ch in self.channels)
    
    def send(self, message: str, channel: str = None):
        """Send a message to a specific channel."""
        if channel is None:
            channel = self.get_primary()
        
        if channel == "terminal":
            print(message)
        # Telegram and Discord coming in future versions
    
    def receive(self, channel: str = None) -> str:
        """Receive input from a channel."""
        if channel is None:
            channel = self.get_primary()
        
        if channel == "terminal":
            return input("> ")
        return ""
