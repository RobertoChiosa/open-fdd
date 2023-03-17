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

import pandas as pd

from faults import FaultConditionThirteen
from reports import FaultCodeThirteenReport


def custom_arg_parser():
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
