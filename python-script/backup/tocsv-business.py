import json
import pandas as pd

def export_to_csv():
    file_path = '../input-data/yelp-dataset/yelp_academic_dataset_business.json'
    with open(file_path) as f:
        data = [json.loads(line) for line in f]
        df = pd.json_normalize(data)
        for col in df.columns:
            if isinstance(df[col][0], dict):
                level_1_cols = []
                for key in df[col][0].keys():
                    if isinstance(df[col][0][key], dict):
                        level_2_cols = []
                        for sub_key in df[col][0][key].keys():
                            if isinstance(df[col][0][key][sub_key], dict):
                                level_3_cols = []
                                for sub_sub_key in df[col][0][key][sub_key].keys():
                                    col_name = col + '_' + key + '_' + sub_key + '_' + sub_sub_key
                                    df[col_name] = df[col].apply(lambda x: x.get(key, {}).get(sub_key, {}).get(sub_sub_key))
                                    level_3_cols.append(col_name)
                                col_name = col + '_' + key + '_' + sub_key
                                df = df.drop(columns=col_name)
                                level_2_cols.extend(level_3_cols)
                            else:
                                col_name = col + '_' + key + '_' + sub_key
                                df[col_name] = df[col].apply(lambda x: x.get(key, {}).get(sub_key))
                                level_2_cols.append(col_name)
                        col_name = col + '_' + key
                        df = df.drop(columns=col_name)
                        level_1_cols.extend(level_2_cols)
                    else:
                        col_name = col + '_' + key
                        df[col_name] = df[col].apply(lambda x: x.get(key))
                        level_1_cols.append(col_name)
                df = df.drop(columns=col)
                df = df[level_1_cols]
        df.to_csv('../output-data/business.csv', index=False)

export_to_csv()
