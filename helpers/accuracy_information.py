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
    survived the source evaluation, the probability that an accepted argument is right
    and the probability that an accepted argument is wrong.
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
        supports the alternative that is in the agent's best interest
    content_evaluation_wrong: float = 0.5
        Level of content evaluative capacity for wrong content, i.e., content that does
        not support the alternative that is in the agent's best interest

    Returns
    -------
    information_accuracy: float
        The probability that an accepted piece of information supports the right
        alternative, i.e., the alternative is in the agent's best interest"""

    # 1. Calculate the probability that a piece of information from an accepted source
    # supports the right alternative and survives both source and content evaluation:
    # (The probability that the source is an associate who produced a right argument
    # plus the probability that the source is an opposer who produced a right argument)
    # times the probability that a right argument is correctly identified
    # (and thus accepted)
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
