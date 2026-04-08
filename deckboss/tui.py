"""Terminal UI for Deckboss."""
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

from .session import Session

class DeckbossTUI:
    def __init__(self, config: dict, character_sheet):
        self.console = Console()
        self.config = config
        self.sheet = character_sheet
        self.session = Session(config, character_sheet)
        self.running = True
    
    def run(self):
        """Main TUI loop."""
        self.console.print(Panel(
            f"[bold amber]Deckboss[/] v0.1.0 — [cyan]{self.sheet.profile}[/] — {self.sheet.role}\n"
            f"[dim]{self.sheet.hw.get('device', 'Unknown')} | "
            f"{self.sheet.resources.get('model_engine', 'ollama')} | "
            f"{self.sheet.io.get('primary', 'terminal')}[/]"
        ))
        self.console.print("[dim]Type 'help' for commands, 'quit' to exit.[/]\n")
        
        while self.running:
            try:
                user_input = Prompt.ask("\n[bold amber]>[/]")
                if not user_input.strip():
                    continue
                
                if user_input.strip().lower() in ("quit", "exit", "q"):
                    self.console.print("[dim]Goodbye.[/]")
                    break
                
                if user_input.strip().lower() == "help":
                    self._show_help()
                    continue
                
                if user_input.strip().lower() == "status":
                    self.sheet.display()
                    continue
                
                if user_input.strip().lower() == "agents":
                    from .git_agent import list_agents
                    list_agents()
                    continue
                
                # Send to session for AI processing
                response = self.session.send(user_input)
                self.console.print(Markdown(response))
                
            except KeyboardInterrupt:
                self.console.print("\n[dim]Use 'quit' to exit.[/]")
            except EOFError:
                break
    
    def _show_help(self):
        self.console.print("""
[bold]Commands:[/]
  [cyan]help[/]     — Show this help
  [cyan]status[/]   — Display character sheet
  [cyan]agents[/]   — List equipped agents
  [cyan]pull <name>[/] — Pull an agent from profile
  [cyan]quit[/]     — Exit Deckboss

[bold]In conversation:[/]
  Just type naturally. Deckboss will use the best available model
  for your request. For system design, it will use reasoning models.
  For quick questions, it uses faster models.

[bold]Examples:[/]
  "I need bilge flood detection for a 42ft fishing vessel"
  "Help me design a sensor network for engine monitoring"
  "What agents are available in the marine profile?"
  "Explain the git-agent architecture"
        """)
