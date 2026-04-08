"""Character sheet — hardware resource allocation and planning."""
import yaml

class CharacterSheet:
    def __init__(self, config: dict):
        self.config = config
        self.hw = config.get("hardware", {})
        self.resources = config.get("resource_plan", {})
        self.models = config.get("models", {})
        self.io = config.get("io", {})
        self.profile = config.get("profile", "unknown")
        self.role = config.get("role", "system-designer")
    
    def display(self):
        """Show the character sheet in a readable format."""
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        
        console = Console()
        
        console.print(Panel(
            f"[bold cyan]Deckboss v0.1.0[/] — {self.profile} — {self.role}",
            subtitle=self.hw.get("device", "Unknown device")
        ))
        
        # Hardware
        hw_table = Table(title="Hardware")
        hw_table.add_column("Resource", style="bold")
        hw_table.add_column("Value")
        hw_table.add_row("Device", self.hw.get("device", "Unknown"))
        hw_table.add_row("RAM", f"{self.hw.get('ram_gb', '?')} GB")
        hw_table.add_row("VRAM", f"{self.hw.get('vram_gb', 'N/A')} GB")
        hw_table.add_row("Storage", self.hw.get("storage", "~/.deckboss"))
        detected = self.hw.get("detected", {})
        if detected:
            for k, v in detected.items():
                hw_table.add_row(k, str(v))
        console.print(hw_table)
        
        # Resource plan
        rp_table = Table(title="Resource Plan")
        rp_table.add_column("Setting", style="bold")
        rp_table.add_column("Value")
        rp_table.add_row("Model Engine", self.resources.get("model_engine", "ollama"))
        rp_table.add_row("Pipeline", self.resources.get("pipeline_mode", "serial"))
        rp_table.add_row("Max GPU Model", f"{self.resources.get('max_gpu_model_size_gb', '?')} GB")
        console.print(rp_table)
        
        # Models
        if self.models:
            m_table = Table(title="Models")
            m_table.add_column("Role", style="bold")
            m_table.add_column("Engine")
            m_table.add_column("Source")
            m_table.add_column("Model")
            m_table.add_column("Priority")
            for role, cfg in sorted(self.models.items(), key=lambda x: x[1].get("priority", 99)):
                m_table.add_row(
                    role,
                    cfg.get("engine", "?"),
                    cfg.get("source", "?"),
                    cfg.get("model", "?"),
                    str(cfg.get("priority", "?"))
                )
            console.print(m_table)
        
        # I/O
        io_table = Table(title="Input/Output")
        io_table.add_column("Channel", style="bold")
        io_table.add_column("Type")
        io_table.add_row("Primary", self.io.get("primary", "terminal"))
        for sec in self.io.get("secondary", []):
            io_table.add_row(sec.get("type", "?"), str(sec))
        console.print(io_table)
    
    def get_primary_model(self) -> dict:
        """Get the highest-priority model configuration."""
        if not self.models:
            return {}
        return min(self.models.values(), key=lambda m: m.get("priority", 99))
    
    def get_model_for_task(self, task: str) -> dict:
        """Select the best model for a given task type."""
        task_lower = task.lower()
        
        # Reasoning tasks
        if any(w in task_lower for w in ["design", "plan", "architect", "reason", "analyze"]):
            if "reasoning" in self.models:
                return self.models["reasoning"]
        
        # Fast tasks
        if any(w in task_lower for w in ["quick", "simple", "chat", "summarize"]):
            if "fast" in self.models:
                return self.models["fast"]
        
        # STT
        if "transcribe" in task_lower or "speech" in task_lower:
            if "stt" in self.models:
                return self.models["stt"]
        
        # Default to primary
        return self.get_primary_model()
