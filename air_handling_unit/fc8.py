import os

import pandas as pd

from faults import FaultConditionEight
from reports import FaultCodeEightReport
# python 3.10 on Windows 10
# py .\fc8.py -i ./ahu_data/MZVAV-1.csv -o MZVAV-1_fc8_report
# py .\fc8.py -i ./ahu_data/MZVAV-2-1.csv -o MZVAV-2-1_fc8_report
# py .\fc8.py -i ./ahu_data/MZVAV-2-2.csv -o MZVAV-2-2_fc8_report
from utils import custom_arg_parser

args = custom_arg_parser()

# G36 params shouldnt need adjusting
# error threshold parameters
DELTA_SUPPLY_FAN = 2
MIX_DEGF_ERR_THRES = 5
SUPPLY_DEGF_ERR_THRES = 2

# ADJUST this param for the AHU MIN OA damper stp
AHU_MIN_OA = 20

_fc8 = FaultConditionEight(
    DELTA_SUPPLY_FAN,
    MIX_DEGF_ERR_THRES,
    SUPPLY_DEGF_ERR_THRES,
    AHU_MIN_OA,
    "AHU: Mixed Air Temperature",
    "AHU: Supply Air Temperature",
    "AHU: Outdoor Air Damper Control Signal",
    "AHU: Cooling Coil Valve Control Signal"
)

_fc8_report = FaultCodeEightReport(
    "AHU: Mixed Air Temperature",
    "AHU: Supply Air Temperature",
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
df2 = _fc8.apply(df)
print(df2.head())
print(df2.describe())

document = _fc8_report.create_report(args.output, df2)
path = os.path.join(os.path.curdir, "final_report")
if not os.path.exists(path):
    os.makedirs(path)
document.save(os.path.join(path, f"{args.output}.docx"))
