def percentile(x, ys):
    """
    Calculated percentile score of the user with karma (x) among all users with the following list of karmas (ys)

    :param x: The karma of the user whose percentile score is desired
    :param ys: The karma of all the users who are interacting with the platform. Interaction -> Asks Question, Answers
    :return: percentile score of the user
    """
    sz_y = len(ys)
    if sz_y == 0:
        return -1
    elif sz_y == 1:
        return 0.
    else:
        return sum(y < x for y in ys) / float(len(ys) - 1) * 100
