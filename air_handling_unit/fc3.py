import pandas as pd

from faults import FaultConditionThree
from reports import FaultCodeThreeReport
from utils import custom_arg_parser, save_report

# python 3.10 on Windows 10
# py .\fc3.py -i ./ahu_data/MZVAV-1.csv -o MZVAV-1_fc3_report
# py .\fc3.py -i ./ahu_data/MZVAV-2-1.csv -o MZVAV-2-1_fc3_report
# py .\fc3.py -i ./ahu_data/MZVAV-2-2.csv -o MZVAV-2-2_fc3_report
if __name__ == '__main__':
    args = custom_arg_parser()

    # G36 params shouldn't need adjusting
    # °F error threshold parameters
    OUTDOOR_DEGF_ERR_THRES = 5.
    MIX_DEGF_ERR_THRES = 5.
    RETURN_DEGF_ERR_THRES = 2.

    _fc3 = FaultConditionThree(
        mix_degf_err_thres=MIX_DEGF_ERR_THRES,
        return_degf_err_thres=RETURN_DEGF_ERR_THRES,
        outdoor_degf_err_thres=OUTDOOR_DEGF_ERR_THRES,
        mat_col="AHU: Mixed Air Temperature",
        rat_col="AHU: Return Air Temperature",
        oat_col="AHU: Outdoor Air Temperature",
        fan_vfd_speed_col="AHU: Supply Air Fan Speed Control Signal"
    )

    _fc3_report = FaultCodeThreeReport(
        mix_degf_err_thres=MIX_DEGF_ERR_THRES,
        return_degf_err_thres=RETURN_DEGF_ERR_THRES,
        outdoor_degf_err_thres=OUTDOOR_DEGF_ERR_THRES,
        mat_col="AHU: Mixed Air Temperature",
        rat_col="AHU: Return Air Temperature",
        oat_col="AHU: Outdoor Air Temperature",
        fan_vfd_speed_col="AHU: Supply Air Fan Speed Control Signal"
    )

    df = pd.read_csv(args.input, index_col="Date", parse_dates=True).rolling("5T").mean()

    # describe dataset printing some stuff
    describe_dataset(df)

    # return a whole new dataframe with fault flag as new col
    df2 = _fc3.apply(df)
    print(df2.head())
    print(df2.describe())

    save_report(args, df, _fc3_report)
