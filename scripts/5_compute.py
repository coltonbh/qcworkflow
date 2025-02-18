"""
This script runs conformer search calculations on the U2 anion using the CREST program.
"""

from itertools import product
from pathlib import Path

from chemcloud import compute
from qcio import ProgramInput, CalcType, Structure

# Define directories
CALC_DIR = Path("./data/calcs")
STRUCT_DIR = Path("./data/structures")
FRAG_DIR = STRUCT_DIR / "frags"
# Iterate over all names in the fragments directory
names = [f.stem for f in FRAG_DIR.glob("*.json")]
# View all available options with CalcType.__members__.keys()
calctypes = [CalcType.energy]
program = "crest"

# Define the calculations
prog_inputs = []
for name, calctype in product(names, calctypes):
    # Open the structure
    struct = Structure.open(FRAG_DIR / f"{name}.json")

    # Create the ProgramInput object
    input_obj = ProgramInput(
        calctype=calctype,
        structure=struct,
        model={"method": "gfnff"},
        keywords={
            "calculation": {
                "level": [{"alpb": "ch2cl2"}],
            },
        },
        extras={
            "save_path": (
                CALC_DIR / "frags" / f"{name}-{program}-{calctype.value}.json"
            ).absolute()
        },
    )
    prog_inputs.append(input_obj)

# Run the calculations in parallel
print(f"Submitting {len(prog_inputs)} calculations and waiting on results...")
prog_outputs = compute(program, prog_inputs)
print("Calculations complete!")

# Save the results to data/calcs
for prog_output in prog_outputs:
    prog_output.save(prog_output.input_data.extras["save_path"])
