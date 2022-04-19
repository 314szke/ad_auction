from src.utils import ROUND


class Buyer:
    def __init__(self, buyer_id, budget):
        self.id = buyer_id
        self.budget = budget
        self.allowed_budget = 0
        self.has_adjusted_budget = (budget == 0)
        self.wanted_item_ids = []
        self.bids = {}
        self.potential_expense = 0
        self.value = 0.0


    def __repr__(self):
        return f'Buyer\t[{self.id}]:\tbudget = {self.budget},\twanted_items = {self.wanted_item_ids}'


    def reset(self):
        self.value = 0


    def update_value(self, item_id, constant):
        bid_ratio = self.bids[item_id] / self.budget
        if constant == 1.0:
            sys.exit('ERROR: C cannot be 1! (caused by eta = 0)')
        constant_ratio = 1 / (constant - 1)
        self.value = ROUND(self.value * (1 + bid_ratio) + bid_ratio * constant_ratio)


    def get_value(self):
        return max(0, ROUND(1.0 - self.value))



class Item:
    def __init__(self, item_id, buyer_ids):
        self.id = item_id
        self.interested_buyers = buyer_ids
        self.prediction = None


    def __repr__(self):
        return f'Item\t[{self.id}]:\tprediction = {self.prediction},\tinterested_buyers = {self.interested_buyers}'



class ProblemInput:
    def __init__(self, configuration):
        self.config = configuration
        self.buyers = []
        self.buyer_ids = list(range(self.config.num_buyers))
        self.items = []
        self.item_ids = list(range(self.config.num_items))


    def _get_metric_string(self, name, value_list, all):
        min_value = int(min(value_list))
        max_value = int(max(value_list))
        sum_value = int(sum(value_list))
        avg_value = int(ROUND(sum_value / all))
        return f'{name}\tmin = {min_value},\tmax = {max_value},\taverage = {avg_value}\n'


    def __str__(self):
        output = self.config.__str__()
        output += '\n\nObservations of the input:\n'

        budget_list = [x.budget for x in self.buyers]
        output += self._get_metric_string('Budget:\t', budget_list, self.config.num_buyers)

        bid_list = []
        for buyer in self.buyers:
            for bid in buyer.bids.values():
                bid_list.append(bid)
        output += self._get_metric_string('Price:\t', bid_list, self.config.num_buyers)

        buyers_list = [len(x.interested_buyers) for x in self.items]
        output += self._get_metric_string('NumBuyers:', buyers_list, self.config.num_items)

        items_list = [len(x.wanted_item_ids) for x in self.buyers]
        output += self._get_metric_string('NumItems:', items_list, self.config.num_buyers)

        expense_list = [x.potential_expense for x in self.buyers]
        output += self._get_metric_string('Expenses:', expense_list, self.config.num_buyers)

        overflow = sum([x.potential_expense > x.budget for x in self.buyers])
        percentage = ROUND((overflow / self.config.num_buyers) * 100)
        output += f'{int(percentage)} % number of buyers want to spend more, than their budget.\n'
        return output
