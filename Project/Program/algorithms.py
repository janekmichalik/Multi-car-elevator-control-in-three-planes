from constant import ElevatorConst


def waiter_two_elev(jinx_elev, not_jinx_elev, pnt):

    # jesli obecny punkt pechowej windy nie znajduje sie w sciezce szczesliwej windy
    # - winda pechowa czeka
    if jinx_elev.final_path[pnt - 1] \
            not in not_jinx_elev.final_path:
        wait_point = jinx_elev.final_path[pnt - 1]
        wait_pint_index = jinx_elev.final_path.index(wait_point)
        tmp = jinx_elev.final_path
        stops = 3 if wait_point == jinx_elev.DESTINATION else 2
        [tmp.insert(wait_pint_index, wait_point) for _ in range(stops)]
        return jinx_elev.final_path, not_jinx_elev.final_path
    else:
        return get_hide(jinx_elev=jinx_elev, not_jinx_elev=not_jinx_elev, pnt=pnt)


def waiter_three_elev(cnt, elevators, pnt):
    if cnt % 2:
        jinx_ids = [0, 1]
        not_jinx_id = 2
    elif cnt % 3:
        jinx_ids = [1, 2]
        not_jinx_id = 0
    else:
        jinx_ids = [0, 2]
        not_jinx_id = 1
    jinx_elev1 = elevators[jinx_ids[0]]
    jinx_elev2 = elevators[jinx_ids[1]]
    not_jinx_elev = elevators[not_jinx_id]

    # jesli obecny punkt pechowej windy nie znajduje sie w sciezce szczesliwej windy
    # - winda pechowa czeka
    if (jinx_elev1.final_path[pnt-1]
        not in jinx_elev2.final_path) and \
            (jinx_elev1.final_path[pnt-1] not in not_jinx_elev.final_path):
        wait_point1 = jinx_elev1.final_path[pnt-1]
        wait_point2 = jinx_elev2.final_path[pnt-1]
        wait_pint_index1 = jinx_elev1.final_path.index(wait_point1)
        wait_pint_index2 = jinx_elev2.final_path.index(wait_point2)

        tmp1 = jinx_elev1.final_path
        tmp2 = jinx_elev2.final_path
        stops1 = 3 if wait_point1 == jinx_elev1.DESTINATION else 2
        [tmp1.insert(wait_pint_index1, wait_point1) for _ in range(stops1)]
        stops2 = 4 if wait_point2 == jinx_elev2.DESTINATION else 3
        [tmp2.insert(wait_pint_index2, wait_point2) for _ in range(stops2)]
        return jinx_elev1.final_path, jinx_elev2.final_path, not_jinx_elev.final_path
    else:
        return get_hide_three_elev(jinx_elev1=jinx_elev1, jinx_elev2=jinx_elev2, not_jinx_elev=not_jinx_elev, pnt=pnt)


