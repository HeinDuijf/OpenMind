from scipy.stats import binom

from helpers.accuracy_information import accuracy_information


def expected_accuracy(
    degree_open_mindedness: int = 10,
    competence_opposer: float = 0.7,
    competence_associate: float = 0.6,
    source_evaluative_capacity: float = 0.5,
    content_evaluative_capacity: float = 0.5,
    probability_companion_right: float = None,
):
    """Function returns the expected accuracy of an open-minded agent given certain
    input.

     Input can be either:
        a) a given degree of open-mindedness, the principal agent's competence and the
           companion's accuracy, or
        b) a given degree of open-mindedness, competences, and source and content
           evaluative capacity
        In other words, one can either input the companion's accuracy directly or this
        function calculates it from the other input

    Parameters
    ----------
    degree_open_mindedness: int
        The number of pieces of information taken into consideration
    competence_associate: float
        Competence level of associates, i.e., agents with aligned interests
    competence_opposer: float
        Competence level of opposers, i.e., agents with opposed interests
    source_evaluative_capacity: float
        Level of source evaluative capacity
    content_evaluative_capacity: float = 0.5
        Level of content evaluative capacity for right content, i.e., content that
        supports the alternative that is in the agent's best interest
    probability_companion_right: float
        The probability that a companion supports the right alternative, i.e., the
        alternative that is in the agent's best interest

    Returns
    -------
    probability_right: float
        The probability that an open-minded agent selects the right alternative, i.e.,
        the alternative that is in her best interest"""

    # 0. Special case of close-minded agent
    if degree_open_mindedness == 0:
        probability_right = competence_associate
        return probability_right

    # 1. Initialize variables
    probability_right: float = 0

    # 2. Open-minded agent
    # Calculate companion's accuracy if it has not been given as input
    if probability_companion_right is None:
        probability_companion_right = accuracy_information(
            source_evaluative_capacity=source_evaluative_capacity,
            competence_associate=competence_associate,
            competence_opposer=competence_opposer,
            content_evaluation_right=content_evaluative_capacity,
            content_evaluation_wrong=content_evaluative_capacity,
        )

    # 2.a. Case where degree_open_mindedness is even and there can be no ties.
    if (degree_open_mindedness % 2) == 0:
        # the group that determines the individual vote is odd,
        # so I win in two events:
        # (a) exactly half of the neighbors are correct and I am correct or
        # (b) more than half of the neighbors are correct
        probability_right = binom.pmf(
            degree_open_mindedness / 2,
            degree_open_mindedness,
            probability_companion_right,
        ) * competence_associate + binom.sf(
            degree_open_mindedness / 2,
            degree_open_mindedness,
            probability_companion_right,
        )
    # 2.b. Case where degree_open_mindedness is odd and there can be ties.
    else:
        # the group that determines the individual vote is even,
        # so a tie occurs in two events:
        # (a) exactly half of the neighbors minus 1 are correct and I am correct
        # (b) exactly half of the neighbors plus 1 are correct and I am incorrect
        probability_tie = binom.pmf(
            (degree_open_mindedness - 1) / 2,
            degree_open_mindedness,
            probability_companion_right,
        ) * competence_associate + binom.pmf(
            (degree_open_mindedness + 1) / 2,
            degree_open_mindedness,
            probability_companion_right,
        ) * (
            1 - competence_associate
        )
        # the group that determines the individual vote is even,
        # so I win in three events:
        # (a) exactly half of the neighbors plus 1 are correct and I am correct
        # (b) more than half of the neighbors plus 1 are correct
        # (c) there's a tie and the random choice is correct
        probability_right = (
            binom.pmf(
                (degree_open_mindedness + 1) / 2,
                degree_open_mindedness,
                probability_companion_right,
            )
            * competence_associate
            + binom.sf(
                (degree_open_mindedness + 1) / 2,
                degree_open_mindedness,
                probability_companion_right,
            )
            + probability_tie / 2
        )
    return probability_right
