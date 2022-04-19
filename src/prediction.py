import random

def include_prediction(data, error_rate, optimal_solution):
    random.seed(data.config.random_seed)

    for item_id in data.item_ids:
        data.items[item_id].prediction = None

    number_of_predicted_items = 0
    number_of_modifications = 0
    spent = [0 for _ in data.buyer_ids]
    for buyer_id, assigned_items in enumerate(optimal_solution):
        for item_id, fraction in assigned_items.items():
            if fraction == 1.0:
                number_of_predicted_items += 1
                # Impose error in the prediction but keep it feasible
                if random.random() < error_rate:
                    if len(data.items[item_id].interested_buyers) == 1:
                        if (spent[buyer_id] + data.buyers[buyer_id].bids[item_id]) <= data.buyers[buyer_id].allowed_budget:
                            data.items[item_id].prediction = buyer_id
                            spent[buyer_id] += data.buyers[buyer_id].bids[item_id]
                        else:
                            number_of_modifications += 1
                    else:
                        remaining_buyers = []
                        for idx in set(data.items[item_id].interested_buyers).difference(set([buyer_id])):
                            if (spent[idx] + data.buyers[idx].bids[item_id]) <= data.buyers[idx].allowed_budget:
                                remaining_buyers.append(idx)

                        if remaining_buyers != []:
                            new_buyer_id = random.sample(remaining_buyers, 1)[0]
                            data.items[item_id].prediction = new_buyer_id
                            spent[new_buyer_id] += data.buyers[new_buyer_id].bids[item_id]

                        number_of_modifications += 1

                else: # The prediction is the optimal solution
                    if (spent[buyer_id] + data.buyers[buyer_id].bids[item_id]) <= data.buyers[buyer_id].allowed_budget:
                        data.items[item_id].prediction = buyer_id
                        spent[buyer_id] += data.buyers[buyer_id].bids[item_id]
                    else:
                        number_of_modifications += 1

    return round((number_of_modifications / number_of_predicted_items), 2)
