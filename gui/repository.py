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
            error_handling("Something went wrong \nwhile cloud loading")
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
            error_handling("Something went wrong \nwhile cloud content loading")
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
        error_handling("Something went wrong \nwhile cloud saving")
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
        error_handling("Something went wrong \nwhile configure saving")


def update_meta_file(meta, file_path, error_handling):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            file_json = json.loads(file_content)

        if file_json is not None:
            edition = file_json["edition"]

            img_name = file_json["image"].split("/")[-1].split('.')
            if len(img_name) > 1:
                image = img_name[-2]
            else:
                image = img_name[0]
            print("img", image)


            exp = file_json["image"].split(".")
            if len(exp) > 1:
                exp = exp[-1]
            else:
                exp = None
            print("exp", exp)
            meta_json = getMetaFrom(meta, edition, image, exp)

            with open(file_path, 'w') as file:
                json.dump(file_json | meta_json, file)
    except LookupError as e:
        print(e)
        error_handling("Something went wrong \nwhile meta updating")


def update_meta_dir(meta, dir_path, error_handling):
    pass


def getMetaFrom(meta: dict, N, image_name, exp):
    metadata = {}
    if meta.keys().__contains__("name"):
        metadata["name"] = meta["name"] + " #" + str(N)

    if meta.keys().__contains__("ipfs(image)"):
        if exp is None:
            name = image_name
        else:
            name = image_name + "." + exp
        metadata["image"] = meta["ipfs(image)"] + "/" + name

    if meta.keys().__contains__("collection/name"):
        if not metadata.keys().__contains__("collection"):
            metadata["collection"] = {}
        metadata["collection"]["name"] = meta["collection/name"]

    if meta.keys().__contains__("collection/family"):
        if not metadata.keys().__contains__("collection"):
            metadata["collection"] = {}
        metadata["collection"]["family"] = meta["collection/family"]

    if meta.keys().__contains__("properties/creators/address"):
        if not metadata.keys().__contains__("properties"):
            metadata["properties"] = {}
        if not metadata["properties"].keys().__contains__("creators"):
            metadata["properties"]["creators"] = {}
        metadata["properties"]["creators"]["address"] = meta["properties/creators/address"]

    if meta.keys().__contains__("properties/creators/share"):
        if not metadata.keys().__contains__("properties"):
            metadata["properties"] = {}
        if not metadata["properties"].keys().__contains__("creators"):
            metadata["properties"]["creators"] = {}
        metadata["properties"]["creators"]["share"] = meta["properties/creators/share"]
    return metadata


def load_configure(error_handling):
    path = "app_data/last_session.json"
    if os.path.exists(path):
        try:
            with open(path, 'r') as file:
                return json.load(file)
        except Exception:
            error_handling("Something went wrong \nwhile configure loading")
            return None
    return None
