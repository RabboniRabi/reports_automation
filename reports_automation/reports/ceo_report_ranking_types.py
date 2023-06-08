from enum import Enum

class CEOReportRankingTypes(Enum):
    PERCENT_RANKING = "percent_ranking"
    MULT_COLS_PERCENT_RANKING = "multiple_columns_percent_ranking"
    AVERAGE_RANKING = "average_ranking"
    NUMBER_RANKING = "number_ranking"