def get_hide(jinx_elev, not_jinx_elev, pnt):
    new_index = -1

    jinx_curr_pnt = jinx_elev.final_path[pnt]
    index = jinx_elev.final_path.index(jinx_curr_pnt)
    ilosc = []
    common_points = min(len(jinx_elev.final_path), len(not_jinx_elev.final_path))
    for num in range(index, common_points):
        if jinx_elev.final_path[num] == not_jinx_elev.final_path[num]:
            ilosc.append(num)
    hiding_pnt = jinx_elev.final_path[pnt - 1]
    before_hiding_pnt = jinx_elev.final_path[pnt - 1]

    not_jinx_curr_pnt = not_jinx_elev.final_path[pnt]
    not_index = not_jinx_elev.final_path.index(not_jinx_curr_pnt)
    not_rest_path = not_jinx_elev.final_path[not_index::]
    correct_pnt = int(jinx_elev.floor[hiding_pnt[1]][hiding_pnt[2]])
    cond = correct_pnt == ElevatorConst.WALL or\
           (hiding_pnt in not_rest_path or hiding_pnt == jinx_elev.final_path[index - 1])
    while cond:
        hiding_pnt = [before_hiding_pnt[0], before_hiding_pnt[1] - 1, before_hiding_pnt[2]]
        if 0 <= hiding_pnt[1] < 5 and 0 <= hiding_pnt[2] < 5:
            correct_pnt = int(jinx_elev.floor[hiding_pnt[1]][hiding_pnt[2]])
            cond = correct_pnt == ElevatorConst.WALL or \
                   (hiding_pnt in not_rest_path or hiding_pnt == jinx_elev.final_path[index - 1])
        else:
            cond = True
        if not cond:
            break
        hiding_pnt = [before_hiding_pnt[0], before_hiding_pnt[1] + 1, before_hiding_pnt[2]]
        if 0 <= hiding_pnt[1] < 5 and 0 <= hiding_pnt[2] < 5:
            correct_pnt = int(jinx_elev.floor[hiding_pnt[1]][hiding_pnt[2]])
            cond = correct_pnt == ElevatorConst.WALL or (
                    hiding_pnt in not_rest_path or hiding_pnt == jinx_elev.final_path[index - 1])
        else:
            cond = True
        if not cond:
            break
        hiding_pnt = [before_hiding_pnt[0], before_hiding_pnt[1], before_hiding_pnt[2] + 1]
        if 0 <= hiding_pnt[1] < 5 and 0 <= hiding_pnt[2] < 5:
            correct_pnt = int(jinx_elev.floor[hiding_pnt[1]][hiding_pnt[2]])
            cond = correct_pnt == ElevatorConst.WALL or (
                    hiding_pnt in not_rest_path or hiding_pnt == jinx_elev.final_path[index - 1])
        else:
            cond = True
        if not cond:
            break
        hiding_pnt = [before_hiding_pnt[0], before_hiding_pnt[1], before_hiding_pnt[2] - 1]
        if 0 <= hiding_pnt[1] < 5 and 0 <= hiding_pnt[2] < 5:
            correct_pnt = int(jinx_elev.floor[hiding_pnt[1]][hiding_pnt[2]])
            cond = correct_pnt == ElevatorConst.WALL or (
                    hiding_pnt in not_rest_path or hiding_pnt == jinx_elev.final_path[index - 1])
        else:
            cond = True
        if not cond:
            break
        else:
            before_hiding_pnt = hiding_pnt
            new_index = jinx_elev.final_path.index(jinx_elev.DESTINATION) - 1
            jinx_elev.final_path.insert(new_index, hiding_pnt)

    if not_jinx_elev.final_path[pnt] == jinx_elev.final_path[-1]:
        get_hide(jinx_elev=not_jinx_elev, not_jinx_elev=jinx_elev, pnt=pnt)
    if new_index is -1:
        new_index = jinx_elev.final_path.index(before_hiding_pnt)
    jinx_elev.final_path.insert(new_index + 1, hiding_pnt)
    [jinx_elev.final_path.insert(new_index + 1, hiding_pnt) for _ in range(2)]
    jinx_elev.final_path.insert(new_index + 4, before_hiding_pnt)
    lng = len(jinx_elev.final_path) - len(not_jinx_elev.final_path)
    [not_jinx_elev.final_path.insert(-1, not_jinx_elev.final_path[-1]) for _ in range(lng)]
    return jinx_elev.final_path, not_jinx_elev.final_path


