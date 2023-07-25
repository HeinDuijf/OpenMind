from scipy.stats import binom


class Agent:
    def __init__(
        self,
        degree_open_mindedness: int = 10,
        competence_unreliable_group: float = 0.7,
        competence_reliable_group: float = 0.6,
        source_evaluative_capacity: float = 0.5,
        content_evaluative_capacity: float = 0.5,
        trustee_accuracy: float = None,
    ):
        self.degree_open_mindedness = degree_open_mindedness
        self.competence_unreliable_group = competence_unreliable_group
        self.competence_reliable_group = competence_reliable_group
        self.source_evaluative_capacity = source_evaluative_capacity
        self.content_evaluative_capacity = content_evaluative_capacity
        self.accuracy_close_mind = self.competence_reliable_group
        self.trustee_accuracy = trustee_accuracy

        if self.trustee_accuracy is None:
            self.trustee_accuracy = (
                self.source_evaluative_capacity * self.competence_reliable_group
            ) + (1 - self.source_evaluative_capacity) * (
                1 - self.competence_unreliable_group
            )

    def benefit_open_mind(self) -> float:
        return self.accuracy_open_mind() - self.accuracy_close_mind

    def accuracy_open_mind(self) -> float:
        # Special case of close-minded agent
        if self.degree_open_mindedness == 0:
            return self.competence_reliable_group

        # Otherwise, compute the expected accuracy
        if (self.degree_open_mindedness % 2) == 0:
            return self.probability_right_even_degree()
        else:
            return self.probability_right_uneven_degree()

    def probability_right_even_degree(self) -> float:
        # I win in two events:
        # (a) exactly half of the neighbors are correct and I am correct
        p_me_correct_causing_win = self.competence_reliable_group * binom.pmf(
            self.degree_open_mindedness / 2,
            self.degree_open_mindedness,
            self.accuracy_information(),
        )
        # (b) more than half of the neighbors are correct
        p_win_without_me = binom.sf(
            self.degree_open_mindedness / 2,
            self.degree_open_mindedness,
            self.accuracy_information(),
        )
        return p_me_correct_causing_win + p_win_without_me

    def probability_right_uneven_degree(self) -> float:
        # I win in three events:
        # (a) exactly half of the neighbors plus 1 are correct and I am correct
        p_me_causing_win = self.competence_reliable_group * binom.pmf(
            (self.degree_open_mindedness + 1) / 2,
            self.degree_open_mindedness,
            self.accuracy_information(),
        )

        # (b) more than half of the neighbors plus 1 are correct
        p_win_without_me = binom.sf(
            (self.degree_open_mindedness + 1) / 2,
            self.degree_open_mindedness,
            self.accuracy_information(),
        )

        # (c) there's a tie and the random choice is correct
        p_tie_random_choice_correct = 0.5 * self.p_tie()

        return p_me_causing_win + p_win_without_me + p_tie_random_choice_correct

    def p_tie(self) -> float:
        # A tie occurs in two events:
        # (a) exactly half of the neighbors minus 1 are correct and I am correct
        p_me_correct_causing_tie = (
            binom.pmf(
                (self.degree_open_mindedness - 1) / 2,
                self.degree_open_mindedness,
                self.accuracy_information(),
            )
            * self.competence_reliable_group
        )

        # (b) exactly half of the neighbors plus 1 are correct and I am incorrect
        p_me_wrong_causing_tie = (1 - self.competence_reliable_group) * binom.pmf(
            (self.degree_open_mindedness + 1) / 2,
            self.degree_open_mindedness,
            self.accuracy_information(),
        )

        return p_me_correct_causing_tie + p_me_wrong_causing_tie

    def accuracy_information(self) -> float:
        probability_right_and_accept = (
            self.trustee_accuracy
        ) * self.content_evaluative_capacity

        probability_wrong_and_accept = (1 - self.trustee_accuracy) * (
            1 - self.content_evaluative_capacity
        )
        probability_accept = probability_right_and_accept + probability_wrong_and_accept
        information_accuracy = probability_right_and_accept / probability_accept
        return information_accuracy
