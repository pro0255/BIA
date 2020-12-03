from functions.LateralSurfaceArea import LateralSurfaceArea
from functions.TotalArea import TotalArea
from selection.MaxMinEnum import Approach

MULTI_OBJECTIVE = [LateralSurfaceArea(), TotalArea()]
TASK_APPROACHES = [Approach.Minimazation, Approach.Minimazation]
