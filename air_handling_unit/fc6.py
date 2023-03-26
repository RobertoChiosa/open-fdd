from datetime import timedelta

import pandas as pd

from faults import FaultConditionSix
from reports import FaultCodeSixReport
from utils import custom_arg_parser, save_report, describe_dataset

# python 3.10 on Windows 10
# py .\fc6.py -i ./ahu_data/hvac_random_fake_data/fc6_fake_data1.csv -o fake1_ahu_fc6_report
# todo make it run
if __name__ == '__main__':
    args = custom_arg_parser()

    # G36 params shouldn't need adjusting
    # error threshold parameters
    OAT_DEGF_ERR_THRES = 5
    RAT_DEGF_ERR_THRES = 2
    DELTA_TEMP_MIN = 10
    AIRFLOW_ERR_THRES = .3

    # THIS G36 params NEEDs INPUT It's for the OA
    # ventilation setpoint. Most AHU systems will
    # not have an air flow station with a trend log avail
    # for vent setpoint but instead use a fixed OA setpoint
    # that test & balance (TAB) contractor implements at
    # building startup. Find blueprint records or TAB
    # report for what CFM setpoint the mechanical
    # engineer used to design the system. This param
    # will be right in the mechanical schedule for
    # the AHU along with all other output params for
    # how the AHU was sized to meet all the engineers
    # mechanical requirements
    AHU_MIN_CFM_DESIGN = 2500

    # ADJUST this param for the AHU MIN OA damper stp
    # To verify AHU is operating in Min OA OS1 & OS4 states only
    AHU_MIN_OA_DPR = 20

    var_dict = {
        "vav_total_flow_col": "vav_total_flow",
        "mat_col": "mat",
        "oat_col": "oat",
        "rat_col": "rat",
        "fan_vfd_speed_col": "supply_vfd_speed",
        "economizer_sig_col": "economizer_sig",
        "heating_sig_col": "heating_sig",
        "cooling_sig_col": "cooling_sig"
    }

    _fc6 = FaultConditionSix(
        airflow_err_thres=AIRFLOW_ERR_THRES,
        ahu_min_cfm_design=AHU_MIN_CFM_DESIGN,
        oat_degf_err_thres=OAT_DEGF_ERR_THRES,
        rat_degf_err_thres=RAT_DEGF_ERR_THRES,
        oat_rat_delta_min=DELTA_TEMP_MIN,
        ahu_min_oa_dpr=AHU_MIN_OA_DPR,
        vav_total_flow_col=var_dict["vav_total_flow_col"],
        mat_col=var_dict["mat_col"],
        oat_col=var_dict["oat_col"],
        rat_col=var_dict["rat_col"],
        fan_vfd_speed_col=var_dict["fan_vfd_speed_col"],
        economizer_sig_col=var_dict["economizer_sig_col"],
        heating_sig_col=var_dict["heating_sig_col"],
        cooling_sig_col=var_dict["cooling_sig_col"]
    )

    _fc6_report = FaultCodeSixReport(
        vav_total_flow_col=var_dict["vav_total_flow_col"],
        mat_col=var_dict["mat_col"],
        oat_col=var_dict["oat_col"],
        rat_col=var_dict["rat_col"],
        fan_vfd_speed_col=var_dict["fan_vfd_speed_col"],
    )

    df = pd.read_csv(args.input, index_col="Date", parse_dates=True).rolling(timedelta(minutes=5)).mean()

    # describe dataset printing some stuff
    describe_dataset(df)

    # return a whole new dataframe with fault flag as new col
    df2 = _fc6.apply(df)
    print(df2.head())
    print(df2.describe())
    print(df2.columns)
    save_report(args, df, _fc6_report)
