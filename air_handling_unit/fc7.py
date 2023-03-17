import pandas as pd

from faults import FaultConditionSeven
from reports import FaultCodeSevenReport
from utils import custom_arg_parser
from utils import save_report

# python 3.10 on Windows 10
# py .\fc7.py -i ./ahu_data/MZVAV-1.csv -o MZVAV-1_fc7_report
# py .\fc7.py -i ./ahu_data/MZVAV-2-1.csv -o MZVAV-2-1_fc7_report
# py .\fc7.py -i ./ahu_data/MZVAV-2-2.csv -o MZVAV-2-2_fc7_report

args = custom_arg_parser()

# G36 params shouldn't need adjusting
# error threshold parameters
SAT_DEGF_ERR_THRES = 2

_fc7 = FaultConditionSeven(
    SAT_DEGF_ERR_THRES,
    "AHU: Supply Air Temperature",
    "AHU: Supply Air Temperature Set Point",
    "AHU: Heating Coil Valve Control Signal",
    "AHU: Supply Air Fan Speed Control Signal"
)

_fc7_report = FaultCodeSevenReport(
    "AHU: Supply Air Temperature",
    "AHU: Supply Air Temperature Set Point",
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
df2 = _fc7.apply(df)
print(df2.head())
print(df2.describe())
save_report(args, df, _fc7_report)
