import subprocess
import sys
from pathlib import Path

def validate_tic_tac_toe_output(output: str) -> dict:
    results = {
        "has_react_components": False,
        "has_game_logic": False,
        "has_board_rendering": False,
        "has_win_detection": False,
        "has_styling": False,
    }

    output_lower = output.lower()

    if "component" in output_lower or "jsx" in output_lower or "tsx" in output_lower:
        results["has_react_components"] = True

    if "state" in output_lower or "useState" in output_lower or "useeffect" in output_lower:
        results["has_game_logic"] = True

    if "board" in output_lower or "grid" in output_lower or "cell" in output_lower:
        results["has_board_rendering"] = True

    if "win" in output_lower or "winner" in output_lower or "checkwinner" in output_lower:
        results["has_win_detection"] = True

    if "css" in output_lower or "style" in output_lower or "tailwind" in output_lower:
        results["has_styling"] = True

    return results

def main():
    print("="*60)
    print("🧪 Tic Tac Toe Test - AI Dev Team Validation")
    print("="*60)

    print("\n📋 Test Plan:")
    print("  1. Submit 'Build a tic tac toe game with React' task")
    print("  2. Verify all 5 agents interact properly")
    print("  3. Validate output contains game components")
    print("  4. Check test coverage")
    print("  5. Generate mind map of learned patterns")

    print("\n" + "="*60)
    print("⏳ This test will be run when you start the crew with:")
    print("   python main.py run \"Build a tic tac toe game with React\"")
    print("   or via the web GUI at http://localhost:8501")
    print("="*60)

    return 0

if __name__ == "__main__":
    sys.exit(main())