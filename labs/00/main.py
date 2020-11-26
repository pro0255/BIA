from Application import Application
from experiments.ExperimentsRunner import ExperimentsRunner
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

# app = Application()
# app.start(False)

exp = ExperimentsRunner()
exp.start_experiments_for_functions()
