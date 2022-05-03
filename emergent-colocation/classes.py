class CascadeRule:
    def __init__(self, antecedent, consequent, cpi) -> None:
        self.antecedent = antecedent
        self.consequent = consequent
        self.cpi = cpi
    def __str__(self) -> str:
        return str(self.antecedent)+' => '+str(self.consequent)+', Cascade Participation Index: '+str(round(self.cpi, 4))