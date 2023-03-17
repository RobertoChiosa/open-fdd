import os

import pandas as pd

from faults import FaultConditionFive
from reports import FaultCodeFiveReport
from utils import custom_arg_parser

# python 3.10 on Windows 10
# py .\fc5.py -i ./ahu_data/MZVAV-1.csv -o MZVAV-1_fc5_report
# py .\fc5.py -i ./ahu_data/MZVAV-2-1.csv -o MZVAV-2-1_fc5_report
# py .\fc5.py -i ./ahu_data/MZVAV-2-2.csv -o MZVAV-2-2_fc5_report

args = custom_arg_parser()
# G36 params shouldnt need adjusting
# °F error threshold parameters
DELTA_T_SUPPLY_FAN = 2.
SUPPLY_DEGF_ERR_THRES = 2.
MIX_DEGF_ERR_THRES = 5.

_fc5 = FaultConditionFive(
    MIX_DEGF_ERR_THRES,
    SUPPLY_DEGF_ERR_THRES,
    DELTA_T_SUPPLY_FAN,
    "AHU: Mixed Air Temperature",
    "AHU: Supply Air Temperature",
    "AHU: Heating Coil Valve Control Signal",
    "AHU: Supply Air Fan Speed Control Signal"
)

_fc5_report = FaultCodeFiveReport(
    MIX_DEGF_ERR_THRES,
    SUPPLY_DEGF_ERR_THRES,
    DELTA_T_SUPPLY_FAN,
    "AHU: Mixed Air Temperature",
    "AHU: Supply Air Temperature",
    "AHU: Heating Coil Valve Control Signal",
    "AHU: Supply Air Fan Speed Control Signal"
)

df = pd.read_csv(args.input, index_col="Date", parse_dates=True).rolling("5T").mean()

start = df.head(1).index.date
print("Dataset start: ", start)

end = df.tail(1).index.date
print("Dataset end: ", end)

for col in df.columns:
    print("df column: ", col, "- max len: ", df[col].size)

# return a whole new dataframe with fault flag as new col
df2 = _fc5.apply(df)
print(df2.head())
print(df2.describe())

document = _fc5_report.create_report(args.output, df2)
path = os.path.join(os.path.curdir, "final_report")
if not os.path.exists(path):
    os.makedirs(path)
document.save(os.path.join(path, f"{args.output}.docx"))
