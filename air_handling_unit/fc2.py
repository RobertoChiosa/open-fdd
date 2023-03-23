import pandas as pd

from faults import FaultConditionTwo
from reports import FaultCodeTwoReport
from utils import custom_arg_parser, save_report, describe_dataset

# python 3.10 on Windows 10
# py .\fc2.py -i ./ahu_data/MZVAV-1.csv -o MZVAV-1_fc2_report
# py .\fc2.py -i ./ahu_data/MZVAV-2-1.csv -o MZVAV-2-1_fc2_report
# py .\fc2.py -i ./ahu_data/MZVAV-2-2.csv -o MZVAV-2-2_fc2_report
# python 3.9 on macOS
# python ./fc2.py -i ./ahu_data/MZVAV-1.csv -o MZVAV-1_fc2_report
# python ./fc2.py -i ./ahu_data/MZVAV-2-1.csv -o MZVAV-2-1_fc2_report
# python ./fc2.py -i ./ahu_data/MZVAV-2-2.csv -o MZVAV-2-2_fc2_report

if __name__ == '__main__':
    args = custom_arg_parser()

    # G36 params shouldn't need adjusting
    # °F error threshold parameters
    OUTDOOR_DEGF_ERR_THRES = 5.
    MIX_DEGF_ERR_THRES = 5.
    RETURN_DEGF_ERR_THRES = 2.

    var_dict = {
        "mat_col": "AHU: Mixed Air Temperature",
        "rat_col": "AHU: Return Air Temperature",
        "oat_col": "AHU: Outdoor Air Temperature",
        "fan_vfd_speed_col": "AHU: Supply Air Fan Speed Control Signal"
    }

    _fc2 = FaultConditionTwo(
        mix_degf_err_thres=MIX_DEGF_ERR_THRES,
        return_degf_err_thres=RETURN_DEGF_ERR_THRES,
        outdoor_degf_err_thres=OUTDOOR_DEGF_ERR_THRES,
        mat_col=var_dict["mat_col"],
        rat_col=var_dict["rat_col"],
        oat_col=var_dict["oat_col"],
        fan_vfd_speed_col=var_dict["fan_vfd_speed_col"]
    )

    _fc2_report = FaultCodeTwoReport(
        mix_degf_err_thres=MIX_DEGF_ERR_THRES,
        return_degf_err_thres=RETURN_DEGF_ERR_THRES,
        outdoor_degf_err_thres=OUTDOOR_DEGF_ERR_THRES,
        mat_col=var_dict["mat_col"],
        rat_col=var_dict["rat_col"],
        oat_col=var_dict["oat_col"],
        fan_vfd_speed_col=var_dict["fan_vfd_speed_col"]
    )

    df = pd.read_csv(args.input, index_col="Date", parse_dates=True).rolling("5T").mean()

    '''
    # weather data from a different source
    oat = pd.read_csv('./ahu_data/oat.csv', index_col="Date", parse_dates=True).rolling("5T").mean()
    df = oat.join(df)
    df = df.ffill().bfill()
    print(df)
    '''

    # describe dataset printing some stuff
    describe_dataset(df)

    # return a whole new dataframe with fault flag as new col
    df2 = _fc2.apply(df)
    print(df2.head())
    print(df2.describe())

    save_report(args, df, _fc2_report)
