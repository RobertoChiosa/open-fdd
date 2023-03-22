import pandas as pd

from faults import FaultConditionNine
from reports import FaultCodeNineReport
from utils import custom_arg_parser, save_report, describe_dataset

# python 3.10 on Windows 10
# py .\fc9.py -i ./ahu_data/MZVAV-1.csv -o MZVAV-1_fc9_report
# py .\fc9.py -i ./ahu_data/MZVAV-2-1.csv -o MZVAV-2-1_fc9_report
# py .\fc9.py -i ./ahu_data/MZVAV-2-2.csv -o MZVAV-2-2_fc9_report
if __name__ == '__main__':
    args = custom_arg_parser()

    # G36 params shouldn't need adjusting
    # error threshold parameters
    DELTA_SUPPLY_FAN = 2
    OAT_DEGF_ERR_THRES = 5
    SUPPLY_DEGF_ERR_THRES = 2

    # ADJUST this param for the AHU MIN OA damper stp
    AHU_MIN_OA = 20

    _fc9 = FaultConditionNine(
        delta_supply_fan=DELTA_SUPPLY_FAN,
        oat_err_thres=OAT_DEGF_ERR_THRES,
        supply_err_thres=SUPPLY_DEGF_ERR_THRES,
        ahu_min_oa=AHU_MIN_OA,
        satsp_col="AHU: Supply Air Temperature Set Point",
        oat_col="AHU: Outdoor Air Temperature",
        cooling_sig_col="AHU: Cooling Coil Valve Control Signal",
        economizer_sig_col="AHU: Outdoor Air Damper Control Signal"
    )

    _fc9_report = FaultCodeNineReport(
        satsp_col="AHU: Supply Air Temperature Set Point",
        oat_col="AHU: Outdoor Air Temperature",
        fan_vfd_speed_col="AHU: Supply Air Fan Speed Control Signal",
        economizer_sig_col="AHU: Outdoor Air Damper Control Signal"
    )

    df = pd.read_csv(args.input, index_col="Date", parse_dates=True).rolling("5T").mean()

    # describe dataset printing some stuff
    describe_dataset(df)

    # return a whole new dataframe with fault flag as new col
    df2 = _fc9.apply(df)
    print(df2.head())
    print(df2.describe())

    save_report(args, df, _fc9_report)
