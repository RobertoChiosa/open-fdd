# Author:       Roberto Chiosa
# Copyright:    Roberto Chiosa, © 2023
# Email:        roberto.chiosa@pinvision.it
#
# Created:      16/03/23
# Script Name:  utils.py
# Path:         air_handling_unit
#
# Script Description:
#
#
# Notes:

import argparse

import os


def custom_arg_parser():
    """
    Parse command line arguments. Used in all py functions and war duplicated
    """
    parser = argparse.ArgumentParser(add_help=False)
    args = parser.add_argument_group("Options")

    args.add_argument(
        "-h", "--help", action="help", help="Show this help message and exit."
    )
    args.add_argument("-i", "--input", required=True, type=str, help="CSV File Input")
    args.add_argument(
        "-o", "--output", required=True, type=str, help="Word File Output Name"
    )
    """
    FUTURE 
     * incorporate an arg for SI units 
     * °C on temp sensors
     * piping pressure sensor PSI conversion
     * air flow CFM conversion
     * AHU duct static pressure "WC
    
    args.add_argument('--use-SI-units', default=False, action='store_true')
    args.add_argument('--no-SI-units', dest='use-SI-units', action='store_false')
    """
    args = parser.parse_args()
    return args


def save_report(args, df, report):
    document = report.create_report(args.output, df)
    path = os.path.join(os.path.curdir, "final_report")
    if not os.path.exists(path):
        os.makedirs(path)
    document.save(os.path.join(path, f"{args.output}.docx"))


# create a function to describe dataset
def describe_dataset(df):
    start = df.head(1).index.date
    print("Dataset start: ", start)

    end = df.tail(1).index.date
    print("Dataset end: ", end)

    for col in df.columns:
        print("df column: ", col, "- max len: ", df[col].size)
