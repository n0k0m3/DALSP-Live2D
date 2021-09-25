import json
import logging
import math
import os
import shutil
import sys

from lupa import LuaRuntime

import dalsp_l2d_addfeatures as l2d_add

lua = LuaRuntime(unpack_returned_tuples=True)


class DALSP_L2D:
    def __init__(self, options):
        self.dataPath = os.path.abspath(options.dataPath)
        self.wkPath = os.path.abspath(options.wkPath)
        self.list = options.list
        self.spirit_need = options.spirit_need
        self.region = options.region
        self.verbose = options.verbose
        if self.verbose:
            # logger to debug.log
            FORMAT = "%(name)-10s: %(levelname)-8s %(message)s"
            logging.basicConfig(filename='../debug.log',
                                filemode='w', format=FORMAT)

            # logger to stdout
            console = logging.StreamHandler(sys.stdout)
            console.setLevel(logging.INFO)
            formatter = logging.Formatter(FORMAT)
            console.setFormatter(formatter)
            logging.getLogger().addHandler(console)
            output_file_handler = logging.FileHandler("debug.log")
            output_file_handler.setLevel(logging.INFO)
            formatter = logging.Formatter(FORMAT)
            output_file_handler.setFormatter(formatter)
            logging.getLogger().addHandler(output_file_handler)
            self.logger = logging.getLogger('DALSP_L2D')
            self.logger.setLevel(logging.INFO)

    def readlua(self, luafile):
        with open(luafile, "r+", encoding="UTF-8") as f:
            dat = f.read()[7:]
            return lua.eval(dat)

    def create_spirit_dict(self):
        spirit_code_dict = {}
        for k in sorted(self.role):
            v = self.role[k]
            try:
                name = self.role[k].enName2.strip()
            except AttributeError:
                try:
                    name = self.string[int(self.hero[v.heroId].nameTextId)].text.strip()
                except AttributeError:
                    name = self.string[self.role[k].nameId].text.strip()
            if self.region == "EN" and "Wallenstein" not in name :
                if len(name.split()) == 2:
                    name = " ".join(name.split()[::-1])
            # Hotfix Ellen
            if name == "Meizasu":
                name =  "Ellen Mira Mathers"
            spirit_code_dict[k] = name.title()
        return spirit_code_dict

    def find_id_by_name(self, keyword, spirit_code_dict):
        for k, v in spirit_code_dict.items():
            if keyword.lower() in v.lower():
                if self.verbose:
                    self.logger.info("Spirit Name: {:30}ID: {}".format(v, k))
                return k, v
        return None, None

    def path_join_mkdirs(self, *pathv):
        path = ""
        for p in pathv:
            path = os.path.join(path, p)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        return path

    def get_sound_files(self):
        with open(self.model3_file_path, "r+") as f:
            data = json.load(f)
        motion_dict = data["FileReferences"]["Motions"]
        for motion in motion_dict:
            file_dict = motion_dict[motion][0]
            if "Sound" in file_dict.keys():
                try:
                    shutil.copy2(os.path.join(self.resPath, file_dict["Sound"]), self.path_join_mkdirs(
                        self.kanban_folder, file_dict["Sound"]))
                except FileNotFoundError:
                    if self.verbose:
                        self.logger.error(os.path.join(
                            self.resPath, file_dict["Sound"])+" doesn't exist")

    def get_bg_bgm(self):
        v = self.dress[self.dress_id]
        if v is not None:
            if v.background != "":
                bg_file = os.path.join(self.resPath, v.background)
                bg_file_base = os.path.basename(bg_file)
                if self.verbose:
                    self.logger.info("        Copying BG " + bg_file_base)
                try:
                    shutil.copy2(bg_file, self.path_join_mkdirs(
                        self.kanban_folder, "extra", bg_file_base))
                except FileNotFoundError:
                    if self.verbose:
                        self.logger.error(bg_file+" doesn't exist")

            if v.kanbanBgm != "":
                bgm_file = os.path.join(self.resPath, v.kanbanBgm)
                bgm_file_base = os.path.basename(bgm_file)
                if self.verbose:
                    self.logger.info("        Copying BGM " + bgm_file_base)
                try:
                    shutil.copy2(bgm_file, self.path_join_mkdirs(
                        self.kanban_folder, "extra", bgm_file_base))
                except FileNotFoundError:
                    if self.verbose:
                        self.logger.error(bgm_file+" doesn't exist")

    def copy(self, spirit_id, folder_name):
        if spirit_id is None:
            print(f"[ERROR] Spirit {spirit_id} doesn't exist in the database")
            return

        # change working path to the spirit folder
        curPath = self.path_join_mkdirs(self.wkPath, folder_name)
        kanban_id = "bust_" + str(spirit_id)

        # Copy all L2D models from bust_kanban to working path
        modelExist = False
        if self.verbose:
            self.logger.info(
                "Copying L2D models for {} to destination".format(folder_name))
        for folder in os.listdir(self.bust_kanbanPath):
            if kanban_id in folder:
                modelExist = True
                if self.verbose:
                    self.logger.info("    Copying "+os.path.join(
                        self.bust_kanbanPath, folder))
                try:
                    shutil.copytree(os.path.join(self.bust_kanbanPath, folder),
                                    self.path_join_mkdirs(curPath, folder))
                except FileExistsError:
                    shutil.rmtree(os.path.join(curPath, folder))
                    shutil.copytree(os.path.join(self.bust_kanbanPath, folder),
                                    self.path_join_mkdirs(curPath, folder))
        if modelExist is not True:
            print(f"[ERROR] Model for spirit {spirit_id} doesn't exist")
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
        if self.verbose:
            self.logger.info("  Copying extras:")
        for folder in os.listdir(curPath):
            self.kanban_folder = os.path.join(curPath, folder)
            self.pre_dress_id = int(folder.split("_")[1])
            self.model3_file = "bust_{}_new.model3.json".format(
                self.pre_dress_id)
            self.model3_file_path = os.path.join(
                self.kanban_folder, self.model3_file)
            if not os.path.exists(self.model3_file_path):
                self.model3_file = "bust_{}.model3.json".format(
                    self.pre_dress_id)
                self.model3_file_path = os.path.join(
                    self.kanban_folder, self.model3_file)
            self.dress_id = self.pre_dress_id + 4 * \
                (10 ** (1 + math.floor(math.log10(self.pre_dress_id))))

            # Copy sound files
            if self.verbose:
                self.logger.info("    Copying sound files for model " +
                                 os.path.basename(self.kanban_folder))
            self.get_sound_files()
            # Copy BGM and BG images
            self.get_bg_bgm()
            fileout = l2d_add.edit_model3(self.kanban_folder, self.model3_file,
                                          self.luatablePath, self.dress_id, self.string, self.dress)
            mlve_add = {
                "name": os.path.splitext(os.path.basename(fileout))[0],
                "path": os.path.join(self.kanban_folder, fileout)
            }
            mlve_json["list"][0]["costume"].append(mlve_add)
        os.chdir(self.wkPath)
        with open(folder_name + ".mlve", "w+") as f:
            f.write(json.dumps(mlve_json, indent=2))
        if self.verbose:
            self.logger.info("Done copying {}".format(folder_name))

    def getfile(self):
        # Setting up data path
        self.resPath = os.path.join(self.dataPath, r"res/basic")
        self.luatablePath = os.path.join(self.dataPath, r"src/lua/table/primary")
        self.bust_kanbanPath = os.path.join(self.resPath, r"modle/bust_kanban")

        # Load required lua
        rolefile = "Role.lua"
        stringfile = "String.lua"
        herofile = "Hero.lua"
        dressfile = "Dress.lua"
        if self.region == "EN":
            #rolefile = "Role_en.lua"
            luastringPath = os.path.join(self.dataPath, r"src/lua/table/secondary/en")
            self.string = self.readlua(os.path.join(luastringPath, stringfile))
            #herofile = "Hero_en.lua"
        elif self.region == "CN":
            self.string = self.readlua(os.path.join(self.luatablePath, stringfile))
        self.role = self.readlua(os.path.join(self.luatablePath, rolefile))
        self.hero = self.readlua(os.path.join(self.luatablePath, herofile))
        self.dress = self.readlua(os.path.join(self.luatablePath, dressfile))

        # Find spirit name and create folder
        self.spirit_code_dict = self.create_spirit_dict()
        if self.list:
            print("Available Spirits")
            print("{:5}{}".format("ID", "Spirit Name"))
            for k, v in self.spirit_code_dict.items():
                print("{:5}{}".format(str(k), v))
            return

        if self.spirit_need != "all":
            spirit_id, folder_name = self.find_id_by_name(
                self.spirit_need, self.spirit_code_dict)
            self.copy(spirit_id, folder_name)
        else:
            for spirit_id, folder_name in self.spirit_code_dict.items():
                self.copy(spirit_id, folder_name)


