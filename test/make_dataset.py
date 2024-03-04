import sys
import json
import pandas as pd

sys.path.append(".")

from config import RESULTS_FILE_PATH, TEST_DATA_PATH

RESULTS = RESULTS_FILE_PATH
PATH = TEST_DATA_PATH


def get_connections(x):
    item = json.loads(x[0])
    cabinets = list(
        map(
            lambda c, s: f"{s}-{c}",
            item["cabinet_node"],
            item["station_node"],
        )
    )
    return cabinets


def pop_id(row):
    row["CABINETS"].remove(row.name)
    return row


def wrangle(df):
    df.dropna(inplace=True)  # droppign rows witout a stationid
    df["STATIONNUMBER"] = df["STATIONNUMBER"].astype(int)
    df["id"] = df["STATIONNUMBER"].astype(str) + "-" + df["CABINETNUMBER"].astype(str)
    df = df.rename(columns={"SAP_TO_TOPOLOGY_JOIN_KEY": "TSO"}).astype(str)
    df.set_index("id", inplace=True)
    df = df.groupby(level=0).agg(lambda x: x.tolist())
    df["CABINETS"] = df["json_data"].apply(get_connections)
    df = df.apply(pop_id, axis=1)
    df = df.drop(columns=["json_data", "STATIONNUMBER", "CABINETNUMBER"])
    return df


def get_df(path):
    df = pd.read_csv(path)
    df = wrangle(df)
    return df


def main():
    df = get_df(PATH)
    df.to_csv("historic_connections.csv")


if __name__ == "__main__":
    main()
