from constant import ElevatorConst


def waiter_two_elev(jinx_elev, not_jinx_elev, pnt, find_again, other_elev):

    # jesli obecny punkt pechowej windy nie znajduje sie w sciezce szczesliwej windy
    # - winda pechowa czeka
    if jinx_elev.final_path[pnt - 1] \
            not in not_jinx_elev.final_path:
        wait_point = jinx_elev.final_path[pnt - 1]
        wait_pint_index = jinx_elev.final_path.index(wait_point)
        stops = 3 if wait_point == jinx_elev.DESTINATION else 2
        [jinx_elev.final_path.insert(wait_pint_index, wait_point) for _ in range(stops)]
        return jinx_elev.final_path, not_jinx_elev.final_path
    else:
        return get_hide(jinx_elev=jinx_elev, not_jinx_elev=not_jinx_elev, pnt=pnt, find_again=find_again,
                        other_elev=other_elev)


def get_hide(jinx_elev, not_jinx_elev, pnt, find_again, other_elev=None):
    new_index = -1

    RESTRICTED = []
    if other_elev:
        RESTRICTED.append(other_elev[pnt - 1])
    RESTRICTED.append(jinx_elev.final_path[pnt - 1])
    RESTRICTED.append(not_jinx_elev.final_path[pnt])
    # punkt - schowek
    hiding_pnt = jinx_elev.final_path[pnt - 1]
    # punkt - zapamietany schowek
    previous_hiding_pnt = hiding_pnt

    cond = True

    steps_for_while = 0
    while cond and steps_for_while < 4:
        print("Inf")
        # zwraca liste mozliwych schowkow
        hiding_pnts = get_hiden_points(previous_hiding_pnt, jinx_elev, jinx_elev.final_path[pnt-1], RESTRICTED)
        for point in hiding_pnts:
            if _check_cond(jinx_elev, not_jinx_elev, pnt, point, RESTRICTED):
                hiding_pnt = point
                steps_for_while = 4
                # RESTRICTED.append(hiding_pnt)
                break
            else:
                previous_hiding_pnt = point
                if point != jinx_elev.final_path[pnt]:
                    new_index = jinx_elev.final_path.index(jinx_elev.DESTINATION) + 3
                    jinx_elev.final_path.insert(new_index, point)

        steps_for_while = steps_for_while + 1

    if new_index is -1:
        new_index = jinx_elev.final_path.index(previous_hiding_pnt)
    jinx_elev.final_path.insert(new_index + 1, hiding_pnt)
    if not find_again:
        [jinx_elev.final_path.insert(new_index + 1, hiding_pnt) for _ in range(2)]
        jinx_elev.final_path.insert(new_index + 4, previous_hiding_pnt)
    lng = len(jinx_elev.final_path) - len(not_jinx_elev.final_path)
    [not_jinx_elev.final_path.insert(-1, not_jinx_elev.final_path[-1]) for _ in range(lng)]

    if find_again:
        num = jinx_elev.final_path[new_index+2:].count(jinx_elev.DESTINATION)
        jinx_elev.final_path[new_index + 2:] = num*[hiding_pnt]

    return jinx_elev.final_path, not_jinx_elev.final_path


def _check_cond(jinx_elev, not_jinx_elev, pnt, hiding_pnt, RESTRICTED):
    # sprawdzenie czy pierwszy punkt - schowek nie jest sciana
    is_not_wall = int(jinx_elev.floor[hiding_pnt[1]][hiding_pnt[2]])
    # warunek prawidlowego punktu-schowka:
    # nie jest sciana, nie zawiera sie w sciezce windy niechowajacej, nie jest punktem koncowym windy chowajacej
    cond = is_not_wall != ElevatorConst.WALL and \
           (hiding_pnt not in RESTRICTED) and \
           (hiding_pnt not in not_jinx_elev.final_path[pnt-1:])

    return cond


