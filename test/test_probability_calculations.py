from _old.prob_calc import accuracy_information, expected_accuracy
from probability_calculator import ProbabilityCalculator


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
    new_ia = ProbabilityCalculator(**new_params).accuracy_information()

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
    acc_new = ProbabilityCalculator(**default_params).compute_probability_right()
    assert acc_old == acc_new

    some_other_params = {
        "degree_open_mindedness": 4,
        "competence_opposer": 0.3,
        "competence_associate": 0.9,
        "source_evaluative_capacity": 0.5,
        "content_evaluative_capacity": 0.5,
        "probability_companion_right": 0.2,
    }

    acc_old = expected_accuracy(**some_other_params)
    acc_new = ProbabilityCalculator(**some_other_params).compute_probability_right()
    assert acc_old == acc_new

    different_capacities = {
        "degree_open_mindedness": 4,
        "competence_opposer": 0.3,
        "competence_associate": 0.9,
        "source_evaluative_capacity": 0.4,
        "content_evaluative_capacity": 0.9,
        "probability_companion_right": 0.2,
    }

    acc_old = expected_accuracy(**different_capacities)
    acc_new = ProbabilityCalculator(**different_capacities).compute_probability_right()
    assert acc_old == acc_new
