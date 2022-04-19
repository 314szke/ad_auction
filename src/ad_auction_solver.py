import math

from collections import defaultdict
from src.utils import ROUND


class AdAuctionSolver:
    def __init__(self, data, verbose):
        self.buyers = data.buyers
        self.items = data.items
        self.verbose = verbose

        self.eta = 0.0
        self.constant = 0.0
        self.r_max = self._get_max_bid_budget_ratio()
        self.objective_value = 0
        self._init_solver()


    def _get_max_bid_budget_ratio(self):
        r_max = -1
        for buyer in self.buyers:
            for bid in buyer.bids.values():
                ratio = ROUND(bid / buyer.budget)
                if ratio > r_max:
                    r_max = ratio
        return r_max


    def _init_solver(self):
        for idx in range(len(self.buyers)):
            self.buyers[idx].reset()
        self.assignment = [defaultdict(lambda: 0) for _ in self.buyers]


    def _get_buyer_with_max_bid_budget(self, item):
        max_product = 0
        max_id = -1
        for buyer_id in item.interested_buyers:
            value = ROUND(self.buyers[buyer_id].bids[item.id] * self.buyers[buyer_id].get_value())
            if value > max_product:
                max_product = value
                max_id = buyer_id
        return max_id


    def _calculate_objective_value(self):
        self.objective_value = 0.0
        for buyer_id, sold_items in enumerate(self.assignment):
            for item_id, fraction in sold_items.items():
                self.objective_value += self.buyers[buyer_id].bids[item_id] * fraction
        self.objective_value = ROUND(self.objective_value)


    def solve(self, eta):
        self.eta = ROUND(eta)
        self.constant = math.pow((1 + self.r_max), (self.eta / self.r_max))
        self._init_solver()

        for item in self.items:
            if item.prediction is None: continue
            buyer_id = self._get_buyer_with_max_bid_budget(item)
            if buyer_id == -1: continue

            if self.buyers[buyer_id].bids[item.id] < self.buyers[item.prediction].bids[item.id]:
                self.assignment[buyer_id][item.id] = self.eta
                self.assignment[item.prediction][item.id] = ROUND(1 - self.eta)
            else:
                self.assignment[buyer_id][item.id] = 1
            self.buyers[buyer_id].update_value(item.id, self.constant)

        self._calculate_objective_value()
        return self.objective_value


    def get_solution_robustness(self, offline_objective_value):
        return ROUND (self.objective_value / offline_objective_value)


    def print_solution(self, error, offline_objective_value):
        print('The online solution:')
        print(f'Prediction error = {error}')
        print(f'Eta = {self.eta}')
        print(f'Objective value = {self.objective_value}')
        print(f'Robustness = {self.get_solution_robustness(offline_objective_value)}')
        if self.verbose:
            self.print_assignment()
        print()


    def print_assignment(self):
        for idx, items in enumerate(self.assignment):
            print(f'Buyer [{idx}] purchased: {dict(items)}')
