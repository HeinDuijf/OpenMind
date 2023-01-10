from scipy.stats import binom


def accuracy_information(
    source_evaluative_capacity: float,
    competence_associate: float,
    competence_opposer: float,
    content_evaluation_right: float = 0.5,
    content_evaluation_wrong: float = 0.5,
):
    """Function returns the information accuracy when the agent evaluates the source
    and the content.
    The idea is to calculate the probability that the agent accepts an argument that
    survived the source evaluation,
    the probability that an accepted argument is right and the probability that an
    accepted argument is wrong.
    NOTE: The companion's accuracy (without content evaluation) is given by setting
    content evaluation to 0.5.
    Parameters
    ----------
    competence_associate: float
        Competence level of associates, i.e., agents with aligned interests
    competence_opposer: float
        Competence level of opposers, i.e., agents with opposed interests
    source_evaluative_capacity: float
        Level of source evaluative capacity
    content_evaluation_right: float = 0.5
        Level of content evaluative capacity for right content, i.e., content that
        supports the alternative that is in
        the agent's best interest
    content_evaluation_wrong: float = 0.5
        Level of content evaluative capacity for wrong content, i.e., content that does
        not support the alternative
        that is in the agent's best interest
    Returns
    -------
    information_accuracy: float
        The probability that an accepted piece of information supports the right
        alternative, i.e., the alternative is
        in the agent's best interest"""

    # 1. Calculate the probability that a piece of information from an accepted source
    # supports the right alternative
    # and survives both source and content evaluation:
    # (The probability that the source is an associate who produced a right argument
    # plus
    # the probability that the source is an opposer who produced a right argument) times
    # the probability that a right argument is correctly identified (and thus accepted)
    probability_right = (
        source_evaluative_capacity * competence_associate
        + (1 - source_evaluative_capacity) * (1 - competence_opposer)
    ) * content_evaluation_right

    # 2. idem for the wrong alternative
    probability_wrong = (
        source_evaluative_capacity * (1 - competence_associate)
        + (1 - source_evaluative_capacity) * competence_opposer
    ) * (1 - content_evaluation_wrong)

    # 3. Calculate information accuracy
    probability_accept = probability_right + probability_wrong
    information_accuracy = probability_right / probability_accept
    return information_accuracy


def expected_accuracy(
    degree_open_mindedness: int = 10,
    competence_opposer: float = 0.7,
    competence_associate: float = 0.6,
    source_evaluative_capacity: float = 0.5,
    content_evaluative_capacity: float = 0.5,
    probability_companion_right: float = "None",
):
    """Function returns the expected accuracy of an open-minded agent given certain
    input.
     Input can be either:
        a) a given degree of open-mindedness, the principal agent's competence and the
        companion's accuracy, or
        b) a given degree of open-mindedness, competences, and source and content
        evaluative capacity
        In other words, one can either input the companion's accuracy directly or this
        function calculates it from
        the other input
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
        supports the alternative that is in
        the agent's best interest
    probability_companion_right: float
        The probability that a companion supports the right alternative, i.e., the
        alternative that is in the
        agent's best interest
    Returns
    -------
    probability_right: float
        The probability that an open-minded agent selects the right alternative, i.e.,
        the alternative that is in
        her best interest"""

    # 0. Initialize variables
    probability_right: float = 0

    # 1. Special case of close-minded agent
    if degree_open_mindedness == 0:
        probability_right = competence_associate

    # 2. Open-minded agent
    else:
        # Calculate companion's accuracy if it has not been given as input
        if probability_companion_right == "None":
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


def find_tipping_evaluation_content(
    competence_associate: float,
    competence_opposer: float,
    source_evaluative_capacity: float,
    degree_open_mindedness: int = 4,
):
    """Function returns the tipping point for content evaluative capacity where
    open-mindedness becomes epistemically
    beneficial for an open-minded agent with specified degree of open-mindedness,
    competences and
    source evaluative capacities.
    The idea is to step-wise increase (or decrease) the content evaluative capacity
     until the point where
    open-mindedness is epistemically beneficial.
    Parameters
    ----------
    degree_open_mindedness: int
        Degree of open-mindedness
    competence_associate: float
        Competence level of associates, i.e., agents with aligned interests
    competence_opposer: float
        Competence level of opposers, i.e., agents with opposed interests
    source_evaluative_capacity: float
        Level of source evaluative capacity
    Returns
    -------
    evaluation_content: float
        Tipping for content evaluative capacity to become epistemically beneficial"""

    # 0. Initialize variables
    evaluation_content: float = 0.5
    step_size = 0.01
    probability_companion_right = accuracy_information(
        source_evaluative_capacity=source_evaluative_capacity,
        competence_associate=competence_associate,
        competence_opposer=competence_opposer,
        content_evaluation_right=evaluation_content,
        content_evaluation_wrong=evaluation_content,
    )
    probability_right = expected_accuracy(
        degree_open_mindedness=degree_open_mindedness,
        probability_companion_right=probability_companion_right,
        competence_associate=competence_associate,
    )
    # 1. If probability_right is lower than competence_associate, the idea is to
    # step-wise increase the content
    # evaluative capacity until the point where open-mindedness is epistemically
    # beneficial
    if probability_right < competence_associate:
        while probability_right < competence_associate:
            evaluation_content = evaluation_content + step_size
            probability_companion_right = accuracy_information(
                source_evaluative_capacity=source_evaluative_capacity,
                competence_associate=competence_associate,
                competence_opposer=competence_opposer,
                content_evaluation_right=evaluation_content,
                content_evaluation_wrong=evaluation_content,
            )
            probability_right = expected_accuracy(
                degree_open_mindedness=degree_open_mindedness,
                probability_companion_right=probability_companion_right,
                competence_associate=competence_associate,
            )
    # 2. If probability_right is higher than competence_associate, the idea is to
    # step-wise decrease the content
    # evaluative capacity until the point where open-mindedness is no longer
    # epistemically beneficial
    else:
        while probability_right > competence_associate:
            evaluation_content = evaluation_content - step_size
            probability_companion_right = accuracy_information(
                source_evaluative_capacity=source_evaluative_capacity,
                competence_associate=competence_associate,
                competence_opposer=competence_opposer,
                content_evaluation_right=evaluation_content,
                content_evaluation_wrong=evaluation_content,
            )
            probability_right = expected_accuracy(
                degree_open_mindedness=degree_open_mindedness,
                probability_companion_right=probability_companion_right,
                competence_associate=competence_associate,
            )
        evaluation_content = evaluation_content + step_size
    return round(evaluation_content, 2)
