"""
This script runs conformer search calculations on the U2 anion using the CREST program.
"""

from pathlib import Path

from chemcloud import compute
from qcio import FileInput

# Define directories
DATA_DIR = Path("./data")
CALC_DIR = DATA_DIR / "calcs"
program = "terachem"

# Define the calculation by reading in TeraChem's native input files
prog_input = FileInput.from_directory(
    DATA_DIR / "terachem-native-input",
    cmdline_args=["tc.in"], # Tell TeraChem to read from tc.in
)
# Run the calculation on ChemCloud
print("Submitting 1 calculation and waiting on results...")
prog_output = compute(program, prog_input)
print("Calculation complete!")

# Save the results object to data/calcs
prog_output.save(CALC_DIR / "terachem-native-output.json")

# Also save the output as native TeraChem output files
prog_output.results.save_files(DATA_DIR / "terachem-native-output")
print("Files saved as a native TeraChem output directory to data/terachem-native-output")