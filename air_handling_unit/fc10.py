import pandas as pd

from faults import FaultConditionTen
from reports import FaultCodeTenReport
from utils import custom_arg_parser, save_report

# python 3.10 on Windows 10
# py .\fc10.py -i ./ahu_data/MZVAV-1.csv -o MZVAV-1_fc10_report
# py .\fc10.py -i ./ahu_data/MZVAV-2-1.csv -o MZVAV-2-1_fc10_report
# py .\fc10.py -i ./ahu_data/MZVAV-2-2.csv -o MZVAV-2-2_fc10_report

args = custom_arg_parser()

# ADJUST this param for the AHU MIN OA damper stp
AHU_MIN_OA = 20

# G36 params shouldn't need adjusting
# error threshold parameters
OAT_DEGF_ERR_THRES = 5
MAT_DEGF_ERR_THRES = 5

_fc10 = FaultConditionTen(
    OAT_DEGF_ERR_THRES,
    MAT_DEGF_ERR_THRES,
    "AHU: Mixed Air Temperature",
    "AHU: Outdoor Air Temperature",
    "AHU: Cooling Coil Valve Control Signal",
    "AHU: Outdoor Air Damper Control Signal",
)

_fc10_report = FaultCodeTenReport(
    "AHU: Mixed Air Temperature",
    "AHU: Outdoor Air Temperature",
    "AHU: Cooling Coil Valve Control Signal",
    "AHU: Outdoor Air Damper Control Signal",
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
df2 = _fc10.apply(df)
print(df2.head())
print(df2.describe())

save_report(args, df, _fc10_report)