def get_hiden_points(curr_pnt, jinx_elev, prev, RESTRICTED):
    hidden_points = [
                        [curr_pnt[0], curr_pnt[1], curr_pnt[2] - 1],
                        [curr_pnt[0], curr_pnt[1], curr_pnt[2] + 1],
                        [curr_pnt[0], curr_pnt[1] - 1, curr_pnt[2]],
                        [curr_pnt[0], curr_pnt[1] + 1, curr_pnt[2]]
                    ]
    new = []
    for pnt in hidden_points:
        if not (0 <= pnt[1] < 5 and 0 <= pnt[2] < 5):
            new.append(pnt)
        elif int(jinx_elev.floor[pnt[1]][pnt[2]]) == ElevatorConst.WALL:
            new.append(pnt)
        elif pnt in RESTRICTED:
            new.append(pnt)
        elif pnt == prev:
            new.append(pnt)
        # elif pnt == not_jix_prev_pnt:
        #     new.append(pnt)
        # elif pnt == elev_waiter_pnt:
        #     new.append(pnt)
    tmp = [pkt for pkt in hidden_points if pkt not in new]
    return tmp


def _pick_jinxs(cnt, elevators, reversed=False):
    if cnt % 2:
        jinx_ids = [0, 1]
        not_jinx_id = 2
    elif cnt % 3:
        jinx_ids = [1, 2]
        not_jinx_id = 0
    else:
        jinx_ids = [0, 2]
        not_jinx_id = 1

    if reversed:
        jinx_elev1_waiter = elevators[jinx_ids[1]]
        jinx_elev2_hider = elevators[jinx_ids[0]]
        not_jinx_elev = elevators[not_jinx_id]
    else:
        jinx_elev1_waiter = elevators[jinx_ids[0]]
        jinx_elev2_hider = elevators[jinx_ids[1]]
        not_jinx_elev = elevators[not_jinx_id]

    return jinx_elev1_waiter, jinx_elev2_hider, not_jinx_elev


def waiter_three_elev(jinx_elev1_waiter, jinx_elev2_hider, not_jinx_elev, pnt):

    jinx_elev1 = jinx_elev1_waiter
    jinx_elev2 = jinx_elev2_hider
    # jesli obecny punkt pechowej windy nie znajduje sie w sciezce szczesliwej windy
    # - winda pechowa czeka
    if (jinx_elev1.final_path[pnt-1]
        not in jinx_elev2.final_path) and \
            (jinx_elev1.final_path[pnt-1] not in not_jinx_elev.final_path) and \
            (jinx_elev2.final_path[pnt - 1] not in jinx_elev1.final_path and
             jinx_elev2.final_path[pnt - 1] not in not_jinx_elev.final_path) and \
            (not_jinx_elev.final_path[pnt-1] not in jinx_elev1.final_path and
             not_jinx_elev.final_path[pnt-1] not in jinx_elev2.final_path):
        wait_point1 = jinx_elev1.final_path[pnt-1]
        wait_point2 = jinx_elev2.final_path[pnt-1]

        stops1 = 3 if wait_point1 == jinx_elev1.DESTINATION else 2
        [jinx_elev1.final_path.insert(pnt-1, wait_point1) for _ in range(stops1)]
        stops2 = 5 if wait_point2 == jinx_elev2.DESTINATION else 4
        [jinx_elev2.final_path.insert(pnt-1, wait_point2) for _ in range(stops2)]
        return jinx_elev1.final_path, jinx_elev2.final_path, not_jinx_elev.final_path
    else:
        wait_point = jinx_elev1_waiter.final_path[pnt-1]
        [jinx_elev1_waiter.final_path.insert(pnt-1, wait_point) for _ in range(6)]
        not_jinx_elev.final_path.insert(pnt-1, not_jinx_elev.final_path[pnt-1])
        jinx_elev2_hider.final_path, not_jinx_elev.final_path =\
            get_hide(jinx_elev=jinx_elev2_hider, not_jinx_elev=not_jinx_elev,
                     pnt=pnt, find_again=False, other_elev=jinx_elev1_waiter.final_path)
        return jinx_elev1_waiter.final_path, jinx_elev2_hider.final_path, not_jinx_elev.final_path
