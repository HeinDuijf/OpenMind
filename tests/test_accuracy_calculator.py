import numpy as np
import pandas as pd
from accuracy_calculator import Agent


def test_closed_mind():
    default_params = {
        "degree_open_mindedness": 4,
        "competence_opposer": 0.7,
        "competence_associate": 0.6,
        "source_evaluative_capacity": 0.5,
        "content_evaluative_capacity": 0.5,
    }

    # Test accuracy of close mind
    competence_values = 0.5 + 0.05 * np.arange(0, 10, dtype=int)
    for competence_opposer in competence_values:
        params_closed_mind = default_params.copy()
        params_closed_mind["degree_open_mindedness"] = 0
        params_closed_mind["competence_opposer"] = competence_opposer
        assert (
            Agent(**params_closed_mind).accuracy_open_mind()
            == params_closed_mind["competence_associate"]
        )
    for competence_associate in competence_values:
        params_closed_mind = default_params.copy()
        params_closed_mind["degree_open_mindedness"] = 0
        params_closed_mind["competence_associate"] = competence_associate
        assert (
            Agent(**params_closed_mind).accuracy_open_mind()
            == params_closed_mind["competence_associate"]
        )


def test_benefit_open_mind():
    default_params = {
        "degree_open_mindedness": 4,
        "competence_opposer": 0.7,
        "competence_associate": 0.6,
        "source_evaluative_capacity": 0.5,
        "content_evaluative_capacity": 0.5,
    }
    # test accuracy open mind
    df = pd.read_csv("data/heatmap_source_evaluation_n2", index_col=0)
    for source_evaluative_capacity in df.columns:
        for competence in df.index:
            params = default_params.copy()
            params["degree_open_mindedness"] = 2
            params["competence_opposer"] = competence
            params["competence_associate"] = competence
            params["source_evaluative_capacity"] = float(source_evaluative_capacity)
            assert (
                round(Agent(**params).benefit_open_mind(), 2)
                == df.at[competence, source_evaluative_capacity]
            )

    df = pd.read_csv("data/heatmap_source_evaluation_n4", index_col=0)
    for source_evaluative_capacity in df.columns:
        for competence in df.index:
            Agent()
            params = default_params.copy()
            params["degree_open_mindedness"] = 4
            params["competence_opposer"] = competence
            params["competence_associate"] = competence
            params["source_evaluative_capacity"] = float(source_evaluative_capacity)
            assert (
                round(Agent(**params).benefit_open_mind(), 2)
                == df.at[competence, source_evaluative_capacity]
            )

    df = pd.read_csv("data/heatmap_content_only_n4", index_col=0, dtype=float)
    for content_evaluative_capacity in df.columns:
        for competence in df.index:
            params = default_params.copy()
            params["competence_opposer"] = competence
            params["competence_associate"] = competence
            params["source_evaluative_capacity"] = 0.5
            params["content_evaluative_capacity"] = float(content_evaluative_capacity)
            assert (
                round(Agent(**params).benefit_open_mind(), 2)
                == df.at[competence, content_evaluative_capacity]
            )
