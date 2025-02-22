from datetime import timedelta

import pandas as pd

from faults import FaultConditionFour
from reports import FaultCodeFourReport
from utils import custom_arg_parser, save_report, describe_dataset

# python 3.10 on Windows 10
# py .\fc4.py -i ./ahu_data/MZVAV-1.csv -o MZVAV-1_fc4_report
# py .\fc4.py -i ./ahu_data/MZVAV-2-1.csv -o MZVAV-2-1_fc4_report
# py .\fc4.py -i ./ahu_data/MZVAV-2-2.csv -o MZVAV-2-2_fc4_report
# todo something is not working fc4_flag

if __name__ == '__main__':
    args = custom_arg_parser()
    # G36 params COULD need adjusting
    # default OS MAX state changes is 7
    # which seems high, could be worth adjusting
    # down to 4 to see what the faults look like
    DELTA_OS_MAX = 7

    # ADJUST this param for the AHU MIN OA damper stp
    AHU_MIN_OA = .20

    var_dict = {
        "economizer_sig_col": "AHU: Outdoor Air Damper Control Signal",
        "heating_sig_col": "AHU: Heating Coil Valve Control Signal",
        "cooling_sig_col": "AHU: Cooling Coil Valve Control Signal",
        "fan_vfd_speed_col": "AHU: Supply Air Fan Speed Control Signal"
    }

    _fc4 = FaultConditionFour(
        delta_os_max=DELTA_OS_MAX,
        ahu_min_oa=AHU_MIN_OA,
        economizer_sig_col=var_dict["economizer_sig_col"],
        heating_sig_col=var_dict["heating_sig_col"],
        cooling_sig_col=var_dict["cooling_sig_col"],
        fan_vfd_speed_col=var_dict["fan_vfd_speed_col"]
    )

    _fc4_report = FaultCodeFourReport(DELTA_OS_MAX)

    df = pd.read_csv(args.input, index_col="Date", parse_dates=True).rolling(timedelta(minutes=5)).mean()

    # describe dataset printing some stuff
    describe_dataset(df)

    # return a whole new dataframe with fault flag as new col
    # data is resampled for hourly averages in df2
    df2 = _fc4.apply(df)
    print(df2.head())
    print(df2.describe())
    save_report(args, df, _fc4_report)
