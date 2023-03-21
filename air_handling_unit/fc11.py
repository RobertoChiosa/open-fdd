import pandas as pd

from faults import FaultConditionEleven
from reports import FaultCodeElevenReport
from utils import custom_arg_parser, save_report, describe_dataset

# python 3.10 on Windows 10
# py .\fc11.py -i ./ahu_data/MZVAV-1.csv -o MZVAV-1_fc11_report
# py .\fc11.py -i ./ahu_data/MZVAV-2-1.csv -o MZVAV-2-1_fc11_report
# py .\fc11.py -i ./ahu_data/MZVAV-2-2.csv -o MZVAV-2-2_fc11_report
if __name__ == '__main__':
    args = custom_arg_parser()

    # G36 params shouldn't need adjusting
    # error threshold parameters
    DELTA_SUPPLY_FAN = 2
    OAT_DEGF_ERR_THRES = 5
    SUPPLY_DEGF_ERR_THRES = 2

    _fc11 = FaultConditionEleven(
        DELTA_SUPPLY_FAN,
        OAT_DEGF_ERR_THRES,
        SUPPLY_DEGF_ERR_THRES,
        "AHU: Supply Air Temperature Set Point",
        "AHU: Outdoor Air Temperature",
        "AHU: Cooling Coil Valve Control Signal",
        "AHU: Outdoor Air Damper Control Signal"
    )

    _fc11_report = FaultCodeElevenReport(
        "AHU: Supply Air Temperature Set Point",
        "AHU: Outdoor Air Temperature",
        "AHU: Cooling Coil Valve Control Signal",
        "AHU: Outdoor Air Damper Control Signal",
        "AHU: Supply Air Fan Speed Control Signal"
    )

    df = pd.read_csv(args.input, index_col="Date", parse_dates=True).rolling("5T").mean()

    # describe dataset printing some stuff
    describe_dataset(df)

    # return a whole new dataframe with fault flag as new col
    df2 = _fc11.apply(df)
    print(df2.head())
    print(df2.describe())

    save_report(args, df, _fc11_report)
