import json
import os


def get_cloud_content(file, error_handling):
    if file is not None and os.path.exists(file):
        try:
            with open(file, 'r') as file:
                content = json.load(file)
                stat = {}
                for k, v in content["Summary"].items():
                    stat[k] = dict()
                    for v_k, v_v in v.items():
                        stat[k][v_k] = str(v_v["pieces"]) + " pcs"\
                        ", " + str(round(v_v["frequency"]*100, 2)) + "%"
                return {
                    "Generation": content["Generation"],
                    "Date": content["Date"],
                    "Count": str(content["Count"]),
                    "Source": content["Source"],
                    "Combinations": stat
                }
        except Exception as ex:
            print(ex)
            error_handling("Something went wrong while cloud loading")
            return None
    return None


def get_cloud_combinations(file, error_handling):
    if file is not None and os.path.exists(file):
        try:
            with open(file, 'r') as file:
                content = json.load(file)
                return content["Combos"], -1, -1
        except Exception as ex:
            print(ex)
            error_handling("Something went wrong while cloud content loading")
            return None
    return None


def save_cloud_content(path, content, error_handling):
    file_name = get_project_file_name(content)
    path = path + '/' + file_name
    file_name = path + '/' + file_name + '.ccld'
    if not os.path.exists(path): os.makedirs(path)
    try:
        with open(file_name, 'w') as file:
            json_string = json.dumps(content)
            file.write(json_string)
    except Exception:
        error_handling("Something went wrong while cloud saving")
    return file_name


def get_project_file_name(content):
    src_file_name = '_'.join(os.path.basename(content["Source"]).split('.')[:-1])
    return "{}_From_{}_For_{}".format(content["Generation"],
                                      src_file_name, content["Count"])


def save_configure(configure, error_handling):
    path = "app_data/"
    if not os.path.exists(path): os.makedirs(path)
    try:
        with open(path + 'last_session.json', 'w') as file:
            json_string = json.dumps(configure)
            file.write(json_string)
    except Exception:
        error_handling("Something went wrong while configure saving")


def load_configure(error_handling):
    path = "app_data/last_session.json"
    if os.path.exists(path):
        try:
            with open(path, 'r') as file:
                return json.load(file)
        except Exception:
            error_handling("Something went wrong while configure loading")
            return None
    return None
