import pandas as pd


def standings_to_markdown(standings: pd.DataFrame):
    output_string = ""
    output_string += "User | Points | PointsGained | Exacts | Corrects | Wrongs\n"
    output_string += ":--|" * 7 + "\n"
    for author, row in standings[["Points", "PointsGained", "Exacts", "Corrects", "Wrongs"]].iterrows():
        data_columns_string = " | ".join([str(e) for e in row.to_list()])
        output_string += f"{author} | {data_columns_string}\n"
    print(output_string)