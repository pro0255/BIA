from Application import Application
from experiments.ExperimentsRunner import ExperimentsRunner
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
import sys


# app = Application()
# app.start(False)

# sys.setrecursionlimit(5000) #else error when resursion :{}


exp = ExperimentsRunner()
exp.start_experiments_for_functions()
