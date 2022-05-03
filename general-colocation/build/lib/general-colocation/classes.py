class Rule:
    def __init__(self, antecedent, consequent, prevalence, probability) -> None:
        self.antecedent = antecedent
        self.consequent = consequent
        self.items = list(antecedent + (consequent,))
        self.items.sort()
        self.items = tuple(self.items)
        self.p = prevalence
        self.cp = probability
    def __str__(self) -> str:
        return '{'+', '.join(self.antecedent)+'} => '+str(self.consequent)+' ('+str(round(self.p, 4))+', '+str(round(self.cp, 4))+')'

class Colocation:
    def __init__(self, items, t, prevalence) -> None:
        self.items = items
        self.table_instance = t
        self.prevalence = prevalence
        self.size = len(t)
    def __str__(self) -> str:
        return ', '.join(self.items)+': '+str(self.size)+' items, p='+str(self.prevalence)