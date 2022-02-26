import argparse
import random
import logging
from io import StringIO

io_obj = StringIO()

logger = logging.getLogger()
logger.setLevel(logging.INFO)
stream = logging.StreamHandler(io_obj)

stream.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(stream)


parser = argparse.ArgumentParser()
parser.add_argument("--import_from")
parser.add_argument("--export_to")


def menu():
    storage = Flashcards()

    args = parser.parse_args()

    if args.import_from:
        storage._import(args.import_from)

    choice = None
    while choice != "exit":
        print("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
        logger.info("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
        choice = input().replace(" ", "_")
        logger.info(choice)
        try:
            eval(f"storage._{choice}()")
        except AttributeError:
            continue

    if args.export_to:
        storage._export(args.export_to)


class Card:

    def __init__(self, term, definition, mistakes=0):
        self.term = term
        self.definition = definition
        self.mistakes = mistakes

    def __repr__(self):
        return f"Card('{self.term}', '{self.definition}', {self.mistakes})"


class Flashcards(list):
    """A class used for storing items of class Card. """

    def _add(self):
        print("The card:")
        logger.info("The card:")
        term = input()
        logger.info(term)
        while True:
            if term in self.terms():
                print(f"This term already exists. Try again:")
                logger.info(f"This term already exists. Try again:")
                term = input()
                logger.info(term)
            else:
                break

        print("The definition of the card:")
        logger.info("The definition of the card:")
        definition = input()
        logger.info(definition)
        while True:
            if definition in self.definitions():
                print(f"This definition already exists. Try again:")
                logger.info(f"This definition already exists. Try again:")
                definition = input()
                logger.info(definition)
            else:
                break
        self.append(Card(term, definition))
        print(f'the pair ("{term}":"{definition}") has been added')
        logger.info(f'the pair ("{term}":"{definition}") has been added')

    def _remove(self, term=None):
        # For internal calls within the class (import)
        if term is not None:
            if term in self.terms():
                self.pop(self.terms().index(term))
                return True
            return False
        else:  # For menu() calls.
            print("Which card?")
            logger.info("Which card?")
            term = input()
            logger.info(term)
            if term in self.terms():
                self.pop(self.terms().index(term))
                print("The card has been removed.")
                logger.info("The card has been removed.")
            else:
                print(f'Can\'t remove "{term}": there is no such card.')
                logger.info(f'Can\'t remove "{term}": there is no such card.')

    def _ask(self):
        """Picks 'n' random Card out of the container and ask for 'Card.term's' corresponding 'Card.definition'.  """
        print("How many times to ask?")
        logger.info("How many times to ask?")
        n = int(input())
        logger.info(n)
        n_obj = random.choices(self, k=n)
        for item in n_obj:
            print(f'Print the definition of "{item.term}":')
            logger.info(f'Print the definition of "{item.term}":')
            answer = input()
            if answer == item.definition:
                print("Correct!")
                logger.info("Correct!")
            elif answer in self.definitions():
                right_term = [t for t, d in self.items() if answer == d][0]
                item.mistakes += 1
                print(f'Wrong. The right answer is "{item.definition}", but your definition is correct for {right_term}')
                logger.info(f'Wrong. The right answer is "{item.definition}", but your definition is correct for {right_term}')
            else:
                item.mistakes += 1
                print(f'Wrong. The right answer is "{item.definition}"')
                logger.info(f'Wrong. The right answer is "{item.definition}"')

    def _import(self, file_name=""):
        if not file_name:
            print("File name:")
            logger.info("File name:")
            file_name = input()
            logger.info(file_name)
        try:
            with open(file_name, "r") as file:
                for representation in file.readlines():
                    if not representation == "\n":
                        card = eval(representation)
                        self._remove(card.term)
                        self.append(card)
                file.seek(0)
                print(f"{len(file.readlines())} cards have been loaded.")
                logger.info(f"{len(file.readlines())} cards have been loaded.")
        except FileNotFoundError:
            print("File not found")
            logger.info("File not found")

    def _export(self, file_name=""):
        if not file_name:
            print("File name:")
            logger.info("File name:")
            file_name = input()
            logger.info(file_name)
        with open(file_name, "w") as file:
            file.writelines(repr(c) + "\n" for c in self)
            print(f"{len(self)} cards have been saved.")
            logger.info(f"{len(self)} cards have been saved.")

    def _hardest_card(self):
        try:
            mistakes = self.mistakes_list()
            highest = mistakes[0][0]
            term = []
            for tup in mistakes:
                if tup[0] == highest:
                    term.append(tup[1])
                else:
                    break

            if highest == 0:
                print("There are no cards with errors.")
                logger.info("There are no cards with errors.")

            elif len(term) == 1:
                print(f'The hardest card is "{term[0]}". You have {highest} errors answering it.')
                logger.info(f'The hardest card is "{term[0]}". You have {highest} errors answering it.')

            else:
                terms = '", '.join(term)
                print(f'The hardest cards are "{terms}". You have {highest} errors answering them.')
                logger.info(f'The hardest cards are "{terms}". You have {highest} errors answering them.')
        except IndexError:
            print("There are no cards with errors.")
            logger.info("There are no cards with errors.")

    def _reset_stats(self):
        for item in self:
            item.mistakes = 0
        print("Card statistics have been reset.")
        logger.info("Card statistics have been reset.")

    def _log(self, inout=io_obj):
        print("File name:")
        logger.info("File name:")
        file_name = input()
        logger.info(file_name)
        with open(file_name, "w") as file:
            inout.seek(0)
            for line in inout.read():
                file.write(line)
            print("The log has been saved.")
            logger.info("The log has been saved.")

    def terms(self):
        return [item.term for item in self]

    def definitions(self):
        return [item.definition for item in self]

    def items(self):
        return zip([item.term for item in self], [item.definition for item in self])

    def mistakes_list(self):
        return sorted([(item.mistakes, item.term) for item in self], reverse=True)

    def _exit(self):
        print("bye bye")
        logger.info("bye bye")


if __name__ == "__main__":
    menu()
