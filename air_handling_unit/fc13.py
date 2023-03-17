import pandas as pd

from faults import FaultConditionThirteen
from reports import FaultCodeThirteenReport
from utils import custom_arg_parser, save_report

# python 3.10 on Windows 10
# py .\fc13.py -i ./ahu_data/MZVAV-1.csv -o MZVAV-1_fc13_report
# py .\fc13.py -i ./ahu_data/MZVAV-2-1.csv -o MZVAV-2-1_fc13_report
# py .\fc13.py -i ./ahu_data/MZVAV-2-2.csv -o MZVAV-2-2_fc13_report
if __name__ == '__main__':
    args = custom_arg_parser()
    # ADJUST this param for the AHU MIN OA damper stp
    AHU_MIN_OA = 20

    # G36 params shouldn't need adjusting
    # error threshold parameters
    SAT_DEGF_ERR_THRES = 2

    _fc13 = FaultConditionThirteen(
        SAT_DEGF_ERR_THRES,
        AHU_MIN_OA,
        "AHU: Supply Air Temperature",
        "AHU: Supply Air Temperature Set Point",
        "AHU: Cooling Coil Valve Control Signal",
        "AHU: Outdoor Air Damper Control Signal",
    )

    _fc13_report = FaultCodeThirteenReport(
        "AHU: Supply Air Temperature",
        "AHU: Supply Air Temperature Set Point",
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
    df2 = _fc13.apply(df)
    print(df2.head())
    print(df2.describe())

    save_report(args, df, _fc13_report)
