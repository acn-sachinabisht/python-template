# python-template

A modern Python project template with:
- Pre-commit hooks for code quality and security
- Ruff for linting and formatting
- Mypy for type checking
- Bandit for security checks
- Pytest for unit testing

## Getting Started

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up pre-commit hooks**
   ```bash
   pre-commit install
   pre-commit run --all-files
   ```

3. **Run tests**
   ```bash
   invoke tests
   ```

4. **Run the application**
   ```bash
   # For CLI mode
   invoke app
   # For GUI mode (if supported)
   invoke app --gui true
   ```

## Project Structure
```
src/         # Source code
  core/      # Core modules
    main.py  # Main entry point

 tests/      # Unit tests
 tasks.py    # Invoke tasks
 README.md   # Project info
 .pre-commit-config.yaml # Pre-commit hooks
```

## Code Quality
- Ruff and ruff-format auto-fix and lint your code.
- Mypy checks for type errors.
- Bandit scans for security issues.

## Usage
- Use `tasks.py` for automation (build, freeze, test, etc.)
- Run `invoke app` to execute the main script in CLI mode.
- Run `invoke app --gui true` to execute in GUI mode (if supported).

**Note:**
All command-line arguments passed to invoke tasks are strings. The `--gui` flag must be passed as `true` or `false` (case-insensitive), and is converted to a boolean in the code. Typer/Click-style boolean flags are not natively supported by invoke.

## License
MIT
