# -*- coding: utf-8 -*-

"""Deal with user on standard output/input """

from hal.strings.utils import get_max_similar


class UserInput:
    """Chat with user and ask questions"""

    YES_INPUT = ["yes", "ok", "fine"]
    NO_INPUT = ["no", "not ok", "none"]
    THRESHOLD_INPUT = 0.9

    def __init__(self, yes_choices=None, no_choices=None, threshold=None,
                 interactive=True):
        """
        :param threshold: Match user answer with the one provided with at least
            this rate
        :param yes_choices: List of answer considered a "yes"
        :param no_choices: List of answer considered a "no"
        :param interactive: True iff program should deal with user not answering
            properly
        """

        if not yes_choices:
            yes_choices = self.YES_INPUT

        if not no_choices:
            no_choices = self.NO_INPUT

        if not threshold:
            threshold = self.THRESHOLD_INPUT

        self.threshold = threshold
        self.yes_input = yes_choices
        self.no_input = no_choices
        self.last_question = None
        self.interactive = bool(interactive)

    def is_yes(self, answer):
        """

        :param answer: User: answer
        :return: True iff considered a "yes" answer
        """
        yes_sim, _ = get_max_similar(answer, self.yes_input)
        no_sim, _ = get_max_similar(answer, self.no_input)
        return yes_sim > no_sim and yes_sim > self.threshold

    def is_no(self, answer):
        """Checks if considered a "yes" answer

        :param answer: User answer
        :return: True iff considered a "yes" answer
        """
        yes_sim, _ = get_max_similar(answer, self.yes_input)
        no_sim, _ = get_max_similar(answer, self.no_input)
        return no_sim > yes_sim and no_sim > self.threshold

    def show_help(self):
        """Prints to stdout help on how to answer properly"""
        print("Sorry, not well understood.")
        print("- use", str(self.yes_input), "to answer 'YES'")
        print("- use", str(self.no_input), "to answer 'NO'")

    def re_ask(self, with_help=True):
        """Re-asks user the last question

        :param with_help: True iff you want to show help on how to answer
            questions
        :return: user answer
        """
        if with_help:
            self.show_help()

        return self.get_answer(self.last_question)

    def get_answer(self, question):
        """Asks user a question, then gets user answer

        :param question: Question: to ask user
        :return: User answer
        """
        self.last_question = str(question).strip()
        user_answer = input(self.last_question)
        return user_answer.strip()

    def get_yes_no(self, question):
        """Checks if question is yes (True) or no (False)

        :param question: Question to ask user
        :return: User answer
        """
        user_answer = self.get_answer(question).lower()
        if user_answer in self.yes_input:
            return True

        if user_answer in self.no_input:
            return False

        is_yes = self.is_yes(user_answer)  # check if similar to yes/no choices
        is_no = self.is_no(user_answer)
        if is_yes and not is_no:
            return True

        if is_no and not is_yes:
            return False

        if self.interactive:
            self.show_help()
            return self.get_yes_no(self.last_question)

        return False

    def get_number(self, question, min_i=float("-inf"), max_i=float("inf"),
                   just_these=None):
        """Parses answer and gets number

        :param question: Question: to ask user
        :param min_i: min acceptable number
        :param max_i: max acceptable number
        :param just_these: Accept only these numbers
        :return: User answer
        """
        try:
            user_answer = self.get_answer(question)
            user_answer = float(user_answer)

            if min_i < user_answer < max_i:
                if just_these:
                    if user_answer in just_these:
                        return user_answer

                    exc = "Number cannot be accepted. Just these: "
                    exc += str(just_these)
                    raise Exception(exc)

                return user_answer

            exc = "Number is not within limits. "
            exc += "Min is " + str(min_i) + ". Max is " + str(max_i) + ""
            raise Exception(exc)
        except Exception as exc:
            print(str(exc))
            return self.get_number(
                self.last_question,
                min_i=min_i,
                max_i=max_i,
                just_these=just_these
            )

    def get_list(self, question,
                 splitter=",", at_least=0, at_most=float("inf")):
        """Parses answer and gets list

        :param question: Question: to ask user
        :param splitter: Split list elements with this char
        :param at_least: List must have at least this amount of elements
        :param at_most: List must have at most this amount of elements
        :return: User answer
        """
        try:
            user_answer = self.get_answer(question)  # ask question
            user_answer = user_answer.split(splitter)  # split items
            user_answer = [str(item).strip() for item in user_answer]  # strip

            if at_least < len(user_answer) < at_most:
                return user_answer

            exc = "List is not correct. "
            exc += "There must be at least " + str(at_least) + " items, "
            exc += "and at most " + str(at_most) + ". "
            exc += "Use '" + str(splitter) + "' to separate items"
            raise Exception(exc)
        except Exception as exc:
            print(str(exc))
            return self.get_list(
                self.last_question,
                at_least=at_least,
                at_most=at_most
            )
