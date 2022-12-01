from scipy.stats import binom


class ProbabilityCalculator:
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

        if self.probability_companion_right is None:
            self.probability_companion_right = self.accuracy_information()

    def compute_probability_right(self) -> float:
        # Special case of close-minded agent
        if self.degree_open_mindedness == 0:
            return self.competence_associate

        # Otherwise, compute the expected accuracy
        if (self.degree_open_mindedness % 2) == 0:
            return self.probability_right_even_degree()
        else:
            return self.probability_right_uneven_degree()

    def probability_right_even_degree(self):
        # I win in two events:
        # (a) exactly half of the neighbors are correct and I am correct
        p_me_correct_causing_win = self.competence_associate * binom.pmf(
            self.degree_open_mindedness / 2,
            self.degree_open_mindedness,
            self.probability_companion_right,
        )
        # (b) more than half of the neighbors are correct
        p_win_without_me = binom.sf(
            self.degree_open_mindedness / 2,
            self.degree_open_mindedness,
            self.probability_companion_right,
        )
        return p_me_correct_causing_win + p_win_without_me

    def probability_right_uneven_degree(self):
        # I win in three events:
        # (a) exactly half of the neighbors plus 1 are correct and I am correct
        p_me_causing_win = self.competence_associate * binom.pmf(
            (self.degree_open_mindedness + 1) / 2,
            self.degree_open_mindedness,
            self.probability_companion_right,
        )

        # (b) more than half of the neighbors plus 1 are correct
        p_win_without_me = binom.sf(
            (self.degree_open_mindedness + 1) / 2,
            self.degree_open_mindedness,
            self.probability_companion_right,
        )

        # (c) there's a tie and the random choice is correct
        p_tie_random_choice_correct = 0.5 * self.p_tie()

        return p_me_causing_win + p_win_without_me + p_tie_random_choice_correct

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

    def find_tipping_evaluation_content(self) -> float:
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
        probability_right = self.compute_probability_right()

        if probability_right < self.competence_associate:
            # step-wise increase the content evaluative capacity until
            # open-mindedness is epistemically beneficial
            while probability_right < self.competence_associate:
                self.source_evaluative_capacity = (
                    self.source_evaluative_capacity + step_size
                )
                self.probability_companion_right = self.accuracy_information()
                probability_right = self.compute_probability_right()
        else:
            # step-wise decrease the content evaluative capacity until
            # open-mindedness is no longer epistemically beneficial
            while probability_right > self.competence_associate:
                self.source_evaluative_capacity = (
                    self.source_evaluative_capacity - step_size
                )
                self.probability_companion_right = self.accuracy_information()
                probability_right = self.compute_probability_right()
            self.source_evaluative_capacity = (
                self.source_evaluative_capacity + step_size
            )
        return round(self.source_evaluative_capacity, 2)
