import pandas as pd

from faults import FaultConditionSeven
from reports import FaultCodeSevenReport
from utils import custom_arg_parser, save_report, describe_dataset

# python 3.10 on Windows 10
# py .\fc7.py -i ./ahu_data/MZVAV-1.csv -o MZVAV-1_fc7_report
# py .\fc7.py -i ./ahu_data/MZVAV-2-1.csv -o MZVAV-2-1_fc7_report
# py .\fc7.py -i ./ahu_data/MZVAV-2-2.csv -o MZVAV-2-2_fc7_report
if __name__ == '__main__':
    args = custom_arg_parser()

    # G36 params shouldn't need adjusting
    # error threshold parameters
    SAT_DEGF_ERR_THRES = 2

    var_dict = {
        "sat_col": "AHU: Supply Air Temperature",
        "satsp_col": "AHU: Supply Air Temperature Set Point",
        "htg_col": "AHU: Heating Coil Valve Control Signal",
        "fan_vfd_speed_col": "AHU: Supply Air Fan Speed Control Signal"
    }

    _fc7 = FaultConditionSeven(
        sat_degf_err_thres=SAT_DEGF_ERR_THRES,
        sat_col=var_dict["sat_col"],
        satsp_col=var_dict["satsp_col"],
        htg_col=var_dict["htg_col"],
        fan_vfd_speed_col=var_dict["fan_vfd_speed_col"]
    )

    _fc7_report = FaultCodeSevenReport(
        sat_col=var_dict["sat_col"],
        satsp_col=var_dict["satsp_col"],
        htg_col=var_dict["htg_col"],
        fan_vfd_speed_col=var_dict["fan_vfd_speed_col"]
    )

    df = pd.read_csv(args.input, index_col="Date", parse_dates=True).rolling("5T").mean()

    # describe dataset printing some stuff
    describe_dataset(df)

    # return a whole new dataframe with fault flag as new col
    df2 = _fc7.apply(df)
    print(df2.head())
    print(df2.describe())
    save_report(args, df, _fc7_report)
