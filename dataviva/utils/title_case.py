import re

# List of words to always make lowercase when in the middle of a phrase.
smalls = ['A', 'An', 'And', 'As', 'At', 'But', 'By', 'For', 'From', 'If', \
          'In', 'Into', 'Near', 'Nor', 'Of', 'On', 'Onto', 'Or', 'That', \
          'The', 'To', 'With', 'Via', 'Vs', 'Vs.', \
          'Um', 'Uma', 'E', 'Como', 'Em', 'No', 'Nos', 'Na', 'Nas', 'Mas', 'Por', \
          'Para', 'Pelo', 'Pela', 'De', 'Do', 'Dos', 'Da', 'Das', 'Se', 'Perto', 'Nem', \
          'Os', 'Ou', 'Que', 'O', 'A', 'Com']

# List of words that always have specific casing, regardless of position in phrase.
exceptions = ["CEOs", "CFOs", "CNC", "COOs", "HVAC", "ID", "IT", "P&D", "R&D", "TI", "TV", "UI"]
excepLower = [s.lower() for s in exceptions]

''' Titlecase Function '''
def title_case(string):

    words = re.split('(\s|-|\/|\()', string)

    def detect_string(s, i):
        if s in exceptions or s.lower() in excepLower:
            index = exceptions.index(s) if s in exceptions else excepLower.index(s.lower())
            return exceptions[index]
        if i != 0 and (s in smalls or s.capitalize() in smalls):
            return s.lower()
        else:
            return s.capitalize()

    for i, word in enumerate(words):
        words[i] = detect_string(word, i)

    return "".join(words)
