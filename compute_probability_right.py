from scipy.stats import binom


class ComputeProbabilityRight:
    def __init__(
        self,
        degree_open_mindedness: int = 10,
        competence_opposer: float = 0.7,
        competence_associate: float = 0.6,
        source_evaluative_capacity: float = 0.5,
        content_evaluative_capacity: float = 0.5,
        probability_companion_right: float = None,
    ):
        self.degree_open_mindedness = degree_open_mindedness
        self.competence_opposer = competence_opposer
        self.competence_associate = competence_associate
        self.source_evaluative_capacity = source_evaluative_capacity
        self.content_evaluative_capacity = content_evaluative_capacity
        self.probability_companion_right = probability_companion_right

        # TODO: in the docstring we describe this thing as _expected accuracy_
        self.probability_right: float = 0
        if self.probability_companion_right is None:
            self.probability_companion_right = self.accuracy_information()

    def __call__(self) -> float:
        # Special case of close-minded agent
        if self.degree_open_mindedness == 0:
            return self.competence_associate

        # Otherwise, compute the expected accuracy
        if (self.degree_open_mindedness % 2) == 0:
            self.probability_right = self.probability_right_even_degree()
        else:
            self.probability_right = self.probability_right_uneven_degree()

        return self.probability_right

    def probability_right_even_degree(self):
        # I win in two events:
        # (a) exactly half of the neighbors are correct and I am correct or
        p_me_correct_and_half_rest = self.competence_associate * binom.pmf(
            self.degree_open_mindedness / 2,
            self.degree_open_mindedness,
            self.probability_companion_right,
        )
        # (b) more than half of the neighbors are correct
        p_more_than_half_rest_correct = binom.sf(
            self.degree_open_mindedness / 2,
            self.degree_open_mindedness,
            self.probability_companion_right,
        )
        return p_me_correct_and_half_rest + p_more_than_half_rest_correct

    def probability_right_uneven_degree(self):
        # I win in three events:
        # (a) exactly half of the neighbors plus 1 are correct and I am correct
        p_me_correct_and_half_rest = self.competence_associate * binom.pmf(
            (self.degree_open_mindedness + 1) / 2,
            self.degree_open_mindedness,
            self.probability_companion_right,
        )

        # (b) more than half of the neighbors plus 1 are correct
        p_more_than_half_rest_correct = binom.sf(
            (self.degree_open_mindedness + 1) / 2,
            self.degree_open_mindedness,
            self.probability_companion_right,
        )

        # (c) there's a tie and the random choice is correct
        p_tie_random_choice_correct = 0.5 * self.p_tie()

        return (
            p_me_correct_and_half_rest
            + p_more_than_half_rest_correct
            + p_tie_random_choice_correct
        )

    def accuracy_information(self):
        probability_right = (
            self.source_evaluative_capacity * self.competence_associate
            + (1 - self.source_evaluative_capacity) * (1 - self.competence_opposer)
        ) * self.content_evaluative_capacity

        probability_wrong = (
            self.source_evaluative_capacity * (1 - self.competence_associate)
            + (1 - self.source_evaluative_capacity) * self.competence_opposer
        ) * (1 - self.content_evaluative_capacity)

        probability_accept = probability_right + probability_wrong
        information_accuracy = probability_right / probability_accept
        return information_accuracy

    def p_tie(self):
        # A tie occurs in two events:
        # (a) exactly half of the neighbors minus 1 are correct and I am correct
        p_me_correct_causing_tie = (
            binom.pmf(
                (self.degree_open_mindedness - 1) / 2,
                self.degree_open_mindedness,
                self.probability_companion_right,
            )
            * self.competence_associate
        )

        # (b) exactly half of the neighbors plus 1 are correct and I am incorrect
        p_me_wrong_causing_tie = (1 - self.competence_associate) * binom.pmf(
            (self.degree_open_mindedness + 1) / 2,
            self.degree_open_mindedness,
            self.probability_companion_right,
        )

        return p_me_correct_causing_tie + p_me_wrong_causing_tie
