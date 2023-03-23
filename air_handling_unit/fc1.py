import pandas as pd

from faults import FaultConditionOne
from reports import FaultCodeOneReport
from utils import custom_arg_parser, save_report, describe_dataset

# python 3.10 on Windows 10
# py .\fc1.py -i ./ahu_data/MZVAV-1.csv -o MZVAV-1_fc1_report
# py .\fc1.py -i ./ahu_data/MZVAV-2-1.csv -o MZVAV-2-1_fc1_report
# py .\fc1.py -i ./ahu_data/MZVAV-2-2.csv -o MZVAV-2-2_fc1_report

# python 3.9 on macOS
# python ./fc1.py -i ./ahu_data/MZVAV-1.csv -o MZVAV-1_fc1_report
# python ./fc1.py -i ./ahu_data/MZVAV-2-1.csv -o MZVAV-2-1_fc1_report
# python ./fc1.py -i ./ahu_data/MZVAV-2-2.csv -o MZVAV-2-2_fc1_report

if __name__ == '__main__':
    args = custom_arg_parser()

    # G36 params shouldn't need adjusting
    # error threshold parameters
    VFD_SPEED_PERCENT_ERR_THRES = 0.05
    VFD_SPEED_PERCENT_MAX = 0.99
    DUCT_STATIC_INCHES_ERR_THRES = 0.1

    # define dictionary to be mapped with brick points
    var_dict = {
        "duct_static_col": "AHU: Supply Air Duct Static Pressure",
        "supply_vfd_speed_col": "AHU: Supply Air Fan Speed Control Signal",
        "duct_static_setpoint_col": "AHU: Supply Air Duct Static Pressure Set Point"
    }

    _fc1 = FaultConditionOne(
        vfd_speed_percent_err_thres=VFD_SPEED_PERCENT_ERR_THRES,
        vfd_speed_percent_max=VFD_SPEED_PERCENT_MAX,
        duct_static_inches_err_thres=DUCT_STATIC_INCHES_ERR_THRES,
        duct_static_col=var_dict["duct_static_col"],
        supply_vfd_speed_col=var_dict["supply_vfd_speed_col"],
        duct_static_setpoint_col=var_dict["duct_static_setpoint_col"],
    )

    _fc1_report = FaultCodeOneReport(
        vfd_speed_percent_err_thres=VFD_SPEED_PERCENT_ERR_THRES,
        vfd_speed_percent_max=VFD_SPEED_PERCENT_MAX,
        duct_static_inches_err_thres=DUCT_STATIC_INCHES_ERR_THRES,
        duct_static_col=var_dict["duct_static_col"],
        supply_vfd_speed_col=var_dict["supply_vfd_speed_col"],
        duct_static_setpoint_col=var_dict["duct_static_setpoint_col"],
    )

    df = pd.read_csv(args.input, index_col="Date", parse_dates=True).rolling('5T').mean()

    # describe dataset printing some stuff
    describe_dataset(df)

    # return a whole new dataframe with fault flag as new col
    df2 = _fc1.apply(df)
    print(df2.head())
    print(df2.describe())

    save_report(args, df, _fc1_report)
