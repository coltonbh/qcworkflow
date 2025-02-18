from pathlib import Path

from chemcloud import CCClient
from qcio import Structure, ProgramInput

# Define directories
CALC_DIR = Path("./data/calcs")
STRUCT_DIR = Path("./data/structures")

# Create ChemCloud client for doing calculations
client = CCClient()

# Open xyz files in order of reaction
struct_names = [
    "iprtu.xyz",
    "naome.xyz",
    "lactd.xyz",
    "ts1.xyz",
    "int1.xyz",
    "int2.xyz",
    "ts2.xyz",
    "int3.xyz",
    "int4.xyz",
    "int5.xyz",
    "int6.xyz",
]

structs = [Structure.open(STRUCT_DIR / name) for name in struct_names]

# Create ProgramInput objects defining the calculations
prog_inputs = [
    ProgramInput(
        calctype="energy",
        structure=struct,
        model={"method": "b3lyp", "basis": "6-31gss"},
        keywords={"purify": "no"},
    )
    for struct in structs
]

# Run the calculations
future_prog_outputs = client.compute("terachem", prog_inputs)
prog_outputs = future_prog_outputs.get()

# Save the results
for prog_output in prog_outputs:
    prog_output.save(CALC_DIR / f"{prog_output.structure.name}.json")
