"""
This script runs energy and optimizations calculations on the U2 and U3 anions using
the CREST program.
"""

from itertools import product
from pathlib import Path

from chemcloud import compute
from qcio import Structure, ProgramInput, CalcType

# Define directories
CALC_DIR = Path("./data/calcs")
STRUCT_DIR = Path("./data/structures")

# Select the structures and declare the program
names = ["u2-anion", "u3-anion"]
# View all available options with CalcType.__members__.keys()
calctypes = [CalcType.energy, CalcType.optimization]
program = "crest"


# Define the calculations
prog_inputs = []
# All combinations of structures and calculation types
for name, calctype in product(names, calctypes):
    # Open the structure
    struct = Structure.open(STRUCT_DIR / f"{name}.json")

    # Create the ProgramInput object
    prog_input = ProgramInput(
        calctype=calctype,
        structure=struct,
        model={"method": "gfnff"},
        # Adds implicit solvent using CREST's ALPB keyword
        keywords={"calculation": {"level": [{"alpb": "ch2cl2"}]}},
        # Defining the save path on the input means we can collect
        # the results later without needing any context from this script
        extras={
            "save_path": (
                CALC_DIR / f"{name}-{program}-{calctype.value}.json"
            ).absolute()
        },
    )

    prog_inputs.append(prog_input)

# Run the calculations in parallel
prog_outputs = compute(program, prog_inputs)

# Save the results to data/calcs
for prog_output in prog_outputs:
    prog_output.save(prog_output.input_data.extras["save_path"])
