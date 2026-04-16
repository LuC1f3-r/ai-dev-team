import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crews.dev_crew import get_dev_crew
from memory import ShortTermMemory, LongTermMemory
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown

console = Console()

AGENTS = ["Manager", "Senior Dev", "Frontend Dev", "Backend Dev", "Tester"]

def show_banner():
    console.print("""
    ╔═══════════════════════════════════════════════════════╗
    ║     🤖  AI Dev Team - Interactive CLI                ║
    ║     Multi-Agent Development Crew                      ║
    ╚═══════════════════════════════════════════════════════╝
    """, style="bold cyan")

def show_status(short_term):
    table = Table(title="Agent Status", show_header=True, header_style="bold magenta")
    table.add_column("Agent", style="cyan")
    table.add_column("Status", style="white")

    agent_states = short_term.agent_states
    for agent in AGENTS:
        state = agent_states.get(agent.lower().replace(" ", "_"), "idle")
        table.add_row(agent, state)

    console.print(table)

def show_help():
    console.print("\n[bold]Available commands:[/bold]")
    console.print("  [cyan]task <description>[/cyan]  - Submit a new task")
    console.print("  [cyan]status[/cyan]              - Show agent status")
    console.print("  [cyan]memory[/cyan]              - Show memory info")
    console.print("  [cyan]projects[/cyan]            - List projects in memory")
    console.print("  [cyan]clear[/cyan]               - Clear session memory")
    console.print("  [cyan]help[/cyan]                - Show this help")
    console.print("  [cyan]exit[/cyan]                - Exit the CLI\n")

def main():
    show_banner()

    short_term = ShortTermMemory()
    long_term = LongTermMemory()

    console.print("[bold green]Welcome![/bold green] Type [cyan]help[/cyan] for available commands.\n")

    while True:
        try:
            user_input = Prompt.ask("\n[bold cyan]>[/bold cyan]")

            if not user_input:
                continue

            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else ""

            if command == "exit" or command == "quit":
                console.print("\n[bold yellow]Goodbye![/bold yellow] 👋\n")
                break

            elif command == "help":
                show_help()

            elif command == "task":
                if not arg:
                    console.print("[red]Please provide a task description[/red]")
                    continue

                console.print(f"\n🚀 [bold]Starting task:[/bold] {arg}")

                short_term.set_current_task(arg)

                for agent_name in ["manager", "senior", "frontend", "backend", "tester"]:
                    short_term.update_agent_state(agent_name, "waiting")

                short_term.update_agent_state("manager", "active")

                with console.status("[bold green]Crew working...") as status:
                    crew = get_dev_crew(arg)
                    result = crew.kickoff()

                console.print("\n[bold green]✅ Task completed![/bold green]\n")

                show_status(short_term)

                console.print("\n[bold]Output:[/bold]")
                console.print(Markdown(str(result)[:500] + "..." if len(str(result)) > 500 else str(result)))

                short_term.add_task({
                    "task": arg,
                    "status": "completed"
                })

                project_name = Prompt.ask("Project name for this task", default="default")
                long_term.add_project(project_name, {"features": [arg]})
                long_term.add_learning(project_name, str(result))

                console.print(f"[dim]Stored in project: {project_name}[/dim]")

            elif command == "status":
                show_status(short_term)

            elif command == "memory":
                memory_info = {
                    "session_id": short_term.session_id,
                    "current_task": short_term.current_task,
                    "context_keys": list(short_term.context.keys()),
                    "projects": long_term.get_all_projects()
                }
                console.print("\n[bold]Memory Info:[/bold]")
                for key, value in memory_info.items():
                    console.print(f"  [cyan]{key}[/cyan]: {value}")

            elif command == "projects":
                projects = long_term.get_all_projects()
                if projects:
                    console.print("\n[bold]Projects in memory:[/bold]")
                    for p in projects:
                        console.print(f"  - {p}")
                else:
                    console.print("[dim]No projects in memory[/dim]")

            elif command == "clear":
                if Confirm.ask("Clear session memory?"):
                    short_term.clear()
                    console.print("[green]Session cleared[/green]")

            else:
                console.print(f"[red]Unknown command: {command}[/red]")
                console.print("Type [cyan]help[/cyan] for available commands")

        except KeyboardInterrupt:
            console.print("\n\n[bold yellow]Interrupted. Type 'exit' to quit.[/bold yellow]")
        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {str(e)}\n")

if __name__ == "__main__":
    main()