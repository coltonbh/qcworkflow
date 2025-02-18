"""
This script runs conformer search calculations on the U2 anion using the CREST program.
"""

from itertools import product
from pathlib import Path

from chemcloud import compute
from qcio import ProgramInput, CalcType, ProgramOutput

# Define directories
CALC_DIR = Path("./data/calcs")
STRUCT_DIR = Path("./data/structures")

# Select the structures and declare the program
names = ["u2-anion"]
# View all available options with CalcType.__members__.keys()
calctypes = [CalcType.conformer_search]
program = "crest"

# Define the calculations
prog_inputs = []
for name, calctype in product(names, calctypes):
    # Get the structure from previously computed results
    opt = ProgramOutput.open(CALC_DIR / f"{name}-crest-optimization.json")
    struct = opt.results.final_structure

    # Create the ProgramInput object
    input_obj = ProgramInput(
        calctype=calctype,
        structure=struct,
        model={"method": "gfnff"},
        keywords={
            "topo": False,
            "preopt": False,
            # Adds implicit solvent using CREST's ALPB keywords
            "calculation": {
                "level": [{"alpb": "ch2cl2"}],
            },
        },
        extras={
            "save_path": (
                CALC_DIR / f"{name}-{program}-{calctype.value}.json"
            ).absolute()
        },
    )
    prog_inputs.append(input_obj)

# Run the calculations in parallel
prog_outputs = compute(program, prog_inputs)

# Save the results to data/calcs
for prog_output in prog_outputs:
    prog_output.save(prog_output.input_data.extras["save_path"])
