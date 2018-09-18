# !/usr/bin/python3
# coding: utf-8


""" Deal with user on standard output/input """

from hal.strings.utils import get_max_similar


class UserInput(object):
    """ Chat with user and ask questions """

    YES = ["yes", "ok", "fine"]
    NO = ["no", "not ok", "none"]
    THRESHOLD_INPUT = 0.9

    def __init__(self, yes_choices=YES, no_choices=NO,
                 threshold=THRESHOLD_INPUT, interactive=True):
        """
        :param threshold: float [0, 1]
            Match user answer with the one provided with at least this rate
        :param yes_choices: [] of str
            List of answer considered a "yes"
        :param no_choices: [] of str
            List of answer considered a "no"
        :param interactive: bool
            True iff program should deal with user not answering properly
        """

        object.__init__(self)

        self.THRESHOLD_INPUT = threshold
        self.YES = yes_choices
        self.NO = no_choices
        self.last_question = None
        self.interactive = bool(interactive)

    def is_yes(self, answer):
        """
        :param answer: str
            User answer
        :return: bool
            True iff considered a "yes" answer
        """

        yes_sim, _ = get_max_similar(answer, self.YES)
        no_sim, _ = get_max_similar(answer, self.NO)
        return yes_sim > no_sim and yes_sim > self.THRESHOLD_INPUT

    def is_no(self, answer):
        """
        :param answer: str
            User answer
        :return: bool
            True iff considered a "yes" answer
        """

        yes_sim, _ = get_max_similar(answer, self.YES)
        no_sim, _ = get_max_similar(answer, self.NO)
        return no_sim > yes_sim and no_sim > self.THRESHOLD_INPUT

    def show_help(self):
        """
        :return: void
            Prints to stdout help on how to answer properly
        """

        print("Sorry, not well understood.")
        print("- use", str(self.YES), "to answer 'YES'")
        print("- use", str(self.NO), "to answer 'NO'")

    def re_ask(self, with_help=True):
        """
        :param with_help: bool
            True iff you want to show help on how to answer questions
        :return: void
            Re-asks user the last question
        """

        if with_help:
            self.show_help()

        return self.get_answer(self.last_question)

    def get_answer(self, question):
        """
        :param question: str
            Question to ask user
        :return: str
            User answer
        """

        self.last_question = str(question).strip()
        user_answer = input(self.last_question)
        return user_answer.strip()

    def get_yes_no(self, question):
        """
        :param question: str
            Question to ask user
        :return: bool
            User answer
        """

        user_answer = self.get_answer(question).lower()
        if user_answer in self.YES:
            return True

        if user_answer in self.NO:
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
        else:
            return False

    def get_number(self, question,
                   min_i=float("-inf"), max_i=float("inf"), just_these=None):
        """
        :param question: str
            Question to ask
        :param min_i: float
            Min acceptable number
        :param max_i: float
            Max acceptable number
        :param just_these: [] of float
            Accept only these numbers
        :return: float
            User answer
        """

        try:
            user_answer = self.get_answer(question)
            user_answer = float(user_answer)

            if min_i < user_answer < max_i:
                if just_these:
                    if user_answer in just_these:
                        return user_answer
                    else:
                        exc = "Number cannot be accepted. Just these: "
                        exc += str(just_these)
                        raise Exception(exc)
                else:
                    return user_answer
            else:
                exc = "Number is not within limits. "
                exc += "Min is " + str(min_i) + ". Max is " + str(max_i) + ""
                raise Exception(exc)
        except Exception as e:
            print(str(e))
            self.get_number(
                self.last_question,
                min_i=min_i,
                max_i=max_i,
                just_these=just_these
            )

    def get_list(self, question,
                 splitter=",", at_least=0, at_most=float("inf")):
        """
        :param question: str
            Question to ask user
        :param splitter: str
            Split list elements with this char/str
        :param at_least: int
            List must have at least this amount of elements
        :param at_most: int
            List must have at most this amount of elements
        :return: []
            User answer
        """

        try:
            user_answer = self.get_answer(question)  # ask question
            user_answer = user_answer.split(splitter)  # split items
            user_answer = [str(item).strip() for item in user_answer]  # strip

            if at_least < len(user_answer) < at_most:
                return user_answer
            else:
                exc = "List is not correct. "
                exc += "There must be at least " + str(at_least) + " items, "
                exc += "and at most " + str(at_most) + ". "
                exc += "Use '" + str(splitter) + "' to separate items"
                raise Exception(exc)
        except Exception as e:
            print(str(e))
            self.get_list(
                self.last_question,
                at_least=at_least,
                at_most=at_most
            )
