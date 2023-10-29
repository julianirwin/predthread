import pandas as pd


def standings_to_markdown(standings: pd.DataFrame):
    output_string = ""
    output_string += "Place | User | Points | PointsGained | Exacts | Corrects | Wrongs\n"
    output_string += ":--|" * 8 + "\n"
    for i, (author, row) in enumerate(standings[["Points", "PointsGained", "Exacts", "Corrects", "Wrongs"]].iterrows()):
        data_columns_string = " | ".join([str(e) for e in row.to_list()])
        output_string += f"{i + 1} | {author} | {data_columns_string}\n"
    return output_string