from dataclasses import dataclass

@dataclass
class ProblemConfiguration:
    num_buyers: int
    num_items: int

    min_budget: int
    max_budget: int

    min_bidders: int
    max_bidders: int

    min_bid: int
    max_bid: int

    random_type: dict
    random_seed: int


    def __str__(self):
        output = 'Configuration:\n'
        output +=  f'Buyers:\t\t{self.num_buyers}\nItems:\t\t{self.num_items}\n'
        output += f'Budget:\t\t[{self.min_budget}, {self.max_budget}]\n'
        output += f'NumBidders:\t[{self.min_bidders}, {self.max_bidders}]\nBids:\t[{self.min_bid}, {self.max_bid}]'
        return output



CONFIGS = {
    0: ProblemConfiguration(10, 10, 10, 100, 1, 3, 1, 10, {}, 42),
    1: ProblemConfiguration(100, 10_000, 10, 0, 6, 6, 0, 10, {'lognorm': {'mu': 0.5, 'sigma': 0.5}} , 0)
}
