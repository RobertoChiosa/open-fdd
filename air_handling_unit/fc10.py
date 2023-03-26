from datetime import timedelta

import pandas as pd

from faults import FaultConditionTen
from reports import FaultCodeTenReport
from utils import custom_arg_parser, save_report, describe_dataset

# python 3.10 on Windows 10
# py .\fc10.py -i ./ahu_data/MZVAV-1.csv -o MZVAV-1_fc10_report
# py .\fc10.py -i ./ahu_data/MZVAV-2-1.csv -o MZVAV-2-1_fc10_report
# py .\fc10.py -i ./ahu_data/MZVAV-2-2.csv -o MZVAV-2-2_fc10_report
if __name__ == '__main__':
    args = custom_arg_parser()

    # ADJUST this param for the AHU MIN OA damper stp
    AHU_MIN_OA = 20

    # G36 params shouldn't need adjusting
    # error threshold parameters
    OAT_DEGF_ERR_THRES = 5
    MAT_DEGF_ERR_THRES = 5

    var_dict = {
        "mat_col": "AHU: Mixed Air Temperature",
        "oat_col": "AHU: Outdoor Air Temperature",
        "clg_col": "AHU: Cooling Coil Valve Control Signal",
        "economizer_sig_col": "AHU: Outdoor Air Damper Control Signal",
        "fan_vfd_speed_col": "AHU: Supply Air Fan Speed Control Signal"
    }

    _fc10 = FaultConditionTen(
        oat_err_thres=OAT_DEGF_ERR_THRES,
        mat_err_thres=MAT_DEGF_ERR_THRES,
        oat_col=var_dict["oat_col"],
        mat_col=var_dict["mat_col"],
        clg_col=var_dict["clg_col"],
        economizer_sig_col=var_dict["economizer_sig_col"]
    )

    _fc10_report = FaultCodeTenReport(
        oat_col=var_dict["oat_col"],
        mat_col=var_dict["mat_col"],
        clg_col=var_dict["clg_col"],
        economizer_sig_col=var_dict["economizer_sig_col"],
        fan_vfd_speed_col=var_dict["fan_vfd_speed_col"]
    )

    df = pd.read_csv(args.input, index_col="Date", parse_dates=True).rolling(timedelta(minutes=5)).mean()

    # describe dataset printing some stuff
    describe_dataset(df)

    # return a whole new dataframe with fault flag as new col
    df2 = _fc10.apply(df)
    print(df2.head())
    print(df2.describe())

    save_report(args, df, _fc10_report)
