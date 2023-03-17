import os

import pandas as pd

from faults import FaultConditionOne
from reports import FaultCodeOneReport
from utils import custom_arg_parser

# python 3.10 on Windows 10
# py .\fc1.py -i ./ahu_data/MZVAV-1.csv -o MZVAV-1_fc1_report
# py .\fc1.py -i ./ahu_data/MZVAV-2-1.csv -o MZVAV-2-1_fc1_report
# py .\fc1.py -i ./ahu_data/MZVAV-2-2.csv -o MZVAV-2-2_fc1_report

# python 3.9 on macOS
# python ./fc1.py -i ./ahu_data/MZVAV-1.csv -o MZVAV-1_fc1_report
# python ./fc1.py -i ./ahu_data/MZVAV-2-1.csv -o MZVAV-2-1_fc1_report
# python ./fc1.py -i ./ahu_data/MZVAV-2-2.csv -o MZVAV-2-2_fc1_report

args = custom_arg_parser()

# G36 params shouldn't need adjusting
# error threshold parameters
VFD_SPEED_PERCENT_ERR_THRES = 0.05
VFD_SPEED_PERCENT_MAX = 0.99
DUCT_STATIC_INCHES_ERR_THRES = 0.1

_fc1 = FaultConditionOne(
    VFD_SPEED_PERCENT_ERR_THRES,
    VFD_SPEED_PERCENT_MAX,
    DUCT_STATIC_INCHES_ERR_THRES,
    "AHU: Supply Air Duct Static Pressure",
    "AHU: Supply Air Fan Speed Control Signal",
    "AHU: Supply Air Duct Static Pressure Set Point",
)

_fc1_report = FaultCodeOneReport(
    VFD_SPEED_PERCENT_ERR_THRES,
    VFD_SPEED_PERCENT_MAX,
    DUCT_STATIC_INCHES_ERR_THRES,
    "AHU: Supply Air Duct Static Pressure",
    "AHU: Supply Air Fan Speed Control Signal",
    "AHU: Supply Air Duct Static Pressure Set Point",
)

df = pd.read_csv(args.input, index_col="Date", parse_dates=True).rolling("5T").mean()

start = df.head(1).index.date
print("Dataset start: ", start)

end = df.tail(1).index.date
print("Dataset end: ", end)

for col in df.columns:
    print("df column: ", col, "- max len: ", df[col].size)

# return a whole new dataframe with fault flag as new col
df2 = _fc1.apply(df)
print(df2.head())
print(df2.describe())

document = _fc1_report.create_report(args.output, df)
path = os.path.join(os.path.curdir, "final_report")
if not os.path.exists(path):
    os.makedirs(path)
document.save(os.path.join(path, f"{args.output}.docx"))
