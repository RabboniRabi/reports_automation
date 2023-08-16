import sys
sys.path.append('../')
import json

import reports.data_fetcher as data_fetcher


file_open = open("configs/10th_board_results.json", "r")
config = json.load(file_open)
source_config = config["source_config"]
source_data = source_config["sources"]
type(source_data)
df_data = data_fetcher.get_data_from_config(source_data[0])
print(df_data)
file_open.close()