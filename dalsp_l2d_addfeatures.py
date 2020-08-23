import os
import json
import re
from lupa import LuaRuntime
lua = LuaRuntime(unpack_returned_tuples=True)


def add_features(dress_id, interaction, intimacy_dict, dat, string_en):
    motion_new_dict = {
        "TuiTap": [],
        "HeadTap": [],
        "BodyTap": []
    }

    tap_map = {
        "tui": "TuiTap",
        "head": "HeadTap",
        "body": "BodyTap"
    }

    motion_set = set()

    for k, inter in interaction.items():
        if inter.modelId == dress_id+100000:
            motion_name = inter.action1
            motion_set.add(motion_name)

            # add subtitles
            v = dat["FileReferences"]["Motions"][motion_name]
            s = []
            for value in inter.lineShow.values():
                s.append(string_en[value].text)
            s = "{$br}".join(s[::-1])
            v[0]["Text"] = s

            # # add intimacy
            # if "Intimacy" not in v[0]:
            #     v[0]["Intimacy"] = {}
            #     v[0]["Intimacy"]["Min"] = intimacy_dict[inter.favor]
            # else:
            #     v[0]["Intimacy"]["Min"] = min(v[0]["Intimacy"]["Min"],intimacy_dict[inter.favor])

    # rearrange to tapping position
            if v[0] not in motion_new_dict[tap_map[inter.position]]:
                motion_new_dict[tap_map[inter.position]].append(v[0])
    dat["FileReferences"]["Motions"].update(motion_new_dict)
    d = dat["FileReferences"]["Motions"]
    for motion_name in motion_set:
        d.pop(motion_name, None)


def delete_keys(dat):
    for v in dat["FileReferences"]["Motions"].values():
        # delete unnecessary keys
        v[0].pop("FadeInTime", None)
        v[0].pop("FadeOutTime", None)


def readlua(luafile):
    with open(luafile, "r+", encoding="UTF-8") as f:
        dat = f.read()[7:]
        return lua.eval(dat)


def edit_model3(path, filename, luatablePath, dress_id, string_en, dress):
    dict_add = """{
        "Controllers": {
            "ParamHit": {},
            "ParamLoop": {},
            "KeyTrigger": {},
            "EyeBlink": {
                "MinInterval": 500,
                "MaxInterval": 6000,
                "Enabled": true
            },
            "LipSync": {
                "Gain": 5.0,
                "Items": [
                    {
                        "Id": "PARAM_MOUTH_OPEN_Y",
                        "Min": 0.0,
                        "Max": 1.0,
                        "Input": 0
                    }
                ],
                "Enabled": true
            },
            "MouseTracking": {
                "SmoothTime": 0.15,
                "Enabled": true
            },
            "AutoBreath": {
                "Enabled": true
            },
            "ExtraMotion": {
                "Enabled": true
            },
            "Accelerometer": {
                "Enabled": true
            },
            "Microphone": {},
            "Transform": {},
            "FaceTracking": {
                "Enabled": true
            },
            "ParamValue": {},
            "PartOpacity": {},
            "ArtmeshOpacity": {},
            "ArtmeshColor": {},
            "ArtmeshCulling": {
                "DefaultMode": 0
            },
            "IntimacySystem": {}
        },
        "HitAreas": [
            {
                "Name": "head",
                "Id": "HitArea",
                "Motion": "HeadTap"
            },
            {
                "Name": "body",
                "Id": "HitArea2",
                "Motion": "BodyTap"
            },
            {
                "Name": "tui",
                "Id": "HitArea3",
                "Motion": "TuiTap"
            }
        ],
        "Options": {}}"""
    dict_add = json.loads(dict_add)
    intimacy_dict = {
        1: 0,
        2: 10,
        3: 20,
        4: 35,
        5: 50}
    interaction = readlua(os.path.join(luatablePath, "Interaction.lua"))
    os.chdir(path)
    with open(filename, "r") as f:
        dat = json.load(f)
    dat.update(dict_add)
    dat.pop("Groups", None)
    delete_keys(dat)
    add_features(dress_id, interaction, intimacy_dict, dat, string_en)
    try:
        ss = string_en[dress[dress_id].nameTextId].text
    except:
        ss = "Unnamed"
    fileout = ss+".model3.json"
    fileout = re.sub(r'[\\/*?:"<>|]', "", fileout)

    with open(fileout, "w+") as f:
        f.write(json.dumps(dat, indent=2))


if __name__ == "__main__":
    class options:
        dataPath = r"D:\DAL\DateALiveData"
    dress_id = 410511
    luatablePath = os.path.join(options.dataPath, r"src/lua/table")
    string_en = readlua(os.path.join(luatablePath, "String_en.lua"))
    dress = readlua(os.path.join(luatablePath, "Dress.lua"))
    path = r"D:\DAL\Live2D\example\Itsuka Kotori\bust_10511_superKanban"
    filename = 'bust_10511_new.model3.json'
    edit_model3(path, filename, luatablePath, dress_id, string_en, dress)
