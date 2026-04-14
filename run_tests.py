import subprocess
import sys
import os

if __name__ == "__main__":
    # Ensure we are in the project root
    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_dir)

    # Path to the actual runner
    runner_path = os.path.join("tests", "run_tests.py")

    if not os.path.exists(runner_path):
        print(f"Error: Could not find test runner at {runner_path}")
        sys.exit(1)

    # Execute the actual runner with same arguments
    cmd = [sys.executable, runner_path] + sys.argv[1:]
    result = subprocess.run(cmd)
    sys.exit(result.returncode)
