from crews.dev_crew import get_dev_crew
from memory import ShortTermMemory, LongTermMemory
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="AI Dev Team - Multi-Agent Development Crew")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    run_parser = subparsers.add_parser("run", help="Run a development task")
    run_parser.add_argument("task", type=str, help="Task description")
    run_parser.add_argument("--project", type=str, default="default", help="Project name")

    memory_parser = subparsers.add_parser("memory", help="Manage memory")
    memory_parser.add_argument("--clear", action="store_true", help="Clear all memory")
    memory_parser.add_argument("--list", action="store_true", help="List all projects")
    memory_parser.add_argument("--export", type=str, help="Export mind map for project")

    args = parser.parse_args()

    if args.command == "run":
        print(f"🚀 Starting task: {args.task}")
        print(f"📁 Project: {args.project}")

        short_term = ShortTermMemory()
        long_term = LongTermMemory()

        short_term.set_current_task(args.task)

        crew = get_dev_crew(args.task)
        result = crew.kickoff()

        print("\n" + "="*50)
        print("📤 OUTPUT")
        print("="*50)
        print(result)
        print("="*50)

        task_record = {
            "task": args.task,
            "project": args.project,
            "status": "completed"
        }
        short_term.add_task(task_record)

        long_term.add_project(args.project, {"features": [args.task]})
        long_term.add_learning(args.project, str(result))

        print("\n✅ Task completed!")

    elif args.command == "memory":
        long_term = LongTermMemory()

        if args.clear:
            print("Clearing all memory...")
            for project in long_term.get_all_projects():
                long_term.clear_project(project)
            print("✅ Memory cleared")

        elif args.list:
            projects = long_term.get_all_projects()
            if projects:
                print("📁 Projects in memory:")
                for p in projects:
                    print(f"  - {p}")
            else:
                print("No projects in memory")

        elif args.export:
            mind_map = long_term.get_mind_map(args.export)
            if mind_map:
                print(f"🧠 Mind map for {args.export}:")
                print(mind_map)
            else:
                print(f"No mind map found for project: {args.export}")

    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()