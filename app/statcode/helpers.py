# Find a better way :(


def zipHelper(mList):
    if len(mList) == 2:
        zippedList = []
        cutOffPoint = len(mList[0])
        for i, col in enumerate(mList):
            if i + 1 != len(mList):
                for index, val in enumerate(col):
                    zippedList.append(val + " " + mList[len(mList) - 1][index])
        return zippedList[0:cutOffPoint]

    if len(mList) == 3:
        zippedList = []
        cutOffPoint = len(mList[0])
        for i, col in enumerate(mList):
            for index, val in enumerate(col):
                zippedList.append(
                    val + " " + mList[1][index] + " " + mList[len(mList) - 1][index]
                )
        return zippedList[0:cutOffPoint]

    if len(mList) == 4:
        zippedList = []
        cutOffPoint = len(mList[0])
        for i, col in enumerate(mList):
            for index, val in enumerate(col):
                zippedList.append(
                    val
                    + " "
                    + mList[1][index]
                    + " "
                    + mList[2][index]
                    + " "
                    + mList[len(mList) - 1][index]
                )
        return zippedList[0:cutOffPoint]

    if len(mList) == 5:
        zippedList = []
        cutOffPoint = len(mList[0])
        for i, col in enumerate(mList):
            for index, val in enumerate(col):
                zippedList.append(
                    val
                    + " "
                    + mList[1][index]
                    + " "
                    + mList[2][index]
                    + " "
                    + mList[3][index]
                    + " "
                    + mList[len(mList) - 1][index]
                )
        return zippedList[0:cutOffPoint]

    if len(mList) == 6:
        zippedList = []
        cutOffPoint = len(mList[0])
        for i, col in enumerate(mList):
            for index, val in enumerate(col):
                zippedList.append(
                    val
                    + " "
                    + mList[1][index]
                    + " "
                    + mList[2][index]
                    + " "
                    + mList[3][index]
                    + " "
                    + mList[4][index]
                    + " "
                    + mList[len(mList) - 1][index]
                )
        return zippedList[0:cutOffPoint]

    if len(mList) == 7:
        zippedList = []
        cutOffPoint = len(mList[0])
        for i, col in enumerate(mList):
            for index, val in enumerate(col):
                zippedList.append(
                    val
                    + " "
                    + mList[1][index]
                    + " "
                    + mList[2][index]
                    + " "
                    + mList[3][index]
                    + " "
                    + mList[4][index]
                    + " "
                    + mList[5][index]
                    + " "
                    + mList[len(mList) - 1][index]
                )
        return zippedList[0:cutOffPoint]

    if len(mList) == 8:
        zippedList = []
        cutOffPoint = len(mList[0])
        for i, col in enumerate(mList):
            for index, val in enumerate(col):
                zippedList.append(
                    val
                    + " "
                    + mList[1][index]
                    + " "
                    + mList[2][index]
                    + " "
                    + mList[3][index]
                    + " "
                    + mList[4][index]
                    + " "
                    + mList[5][index]
                    + " "
                    + mList[6][index]
                    + " "
                    + mList[len(mList) - 1][index]
                )
        return zippedList[0:cutOffPoint]

    if len(mList) == 9:
        zippedList = []
        cutOffPoint = len(mList[0])
        for i, col in enumerate(mList):
            for index, val in enumerate(col):
                zippedList.append(
                    val
                    + " "
                    + mList[1][index]
                    + " "
                    + mList[2][index]
                    + " "
                    + mList[3][index]
                    + " "
                    + mList[4][index]
                    + " "
                    + mList[5][index]
                    + " "
                    + mList[6][index]
                    + " "
                    + mList[7][index]
                    + " "
                    + mList[len(mList) - 1][index]
                )
        return zippedList[0:cutOffPoint]

    if len(mList) == 10:
        zippedList = []
        cutOffPoint = len(mList[0])
        for i, col in enumerate(mList):
            for index, val in enumerate(col):
                zippedList.append(
                    val
                    + " "
                    + mList[1][index]
                    + " "
                    + mList[2][index]
                    + " "
                    + mList[3][index]
                    + " "
                    + mList[4][index]
                    + " "
                    + mList[5][index]
                    + " "
                    + mList[6][index]
                    + " "
                    + mList[7][index]
                    + " "
                    + mList[8][index]
                    + " "
                    + mList[len(mList) - 1][index]
                )
        return zippedList[0:cutOffPoint]

