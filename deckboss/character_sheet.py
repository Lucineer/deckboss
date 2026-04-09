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
        """Show the character sheet."""
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel

        console = Console()

        console.print(Panel(
            f"[bold cyan]Deckboss[/] — [cyan]{self.profile}[/] — {self.role}",
            subtitle=self.hw.get("device", "Unknown device")))

        # Hardware
        hw = Table(title="Hardware")
        hw.add_column("Resource", style="bold")
        hw.add_column("Value")
        hw.add_row("Device", self.hw.get("device", "?"))
        hw.add_row("RAM", f"{self.hw.get('ram_gb', '?')} GB")
        gpu_val = self.hw.get("gpu_gb", 0)
        if gpu_val:
            mem_type = "shared" if self.hw.get("shared_memory") else "dedicated"
            hw.add_row("GPU", f"{gpu_val} GB ({mem_type})")
        else:
            hw.add_row("GPU", "CPU-only mode")
        hw.add_row("CUDA", str(self.hw.get("cuda", False)))
        hw.add_row("Storage", self.hw.get("storage", "~/.deckboss"))
        for k, v in self.hw.get("detected", {}).items():
            hw.add_row(k.capitalize(), str(v))
        console.print(hw)

        # Resource plan
        rp = Table(title="Resource Plan")
        rp.add_column("Setting", style="bold")
        rp.add_column("Value")
        rp.add_row("Engine", self.resources.get("model_engine", "ollama"))
        rp.add_row("Pipeline", self.resources.get("pipeline", self.resources.get("pipeline_mode", "serial")))
        max_gb = self.resources.get("max_model_gb", self.resources.get("max_gpu_model_size_gb", "?"))
        rp.add_row("Max Model", f"{max_gb} GB")
        console.print(rp)

        # Models
        if self.models:
            mt = Table(title="Models")
            mt.add_column("Role", style="bold")
            mt.add_column("Engine")
            mt.add_column("Source")
            mt.add_column("Model")
            mt.add_column("Priority")
            for role, cfg in sorted(self.models.items(), key=lambda x: x[1].get("priority", 99)):
                mt.add_row(role, cfg.get("engine", "?"), cfg.get("source", "?"),
                           cfg.get("model", "?"), str(cfg.get("priority", "?")))
            console.print(mt)

        # I/O
        iot = Table(title="I/O")
        iot.add_column("Channel", style="bold")
        iot.add_column("Type")
        iot.add_row("Primary", self.io.get("primary", "terminal"))
        for ch in self.io.get("secondary", []):
            iot.add_row(ch.get("type", "?"), str(ch.get("port", ch.get("env", ""))))
        console.print(iot)

    def get_primary_model(self) -> dict:
        if not self.models:
            return {}
        return min(self.models.values(), key=lambda m: m.get("priority", 99))

    def get_model_for_task(self, task: str) -> dict:
        """Select best model for a task type."""
        tl = task.lower()

        # Reasoning tasks → use reasoning model
        if any(w in tl for w in ["design", "plan", "architect", "analyze", "why", "how should"]):
            if "reasoning" in self.models:
                return self.models["reasoning"]

        # Quick tasks → use fast model
        if any(w in tl for w in ["quick", "simple", "summarize", "short"]):
            if "fast" in self.models:
                return self.models["fast"]

        # STT
        if "transcribe" in tl or "speech" in tl:
            if "stt" in self.models:
                return self.models["stt"]

        return self.get_primary_model()

    def to_dict(self) -> dict:
        """Export as plain dict."""
        return {
            "hardware": self.hw,
            "resource_plan": self.resources,
            "models": self.models,
            "io": self.io,
            "profile": self.profile,
            "role": self.role,
        }

    @classmethod
    def from_file(cls, path: str) -> "CharacterSheet":
        """Load from YAML file."""
        import yaml
        with open(path) as f:
            return cls(yaml.safe_load(f) or {})
