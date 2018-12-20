import string


def num2alpha(num, maxNumberOfOptions=8):
    """
    Function to turn an integer to A,B,C,D, etc. If out of range, return the num itself
    :param num: input, presumably an integer but can be anything
    :param maxNumberOfOptions: the max integer to convert
    :return: A letter, or the num itself
    """
    if not isinstance(num, int):
        try:
            num = int(num)
        except ValueError:
            return num
    # we have an int now
    try:
        return dict(list(zip(list(range(1, maxNumberOfOptions + 1)), string.ascii_uppercase)))[num]
    except KeyError:
        return num


def alpha2num(alpha, maxNumberOfOptions=8):
    """
    Funtion to turn a single letter to its numerical correspondence (e.g., "A"==1, etc.); if error, return the input

    :param alpha: a single letter; or can be anything
    :return: the numeric correspondence of the input; or the input itself
    """
    try:
        return dict(list(zip(string.ascii_uppercase, list(range(1, maxNumberOfOptions+1)))))[alpha]
    except KeyError:
        return alpha