def get_hide_three_elev(jinx_elev1, jinx_elev2, not_jinx_elev, pnt):
    new_index1, new_index2 = -1, -1

    jinx1_curr_pnt = jinx_elev1.final_path[pnt]
    jinx2_curr_pnt = jinx_elev2.final_path[pnt]
    index1 = jinx_elev1.final_path.index(jinx1_curr_pnt)
    index2 = jinx_elev2.final_path.index(jinx2_curr_pnt)
    ilosc1, ilosc2 = [], []
    common_points = min(len(jinx_elev1.final_path), len(jinx_elev2.final_path), len(not_jinx_elev.final_path))
    for num in range(index1, common_points):
        if jinx_elev1.final_path[num] == not_jinx_elev.final_path[num]:
            ilosc1.append(num)
    for num in range(index2, common_points):
        if jinx_elev2.final_path[num] == not_jinx_elev.final_path[num]:
            ilosc2.append(num)

    hiding_pnt1 = jinx_elev1.final_path[pnt - 1]
    before_hiding_pnt1 = jinx_elev1.final_path[pnt - 1]
    hiding_pnt2 = jinx_elev2.final_path[pnt - 1]
    before_hiding_pnt2 = jinx_elev2.final_path[pnt - 1]

    not_jinx_curr_pnt = not_jinx_elev.final_path[pnt]
    not_index = not_jinx_elev.final_path.index(not_jinx_curr_pnt)
    not_rest_path = not_jinx_elev.final_path[not_index::]

    correct_pnt1 = int(jinx_elev1.floor[hiding_pnt1[1]][hiding_pnt1[2]])
    correct_pnt2 = int(jinx_elev2.floor[hiding_pnt2[1]][hiding_pnt2[2]])
    cond1 = correct_pnt1 == ElevatorConst.WALL or\
           (hiding_pnt1 in not_rest_path or hiding_pnt1 == jinx_elev1.final_path[index1 - 1])
    cond2 = correct_pnt2 == ElevatorConst.WALL or\
           (hiding_pnt2 in not_rest_path or hiding_pnt2 == jinx_elev2.final_path[index2 - 1])

    while cond1 and cond2:
        hiding_pnt1 = [before_hiding_pnt1[0], before_hiding_pnt1[1] - 1, before_hiding_pnt1[2]]
        hiding_pnt2 = [before_hiding_pnt2[0], before_hiding_pnt2[1] - 1, before_hiding_pnt2[2]]
        if 0 <= hiding_pnt1[1] < 5 and 0 <= hiding_pnt1[2] < 5 and 0 <= hiding_pnt2[1] < 5 and 0 <= hiding_pnt2[2]:
            correct_pnt1 = int(jinx_elev1.floor[hiding_pnt1[1]][hiding_pnt1[2]])
            correct_pnt2 = int(jinx_elev2.floor[hiding_pnt2[1]][hiding_pnt2[2]])
            cond1 = correct_pnt1 == ElevatorConst.WALL or \
                    (hiding_pnt1 in not_rest_path or hiding_pnt1 == jinx_elev1.final_path[index1 - 1])
            cond2 = correct_pnt2 == ElevatorConst.WALL or \
                    (hiding_pnt2 in not_rest_path or hiding_pnt2 == jinx_elev2.final_path[index2 - 1])
        else:
            cond1 = True
            cond2 = True
        if not cond1 and not cond2:
            break
        hiding_pnt1 = [before_hiding_pnt1[0], before_hiding_pnt1[1] + 1, before_hiding_pnt1[2]]
        hiding_pnt2 = [before_hiding_pnt2[0], before_hiding_pnt2[1] + 1, before_hiding_pnt2[2]]
        if 0 <= hiding_pnt1[1] < 5 and 0 <= hiding_pnt1[2] < 5 and 0 <= hiding_pnt2[1] < 5 and 0 <= hiding_pnt2[2]:
            correct_pnt1 = int(jinx_elev1.floor[hiding_pnt1[1]][hiding_pnt1[2]])
            correct_pnt2 = int(jinx_elev2.floor[hiding_pnt2[1]][hiding_pnt2[2]])
            cond1 = correct_pnt1 == ElevatorConst.WALL or \
                    (hiding_pnt1 in not_rest_path or hiding_pnt1 == jinx_elev1.final_path[index1 - 1])
            cond2 = correct_pnt2 == ElevatorConst.WALL or \
                    (hiding_pnt2 in not_rest_path or hiding_pnt2 == jinx_elev2.final_path[index2 - 1])
        else:
            cond1 = True
            cond2 = True
        if not cond1 and not cond2:
            break
        hiding_pnt1 = [before_hiding_pnt1[0], before_hiding_pnt1[1], before_hiding_pnt1[2] - 1]
        hiding_pnt2 = [before_hiding_pnt2[0], before_hiding_pnt2[1], before_hiding_pnt2[2] - 1]
        if 0 <= hiding_pnt1[1] < 5 and 0 <= hiding_pnt1[2] < 5 and 0 <= hiding_pnt2[1] < 5 and 0 <= hiding_pnt2[2]:
            correct_pnt1 = int(jinx_elev1.floor[hiding_pnt1[1]][hiding_pnt1[2]])
            correct_pnt2 = int(jinx_elev2.floor[hiding_pnt2[1]][hiding_pnt2[2]])
            cond1 = correct_pnt1 == ElevatorConst.WALL or \
                    (hiding_pnt1 in not_rest_path or hiding_pnt1 == jinx_elev1.final_path[index1 - 1])
            cond2 = correct_pnt2 == ElevatorConst.WALL or \
                    (hiding_pnt2 in not_rest_path or hiding_pnt2 == jinx_elev2.final_path[index2 - 1])
        else:
            cond1 = True
            cond2 = True
        if not cond1 and not cond2:
            break
        hiding_pnt1 = [before_hiding_pnt1[0], before_hiding_pnt1[1], before_hiding_pnt1[2] + 1]
        hiding_pnt2 = [before_hiding_pnt2[0], before_hiding_pnt2[1], before_hiding_pnt2[2] + 1]
        if hiding_pnt1[1] < 5 and hiding_pnt1[2] < 5 and hiding_pnt2[1] < 5 and hiding_pnt2[2]:
            correct_pnt1 = int(jinx_elev1.floor[hiding_pnt1[1]][hiding_pnt1[2]])
            correct_pnt2 = int(jinx_elev2.floor[hiding_pnt2[1]][hiding_pnt2[2]])
            cond1 = correct_pnt1 == ElevatorConst.WALL or \
                    (hiding_pnt1 in not_rest_path or hiding_pnt1 == jinx_elev1.final_path[index1 - 1])
            cond2 = correct_pnt2 == ElevatorConst.WALL or \
                    (hiding_pnt2 in not_rest_path or hiding_pnt2 == jinx_elev2.final_path[index2 - 1])
        else:
            cond1 = True
            cond2 = True
        if not cond1 and not cond2:
            break
        else:
            before_hiding_pnt1 = hiding_pnt1
            before_hiding_pnt2 = hiding_pnt2
            new_index1 = jinx_elev1.final_path.index(jinx_elev1.DESTINATION)
            new_index2 = jinx_elev2.final_path.index(jinx_elev2.DESTINATION)
            jinx_elev1.final_path.insert(new_index1, hiding_pnt1)
            jinx_elev2.final_path.insert(new_index2, hiding_pnt2)

    if new_index1 is -1 and new_index2 is -1:
        new_index1 = jinx_elev1.final_path.index(before_hiding_pnt1)
        new_index2 = jinx_elev2.final_path.index(before_hiding_pnt2)
    jinx_elev1.final_path.insert(new_index1 + 1, hiding_pnt1)
    jinx_elev2.final_path.insert(new_index2 + 1, hiding_pnt2)
    [jinx_elev1.final_path.insert(new_index1 + 1, hiding_pnt1) for _ in range(2)]
    [jinx_elev2.final_path.insert(new_index2 + 1, hiding_pnt2) for _ in range(2)]
    jinx_elev1.final_path.insert(new_index1 + 4, before_hiding_pnt1)
    jinx_elev2.final_path.insert(new_index2 + 4, before_hiding_pnt2)
    lng1 = len(jinx_elev1.final_path) - len(not_jinx_elev.final_path)
    lng2 = len(jinx_elev2.final_path) - len(not_jinx_elev.final_path)
    [not_jinx_elev.final_path.insert(-1, not_jinx_elev.final_path[-1]) for _ in range(lng1)]
    print("BLABLABLABALABA")
    return jinx_elev1.final_path, jinx_elev2.final_path, not_jinx_elev.final_path

