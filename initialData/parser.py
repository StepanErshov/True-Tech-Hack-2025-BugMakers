import pandas as pd
from typing import Tuple


def read_xlsx(path: str) -> Tuple:

    data = pd.read_excel(
        path, sheet_name="Лист1", keep_default_na=True, engine="openpyxl"
    )

    return data.to_dict(orient="records")


# pprint.pprint(read_xlsx("Golden set Q&A для хакатона.xlsx"))
