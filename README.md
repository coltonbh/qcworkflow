# QC Workflow

Sane workflows for happy theoretical chemists ❤️.

## Basic Layout & Core Concepts

```
├── 📂 data
│   ├── 📂 structures # All structure files stored here
│   └── 📂 calcs # All computed data stored here
├── 📂 scripts # Scripts drive computations
├── 📂 notebooks # Notebooks analyze results
├── README.md
└── pyproject.toml
└── uv.lock
```

### Root Files

- `README.md` provides and overview of the research project.
- `pyproject.toml` contains the dependencies required to run and analyze this project.
- `uv.lock` gets created automatically by [uv](https://docs.astral.sh/uv/) to help manage your dependencies.

### Workflow

- `data/` contains all calculated results and structures.
- `scripts/` contains python scripts for driving calculations that follow a simple pattern:
  - Select the structures on which to operate
  - Define the calculations to perform
  - Submit calculations en mass to ChemCloud
  - Save results to `data/calcs` when complete
- Analyze computed data using Jupyter Notebooks stored in `notebooks/`. Notebooks do not submit calculations since this will often result in accidentally running the same calculation multiple times, overwriting previously computed results, etc. Notebooks provide the scientific annotation, context, and analysis on top of the computed results. This makes it easy for anyone to come take over your project, run `uv sync`. And then access all your data with its associated context in your notebooks.

## Getting Started

1. Install [uv](https://docs.astral.sh/uv/).

   MacOS/Linux

   ```sh
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   After installation source either your `~/.bashrc` or `~/.zshrc` depending on your shell.

   ```sh
   source ~/.bashrc
   # or
   source ~/.zshrc
   ```

   Windows

   ```sh
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. Install project dependencies.

   ```sh
   uv sync
   ```

3. Start Jupyter Lab and stat working through the notebooks in order. Start Jupyter Lab from a new terminal, not the built-in terminal of VSCode, otherwise your browser may not be able to access the server due to app sand-boxing.

   ```sh
   uv run jupyter lab notebooks
   ```

## Walkthough

1. Open the `1_structure.ipynb` notebook to familiarize yourself with the `Structure` object. Make sure you get to the end of the notebook and save the structures. They will be used in the next step.
2. Going one script/notebook combination at a time:
   1. Run `uv run scripts/{n}_compute.py`
   2. Open `notebooks/{i}_analysis-*.ipynb` to view the results.
