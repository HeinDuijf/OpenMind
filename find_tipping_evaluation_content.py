from accuracy_calculator import Agent


def find_tipping_evaluation_content(
    degree_open_mindedness: int = 10,
    competence_opposer: float = 0.7,
    competence_associate: float = 0.6,
    source_evaluative_capacity: float = 0.5,
) -> float:
    """Function returns the tipping point for content evaluative capacity where
    open-mindedness becomes epistemically beneficial for an open-minded agent with
    specified degree of open-mindedness, competences and source evaluative
    capacities.

    The idea is to step-wise increase (or decrease) the content evaluative capacity
    until the point where open-mindedness is epistemically beneficial.

    Returns
    -------
    evaluation_content: float
        Tipping for content evaluative capacity to become epistemically beneficial
    """

    # 0. Initialize variables
    step_size = 0.01
    agent_variables: dict = {
        "degree_open_mindedness": degree_open_mindedness,
        "competence_opposer": competence_opposer,
        "competence_associate": competence_associate,
        "source_evaluative_capacity": source_evaluative_capacity,
    }

    current_agent = Agent(content_evaluative_capacity=0.5, **agent_variables)
    current_accuracy = current_agent.accuracy_open_mind()

    # 1. Search for tipping point
    if current_accuracy < current_agent.competence_associate:
        # step-wise increase the content evaluative capacity until
        # open-mindedness is epistemically beneficial
        while current_accuracy < current_agent.competence_associate:
            new_content_evaluative_capacity = (
                current_agent.content_evaluative_capacity + step_size
            )

            current_agent = Agent(
                content_evaluative_capacity=new_content_evaluative_capacity,
                **agent_variables
            )
            current_accuracy = current_agent.accuracy_open_mind()
        tipping_point = round(current_agent.content_evaluative_capacity, 2)
        return tipping_point
    else:
        # step-wise decrease the content evaluative capacity until
        # open-mindedness is no longer epistemically beneficial
        while current_accuracy > current_agent.competence_associate:
            new_content_evaluative_capacity = (
                current_agent.content_evaluative_capacity - step_size
            )

            current_agent = Agent(
                content_evaluative_capacity=new_content_evaluative_capacity,
                **agent_variables
            )
            current_accuracy = current_agent.accuracy_open_mind()
        tipping_point = round(current_agent.content_evaluative_capacity + step_size, 2)
        return tipping_point
