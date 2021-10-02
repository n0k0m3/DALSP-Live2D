from lupa import LuaRuntime

lua = LuaRuntime(unpack_returned_tuples=True)
def readlua(luafile):
    with open(luafile, "r+", encoding="UTF-8") as f:
        dat = f.read()[7:]
        return lua.eval(dat)
