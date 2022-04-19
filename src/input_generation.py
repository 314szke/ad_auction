import random

from src.utils import ROUND
from src.input import Buyer, Item, ProblemInput

class InputGenerator:
    def __init__(self, configuration):
        self.config = configuration
        self.data = ProblemInput(configuration)


    def _get_budget(self):
        if self.config.max_budget == 0:
            return 0
        return random.randint(self.config.min_budget, self.config.max_budget)


    def _get_bid(self):
        if 'lognorm' in self.config.random_type:
            mu = self.config.random_type['lognorm']['mu']
            sigma = self.config.random_type['lognorm']['sigma']
            bid = -1
            while not (self.config.min_bid < bid <= self.config.max_bid):
                bid = ROUND(random.lognormvariate(mu, sigma))
            return bid
        else:
            ratio = random.random()
            bid = ROUND(self.config.max_bid * ratio)
            bid = max(bid, self.config.min_bid)
            return bid


    def _get_buyer_ids(self):
        num_buyers = random.randint(self.config.min_bidders, self.config.max_bidders)
        return random.sample(self.data.buyer_ids, num_buyers)


    def generate(self):
        random.seed(self.config.random_seed)

        for idx in self.data.buyer_ids:
            self.data.buyers.append(Buyer(idx, self._get_budget()))

        for idx in range(self.config.num_items):
            buyer_ids = self._get_buyer_ids()
            self.data.items.append(Item(idx, buyer_ids))
            for buyer_id in buyer_ids:
                bid = self._get_bid()
                self.data.buyers[buyer_id].wanted_item_ids.append(idx)
                self.data.buyers[buyer_id].bids[idx] = bid
                self.data.buyers[buyer_id].potential_expense = ROUND(self.data.buyers[buyer_id].potential_expense + bid)

        for idx in self.data.buyer_ids:
            if self.data.buyers[idx].has_adjusted_budget:
                self.data.buyers[idx].budget = ROUND(self.data.buyers[idx].potential_expense / self.config.min_budget)
            if self.data.buyers[idx].budget < self.config.min_budget:
                self.data.buyers[idx].budget = self.config.min_budget

            if len(self.data.buyers[idx].bids.values()) > 0:
                max_bid = max(self.data.buyers[idx].bids.values())
            else:
                max_bid = 0
            self.data.buyers[idx].allowed_budget = self.data.buyers[idx].budget + max_bid

        return self.data
