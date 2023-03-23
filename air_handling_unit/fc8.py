import pandas as pd

from faults import FaultConditionEight
from reports import FaultCodeEightReport
from utils import custom_arg_parser, save_report, describe_dataset

# python 3.10 on Windows 10
# py .\fc8.py -i ./ahu_data/MZVAV-1.csv -o MZVAV-1_fc8_report
# py .\fc8.py -i ./ahu_data/MZVAV-2-1.csv -o MZVAV-2-1_fc8_report
# py .\fc8.py -i ./ahu_data/MZVAV-2-2.csv -o MZVAV-2-2_fc8_report
if __name__ == '__main__':
    args = custom_arg_parser()

    # G36 params shouldn't need adjusting
    # error threshold parameters
    DELTA_SUPPLY_FAN = 2
    MIX_DEGF_ERR_THRES = 5
    SUPPLY_DEGF_ERR_THRES = 2

    # ADJUST this param for the AHU MIN OA damper stp
    AHU_MIN_OA = 20

    var_dict = {
        "mat_col": "AHU: Mixed Air Temperature",
        "sat_col": "AHU: Supply Air Temperature",
        "economizer_sig_col": "AHU: Outdoor Air Damper Control Signal",
        "cooling_sig_col": "AHU: Cooling Coil Valve Control Signal",
        "fan_vfd_speed_col": "AHU: Supply Air Fan Speed Control Signal"
    }

    _fc8 = FaultConditionEight(
        delta_supply_fan=DELTA_SUPPLY_FAN,
        mix_err_thres=MIX_DEGF_ERR_THRES,
        supply_err_thres=SUPPLY_DEGF_ERR_THRES,
        ahu_min_oa=AHU_MIN_OA,
        mat_col=var_dict["mat_col"],
        sat_col=var_dict["sat_col"],
        economizer_sig_col=var_dict["economizer_sig_col"],
        cooling_sig_col=var_dict["cooling_sig_col"]
    )

    _fc8_report = FaultCodeEightReport(
        mat_col=var_dict["mat_col"],
        sat_col=var_dict["sat_col"],
        economizer_sig_col=var_dict["economizer_sig_col"],
        fan_vfd_speed_col=var_dict["fan_vfd_speed_col"],
    )

    df = pd.read_csv(args.input, index_col="Date", parse_dates=True).rolling("5T").mean()

    # describe dataset printing some stuff
    describe_dataset(df)

    # return a whole new dataframe with fault flag as new col
    df2 = _fc8.apply(df)
    print(df2.head())
    print(df2.describe())
    save_report(args, df, _fc8_report)
