import os
import sys

EXCLUDED_DIRS = {"__pycache__", ".venv"}


def analyze_directory(root_path):
    total_files = 0
    total_lines = 0
    total_symbols = 0

    for root, dirs, files in os.walk(root_path):
        # Exclude unwanted directories
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for file in files:
            if not file.endswith(".py"):
                continue  # Only count Python files

            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    total_files += 1
                    total_lines += content.count("\n") + (1 if content else 0)
                    total_symbols += len(content)
            except Exception:
                continue

    return total_files, total_lines, total_symbols


if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    files, lines, symbols = analyze_directory(directory)

    print(f"Directory analyzed: {os.path.abspath(directory)}")
    print(f"Python files: {files}")
    print(f"Total lines: {lines}")
    print(f"Total symbols (characters): {symbols}")
