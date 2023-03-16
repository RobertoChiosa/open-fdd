import argparse
import os

import pandas as pd

from faults import FaultConditionNine
from reports import FaultCodeNineReport

# python 3.10 on Windows 10
# py .\fc9.py -i ./ahu_data/MZVAV-1.csv -o MZVAV-1_fc9_report
# py .\fc9.py -i ./ahu_data/MZVAV-2-1.csv -o MZVAV-2-1_fc9_report
# py .\fc9.py -i ./ahu_data/MZVAV-2-2.csv -o MZVAV-2-2_fc9_report


parser = argparse.ArgumentParser(add_help=False)
args = parser.add_argument_group("Options")

args.add_argument(
    "-h", "--help", action="help", help="Show this help message and exit."
)
args.add_argument("-i", "--input", required=True, type=str, help="CSV File Input")
args.add_argument(
    "-o", "--output", required=True, type=str, help="Word File Output Name"
)
"""
FUTURE 
 * incorporate an arg for SI units 
 * °C on temp sensors
 * piping pressure sensor PSI conversion
 * air flow CFM conversion
 * AHU duct static pressure "WC

args.add_argument('--use-SI-units', default=False, action='store_true')
args.add_argument('--no-SI-units', dest='use-SI-units', action='store_false')
"""
args = parser.parse_args()

# G36 params shouldnt need adjusting
# error threshold parameters
DELTA_SUPPLY_FAN = 2
OAT_DEGF_ERR_THRES = 5
SUPPLY_DEGF_ERR_THRES = 2

# ADJUST this param for the AHU MIN OA damper stp
AHU_MIN_OA = 20

_fc9 = FaultConditionNine(
    DELTA_SUPPLY_FAN,
    OAT_DEGF_ERR_THRES,
    SUPPLY_DEGF_ERR_THRES,
    AHU_MIN_OA,
    "AHU: Supply Air Temperature Set Point",
    "AHU: Outdoor Air Temperature",
    "AHU: Cooling Coil Valve Control Signal",
    "AHU: Outdoor Air Damper Control Signal"
)

_fc9_report = FaultCodeNineReport(
    "AHU: Supply Air Temperature Set Point",
    "AHU: Outdoor Air Temperature",
    "AHU: Supply Air Fan Speed Control Signal",
    "AHU: Outdoor Air Damper Control Signal"
)

df = pd.read_csv(args.input, index_col="Date", parse_dates=True).rolling("5T").mean()

start = df.head(1).index.date
print("Dataset start: ", start)

end = df.tail(1).index.date
print("Dataset end: ", end)

for col in df.columns:
    print("df column: ", col, "- max len: ", df[col].size)

# return a whole new dataframe with fault flag as new col
df2 = _fc9.apply(df)
print(df2.head())
print(df2.describe())

document = _fc9_report.create_report(args.output, df2)
path = os.path.join(os.path.curdir, "final_report")
if not os.path.exists(path):
    os.makedirs(path)
document.save(os.path.join(path, f"{args.output}.docx"))
