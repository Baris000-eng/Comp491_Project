theme_on_off = "light_mode"

openedNewsDuringCurrentRuntime = False
def toggleOpenedNewsDuringCurrentRuntime():
    global openedNewsDuringCurrentRuntime
    openedNewsDuringCurrentRuntime = not openedNewsDuringCurrentRuntime


def getNewsCount(fromWhere):
    import UserRepository as rp
    if fromWhere == "news":
        return rp.getNewsCount
    else:
        0

