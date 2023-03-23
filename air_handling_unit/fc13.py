import pandas as pd

from faults import FaultConditionThirteen
from reports import FaultCodeThirteenReport
from utils import custom_arg_parser, save_report, describe_dataset

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

    var_dict = {
        "sat_col": "AHU: Supply Air Temperature",
        "satsp_col": "AHU: Supply Air Temperature Set Point",
        "clg_col": "AHU: Cooling Coil Valve Control Signal",
        "economizer_sig_col": "AHU: Outdoor Air Damper Control Signal",
        "fan_vfd_speed_col": "AHU: Supply Air Fan Speed Control Signal"
    }
    _fc13 = FaultConditionThirteen(
        sat_degf_err_thres=SAT_DEGF_ERR_THRES,
        ahu_min_oa_dpr=AHU_MIN_OA,
        sat_col=var_dict["sat_col"],
        satsp_col=var_dict["satsp_col"],
        clg_col=var_dict["clg_col"],
        economizer_sig_col=var_dict["economizer_sig_col"]
    )

    _fc13_report = FaultCodeThirteenReport(
        sat_col=var_dict["sat_col"],
        satsp_col=var_dict["satsp_col"],
        clg_col=var_dict["clg_col"],
        economizer_sig_col=var_dict["economizer_sig_col"],
        fan_vfd_speed_col=var_dict["fan_vfd_speed_col"]
    )

    df = pd.read_csv(args.input, index_col="Date", parse_dates=True).rolling("5T").mean()

    # describe dataset printing some stuff
    describe_dataset(df)

    # return a whole new dataframe with fault flag as new col
    df2 = _fc13.apply(df)
    print(df2.head())
    print(df2.describe())

    save_report(args, df, _fc13_report)
