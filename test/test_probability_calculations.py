from _old.prob_calc import accuracy_information, expected_accuracy
from accuracy_calculator import Agent


def test_accuracy_information():
    base_params = {
        "source_evaluative_capacity": 0.8,
        "competence_associate": 0.3,
        "competence_opposer": 0.4,
    }
    content_evaluative_capacity = 0.5

    old_function_params = base_params.copy()
    # The old function was always called with these two arguments identical to eachother
    old_function_params["content_evaluation_wrong"] = content_evaluative_capacity
    old_function_params["content_evaluation_right"] = content_evaluative_capacity
    old_ia = accuracy_information(**old_function_params)

    new_params = base_params.copy()
    new_params["content_evaluative_capacity"] = content_evaluative_capacity
    new_ia = Agent(**new_params).accuracy_information()

    assert old_ia == new_ia


def test_compute_probability_right():

    default_params = {
        "degree_open_mindedness": 10,
        "competence_opposer": 0.7,
        "competence_associate": 0.6,
        "source_evaluative_capacity": 0.5,
        "content_evaluative_capacity": 0.5,
    }

    acc_old = expected_accuracy(**default_params)
    acc_new = Agent(**default_params).accuracy_open_mind()
    assert acc_old == acc_new

    some_other_params = {
        "degree_open_mindedness": 4,
        "competence_opposer": 0.3,
        "competence_associate": 0.9,
        "source_evaluative_capacity": 0.5,
        "content_evaluative_capacity": 0.5,
        "companion_accuracy": 0.2,
    }

    acc_old = expected_accuracy(**some_other_params)
    acc_new = Agent(**some_other_params).accuracy_open_mind()
    assert acc_old == acc_new

    different_capacities = {
        "degree_open_mindedness": 4,
        "competence_opposer": 0.3,
        "competence_associate": 0.9,
        "source_evaluative_capacity": 0.4,
        "content_evaluative_capacity": 0.9,
        "companion_accuracy": 0.2,
    }

    acc_old = expected_accuracy(**different_capacities)
    acc_new = Agent(**different_capacities).accuracy_open_mind()
    assert acc_old == acc_new
