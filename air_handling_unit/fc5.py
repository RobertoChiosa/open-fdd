import pandas as pd

from faults import FaultConditionFive
from reports import FaultCodeFiveReport
from utils import custom_arg_parser, save_report

# python 3.10 on Windows 10
# py .\fc5.py -i ./ahu_data/MZVAV-1.csv -o MZVAV-1_fc5_report
# py .\fc5.py -i ./ahu_data/MZVAV-2-1.csv -o MZVAV-2-1_fc5_report
# py .\fc5.py -i ./ahu_data/MZVAV-2-2.csv -o MZVAV-2-2_fc5_report
if __name__ == '__main__':
    args = custom_arg_parser()
    # G36 params shouldn't need adjusting
    # °F error threshold parameters
    DELTA_T_SUPPLY_FAN = 2.
    SUPPLY_DEGF_ERR_THRES = 2.
    MIX_DEGF_ERR_THRES = 5.

    _fc5 = FaultConditionFive(
        mix_degf_err_thres=MIX_DEGF_ERR_THRES,
        supply_degf_err_thres=SUPPLY_DEGF_ERR_THRES,
        delta_t_supply_fan=DELTA_T_SUPPLY_FAN,
        mat_col="AHU: Mixed Air Temperature",
        sat_col="AHU: Supply Air Temperature",
        htg_vlv_col="AHU: Heating Coil Valve Control Signal",
        fan_vfd_speed_col="AHU: Supply Air Fan Speed Control Signal"
    )

    _fc5_report = FaultCodeFiveReport(
        mix_degf_err_thres=MIX_DEGF_ERR_THRES,
        supply_degf_err_thres=SUPPLY_DEGF_ERR_THRES,
        delta_t_supply_fan=DELTA_T_SUPPLY_FAN,
        mat_col="AHU: Mixed Air Temperature",
        sat_col="AHU: Supply Air Temperature",
        htg_vlv_col="AHU: Heating Coil Valve Control Signal",
        fan_vfd_speed_col="AHU: Supply Air Fan Speed Control Signal"
    )

    df = pd.read_csv(args.input, index_col="Date", parse_dates=True).rolling("5T").mean()

    # describe dataset printing some stuff
    describe_dataset(df)

    # return a whole new dataframe with fault flag as new col
    df2 = _fc5.apply(df)
    print(df2.head())
    print(df2.describe())
    save_report(args, df, _fc5_report)