class DALSP_L2D_mlve:
    def __init__(self, options):
        self.wkPath = os.path.abspath(options.wkPath)
        self.all = options.all
        self.region = options.region
        self.verbose = options.verbose
        if self.verbose:
            # logger to debug.log
            FORMAT = "%(name)-10s: %(levelname)-8s %(message)s"
            logging.basicConfig(filename='../debug.log',
                                filemode='w', format=FORMAT)

            # logger to stdout
            console = logging.StreamHandler(sys.stdout)
            console.setLevel(logging.INFO)
            formatter = logging.Formatter(FORMAT)
            console.setFormatter(formatter)
            logging.getLogger().addHandler(console)
            output_file_handler = logging.FileHandler("debug.log")
            output_file_handler.setLevel(logging.INFO)
            formatter = logging.Formatter(FORMAT)
            output_file_handler.setFormatter(formatter)
            logging.getLogger().addHandler(output_file_handler)
            self.logger = logging.getLogger('DALSP_L2D_MLVE')
            self.logger.setLevel(logging.INFO)

    def genmlve(self):
        os.chdir(self.wkPath)
        mlve_name = "约战 - 精灵再临"
        if self.region == "EN":
            mlve_name = "Date A Live - Spirit Pledges L2D Costumes"
        mlve_json = {
            "name": mlve_name,
            "version": "1",
            "list": []
        }
        for folder_name in os.listdir(self.wkPath):
            if os.path.isdir(folder_name):
                if not self.all:
                    mlve_json = {
                        "name": folder_name,
                        "version": "1",
                        "list": []
                    }
                character = {
                    "character": folder_name,
                    "costume": []
                }
                for root, _, files in os.walk(os.path.join(self.wkPath, folder_name)):
                    for file_name in files:
                        if "bust" not in file_name and ".model3.json" in file_name:
                            mlve_add = {
                                "name": os.path.splitext(file_name)[0],
                                "path": os.path.join(root, file_name)
                            }
                            character["costume"].append(mlve_add)
                mlve_json["list"].append(character)
                if not self.all:
                    with open(folder_name + ".mlve", "w+") as f:
                        f.write(json.dumps(mlve_json, indent=2))
        if self.all:
            with open("All.mlve", "w+") as f:
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
