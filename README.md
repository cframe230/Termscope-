# TermScope

A Textual-based Linux/server monitoring TUI dashboard built with Textual.

## Features

- Linux distribution display from `/etc/os-release`
- Host identity summary: hostname, kernel, architecture, uptime
- CPU / memory / swap / disk / load metrics
- Neofetch-style distro panel with ASCII logo on the left and system fields on the right
- Distro ASCII logos sourced from neofetch definitions
- Neofetch-like label/value color separation in the distro info panel
- Per-distribution theme colors
- Neofetch-style color blocks at the bottom of the distro panel
- Network RX/TX live rate
- Dashboard process panel shows all processes
- Process panel scrollbar styled closer to btop, with per-distro colors
- Windows Task Manager-like incremental process name search by typing initial letters
- Repeated same initial letter cycles through matching processes
- Temporary prefix highlighting inside process names while searching
- Explicit `/` search mode for building a search query
- Clear no-match feedback when no process name matches the current query
- Selected process remains tracked across refreshes and resorting
- Dedicated Processes screen with CPU / memory sorting
- Automatic refresh every second
- Pause / resume live refresh with space
- `k` opens a confirmation dialog before SIGTERM
- `K` opens a confirmation dialog before SIGKILL

## Controls

- `q` quit
- `r` refresh now
- `space` pause / resume auto refresh
- `k` confirm and send SIGTERM to selected process
- `K` confirm and send SIGKILL to selected process
- `c` toggle CPU sort between descending and ascending
- `m` toggle memory sort between descending and ascending
- Type letters / numbers in the Processes screen to jump by process name prefix
- Repeat the same initial letter to cycle through matching processes
- `/` enter explicit search mode / find by process name
- `Enter` accept and exit explicit search mode
- `Backspace` delete one search character
- `Esc` clear current prefix search and exit search mode

## Run (bash / zsh)

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .[dev]
termscope
```

## Run (fish)

```fish
python -m venv .venv
source .venv/bin/activate.fish
python -m pip install -e .[dev]
termscope
```

## Test

```bash
pytest -q
```
