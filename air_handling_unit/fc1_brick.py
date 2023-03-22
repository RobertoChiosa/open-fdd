import os

import brickschema
import pandas as pd

from faults import FaultConditionOne
from reports import FaultCodeOneReport
from utils import custom_arg_parser, save_report, describe_dataset
from utils_brick import parse_results

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

    ###########################
    # load data
    df = pd.read_csv(args.input, index_col="Datetime", parse_dates=True).rolling('5T').mean()
    # describe dataset printing some stuff
    describe_dataset(df)

    # load metadata and find the relative columns requested
    # generate a blank graph
    g = brickschema.Graph()
    # g = brickschema.Graph(load_brick_nightly=True)
    # adds the system metadata schema to the graph
    g.parse(os.path.join('ahu_data', 'SDAHU.ttl'))
    g.parse(os.path.join('ahu_data', 'Brick.ttl'),
            format='turtle')  # Load Brick schema. We need it to exploit the hierarchy.
    q = """
        select ?duct_static_col ?supply_vfd_speed_col ?duct_static_setpoint_col where {
            ?duct_static_col rdf:type brick:Supply_Air_Static_Pressure_Sensor .
            ?supply_vfd_speed_col rdf:type brick:Speed_Setpoint .
            bldg:Supply_Air_Fan brick:hasPoint ?supply_vfd_speed_col .
            ?duct_static_setpoint_col rdf:type brick:Supply_Air_Static_Pressure_Setpoint .
        }
    """
    res = g.query(q)

    res_df = parse_results(res, df=True)
    # convert res_df to dict
    res_dict = res_df.to_dict('records')[0]
    # remove blg: prefix
    res_dict = {k: v.replace('bldg:', '') for k, v in res_dict.items()}
    ###########################

    # G36 params shouldn't need adjusting
    # error threshold parameters
    VFD_SPEED_PERCENT_ERR_THRES = 0.05
    VFD_SPEED_PERCENT_MAX = 0.99
    DUCT_STATIC_INCHES_ERR_THRES = 0.1

    _fc1 = FaultConditionOne(
        vfd_speed_percent_err_thres=VFD_SPEED_PERCENT_ERR_THRES,
        vfd_speed_percent_max=VFD_SPEED_PERCENT_MAX,
        duct_static_inches_err_thres=DUCT_STATIC_INCHES_ERR_THRES,
        duct_static_col=res_dict['duct_static_col'],
        supply_vfd_speed_col=res_dict['supply_vfd_speed_col'],
        duct_static_setpoint_col=res_dict['duct_static_setpoint_col']
    )

    _fc1_report = FaultCodeOneReport(
        vfd_speed_percent_err_thres=VFD_SPEED_PERCENT_ERR_THRES,
        vfd_speed_percent_max=VFD_SPEED_PERCENT_MAX,
        duct_static_inches_err_thres=DUCT_STATIC_INCHES_ERR_THRES,
        duct_static_col=res_dict['duct_static_col'],
        supply_vfd_speed_col=res_dict['supply_vfd_speed_col'],
        duct_static_setpoint_col=res_dict['duct_static_setpoint_col']
    )

    # return a whole new dataframe with fault flag as new col
    df2 = _fc1.apply(df)
    print(df2.head())
    print(df2.describe())

    save_report(args, df, _fc1_report)
