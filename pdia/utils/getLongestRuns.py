import itertools


def getLongestRuns(label, events):
    """Takes a Pandas series 'label' and a list of 'events', returns the longest run of events.
    It uses values not in the events list as "run stoppers" and does NOT report on their lengths.

    :param label: a Pandas series containing distinctive values.
    :param events: a list of values considered part of the runs
    :returns: the length of the longest run of values in the events list. 0 if none appeared.
    """
    # see http://stackoverflow.com/questions/16857407/pandas-run-length-of-nan-holes
    counts = [len(list(g)) for k, g in itertools.groupby(label, lambda x: x in (events)) if k]
    return 0 if len(counts) == 0 else max(counts)