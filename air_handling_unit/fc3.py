import os

import pandas as pd

from faults import FaultConditionThree
from reports import FaultCodeThreeReport
from utils import custom_arg_parser

# python 3.10 on Windows 10
# py .\fc3.py -i ./ahu_data/MZVAV-1.csv -o MZVAV-1_fc3_report
# py .\fc3.py -i ./ahu_data/MZVAV-2-1.csv -o MZVAV-2-1_fc3_report
# py .\fc3.py -i ./ahu_data/MZVAV-2-2.csv -o MZVAV-2-2_fc3_report

args = custom_arg_parser()

# G36 params shouldnt need adjusting
# °F error threshold parameters
OUTDOOR_DEGF_ERR_THRES = 5.
MIX_DEGF_ERR_THRES = 5.
RETURN_DEGF_ERR_THRES = 2.

_fc3 = FaultConditionThree(
    MIX_DEGF_ERR_THRES,
    RETURN_DEGF_ERR_THRES,
    OUTDOOR_DEGF_ERR_THRES,
    "AHU: Mixed Air Temperature",
    "AHU: Return Air Temperature",
    "AHU: Outdoor Air Temperature",
    "AHU: Supply Air Fan Speed Control Signal"
)

_fc3_report = FaultCodeThreeReport(
    MIX_DEGF_ERR_THRES,
    RETURN_DEGF_ERR_THRES,
    OUTDOOR_DEGF_ERR_THRES,
    "AHU: Mixed Air Temperature",
    "AHU: Return Air Temperature",
    "AHU: Outdoor Air Temperature",
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
df2 = _fc3.apply(df)
print(df2.head())
print(df2.describe())

document = _fc3_report.create_report(args.output, df)
path = os.path.join(os.path.curdir, "final_report")
if not os.path.exists(path):
    os.makedirs(path)
document.save(os.path.join(path, f"{args.output}.docx"))
