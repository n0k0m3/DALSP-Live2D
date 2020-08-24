import json
import os
import shutil
import lupa
from lupa import LuaRuntime
import math
import dalsp_l2d_addfeatures as l2d_add
lua = LuaRuntime(unpack_returned_tuples=True)


def readlua(luafile):
    with open(luafile, "r+", encoding="UTF-8") as f:
        dat = f.read()[7:]
        return lua.eval(dat)


def create_spirit_dict(role, string_en, hero):
    spirit_code_dict = {}
    for k in sorted(role):
        v = role[k]
        if v.heroId == 0:
            continue
        name = string_en[int(hero[v.heroId].nameTextId)].text
        if len(name.split()) == 2:
            name = " ".join(name.split()[::-1])
        spirit_code_dict[k] = name
    return spirit_code_dict


def find_id_by_name(keyword, spirit_code_dict):
    for k, v in spirit_code_dict.items():
        if keyword.lower() in v.lower():
            print("[INFO]", "Spirit Name: {:30}ID: {}".format(v, k))
            return k, v
    return None, None


def path_join_mkdirs(*pathv):
    path = ""
    for p in pathv:
        path = os.path.join(path, p)
    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        os.makedirs(folder)
    return path


def get_sound_files(resPath, model3_file_path, kanban_folder):
    with open(model3_file_path, "r+") as f:
        data = json.load(f)
    motion_dict = data["FileReferences"]["Motions"]
    for motion in motion_dict:
        file_dict = motion_dict[motion][0]
        if "Sound" in file_dict.keys():
            try:
                shutil.copy2(os.path.join(resPath, file_dict["Sound"]), path_join_mkdirs(
                    kanban_folder, file_dict["Sound"]))
            except FileNotFoundError:
                print("[ERROR]", os.path.join(
                    resPath, file_dict["Sound"]), "doesn't exist")


def get_bg_bgm(options, dress, dress_id, resPath, kanban_folder):
    v = dress[dress_id]
    if v is not None:
        if v.background != "":
            bg_file = os.path.join(resPath, v.background)
            bg_file_base = os.path.basename(bg_file)
            if options.verbose:
                print("[INFO]", "        Copying BG", bg_file_base)
            shutil.copy2(bg_file, path_join_mkdirs(
                kanban_folder, "extra", bg_file_base))
        if v.kanbanBgm != "":
            bgm_file = os.path.join(resPath, v.kanbanBgm)
            bgm_file_base = os.path.basename(bgm_file)
            if options.verbose:
                print("[INFO]", "        Copying BGM", bgm_file_base)
            shutil.copy2(bgm_file, path_join_mkdirs(
                kanban_folder, "extra", bgm_file_base))


def getfile(options):
    # Setting up data path
    resPath = os.path.join(options.dataPath, r"res/basic")
    luatablePath = os.path.join(options.dataPath, r"src/lua/table")
    bust_kanbanPath = os.path.join(resPath, r"modle/bust_kanban")

    # Load required lua
    role = readlua(os.path.join(luatablePath, "Role_en.lua"))
    string_en = readlua(os.path.join(luatablePath, "String_en.lua"))
    hero = readlua(os.path.join(luatablePath, "Hero.lua"))
    dress = readlua(os.path.join(luatablePath, "Dress.lua"))

    # Find spirit name and create folder
    spirit_code_dict = create_spirit_dict(role, string_en, hero)
    spirit_id, folder_name = find_id_by_name(
        options.spirit_need, spirit_code_dict)
    if spirit_id is None:
        print("[ERROR] Spirit doesn't exist in the database")
        return

    # change working path to the spirit folder
    curPath = path_join_mkdirs(options.wkPath, folder_name)
    kanban_id = "bust_"+str(spirit_id)

    # Copy all L2D models from bust_kanban to working path
    modelExist = False
    if options.verbose:
        print("[INFO]", "Copying L2D models to destination:")
    for folder in os.listdir(bust_kanbanPath):
        if kanban_id in folder:
            modelExist = True
            if options.verbose:
                print("[INFO]", "    Copying", os.path.join(
                    bust_kanbanPath, folder), end=" ... ")
            try:
                shutil.copytree(os.path.join(bust_kanbanPath, folder),
                                path_join_mkdirs(curPath, folder))
            except FileExistsError:
                shutil.rmtree(os.path.join(curPath, folder))
                shutil.copytree(os.path.join(bust_kanbanPath, folder),
                                path_join_mkdirs(curPath, folder))
            if options.verbose:
                print("Done")
    if modelExist is not True:
        print("[ERROR] Model for this spirit doesn't exist")
        return

    # Extras files/processes
    # MLVE file
    mlve_json = {
        "name": folder_name,
        "version": "1",
        "list": [
            {
                "character": folder_name,
                "costume": []
            }
        ]
    }
    # Other files
    if options.verbose:
        print("[INFO]", "Copying extras:")
    for folder in os.listdir(curPath):
        kanban_folder = os.path.join(curPath, folder)
        pre_dress_id = int(folder.split("_")[1])
        model3_file = "bust_{}_new.model3.json".format(pre_dress_id)
        model3_file_path = os.path.join(kanban_folder, model3_file)
        if not os.path.exists(model3_file_path):
            model3_file = "bust_{}.model3.json".format(pre_dress_id)
            model3_file_path = os.path.join(kanban_folder, model3_file)
        dress_id = pre_dress_id + 4 * \
            (10**(1+math.floor(math.log10(pre_dress_id))))

        # Copy sound files
        if options.verbose:
            print("[INFO]", "    Copying sound files for model",
                  os.path.basename(kanban_folder))
        get_sound_files(resPath, model3_file_path, kanban_folder)
        # Copy BGM and BG images
        get_bg_bgm(options, dress, dress_id, resPath, kanban_folder)
        fileout = l2d_add.edit_model3(kanban_folder, model3_file,
                                      luatablePath, dress_id, string_en, dress)
        mlve_add = {
            "name": os.path.splitext(os.path.basename(fileout))[0],
            "path": os.path.join(kanban_folder, fileout)
        }
        mlve_json["list"][0]["costume"].append(mlve_add)
    os.chdir(options.wkPath)
    with open(folder_name+".mlve", "w+") as f:
        f.write(json.dumps(mlve_json, indent=2))


if __name__ == "__main__":
    class options:
        spirit_need = "kotori"  # input spirit name needed
        dataPath = r"D:\DAL\DateALiveData"
        # get current working folder
        wkPath = os.path.join(os.getcwd(), "example")
        verbose = True
    # Load main()
    getfile(options)
