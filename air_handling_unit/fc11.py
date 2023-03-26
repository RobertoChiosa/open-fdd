from datetime import timedelta

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

    var_dict = {
        "satsp_col": "AHU: Supply Air Temperature Set Point",
        "oat_col": "AHU: Outdoor Air Temperature",
        "clg_col": "AHU: Cooling Coil Valve Control Signal",
        "economizer_sig_col": "AHU: Outdoor Air Damper Control Signal",
        "fan_vfd_speed_col": "AHU: Supply Air Fan Speed Control Signal"
    }

    _fc11 = FaultConditionEleven(
        delta_supply_fan=DELTA_SUPPLY_FAN,
        oat_err_thres=OAT_DEGF_ERR_THRES,
        supply_err_thres=SUPPLY_DEGF_ERR_THRES,
        satsp_col=var_dict["satsp_col"],
        oat_col=var_dict["oat_col"],
        clg_col=var_dict["clg_col"],
        economizer_sig_col=var_dict["economizer_sig_col"]
    )

    _fc11_report = FaultCodeElevenReport(
        satsp_col=var_dict["satsp_col"],
        oat_col=var_dict["oat_col"],
        clg_col=var_dict["clg_col"],
        economizer_sig_col=var_dict["economizer_sig_col"],
        fan_vfd_speed_col=var_dict["fan_vfd_speed_col"]
    )

    df = pd.read_csv(args.input, index_col="Date", parse_dates=True).rolling(timedelta(minutes=5)).mean()

    # describe dataset printing some stuff
    describe_dataset(df)

    # return a whole new dataframe with fault flag as new col
    df2 = _fc11.apply(df)
    print(df2.head())
    print(df2.describe())

    save_report(args, df, _fc11_report)
