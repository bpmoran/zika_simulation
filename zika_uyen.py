import math

# <METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Zika Simulation"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['Uyen Tran', 'Brian Moran']
PROBLEM_CREATION_DATE = "27-APR-2017"
PROBLEM_DESC = \
    '''This formulation of the Eight Puzzle problem with heuristics uses generic
    Python 3 constructs and has been tested with Python 3.4.
    It is designed to work according to the QUIET tools interface, Version 0.2.
    '''


# </METADATA>


CATEGORIES = ['clinic', 'awareness', 'mosquito', 'safe_sex']  # and maybe 'fundraising'


# <CLASS>
class State:
    def __init__(self, data, upper_state=None):
        """
        :param data: A map of variables: population, infect, rate, fund
        """
        self.data = data

        self.depth = 0
        self.h_value = -1
        if upper_state is not None:
            self.depth = upper_state.depth + 1

    def __str__(self):
        return str(self.data)

    def __eq__(self, other):
        if not (type(self) == type(other)):
            return False
        else:
            return self.data == other.data

    def __hash__(self):
        return (str(self)).__hash__()

    def __copy__(self):
        return State(self.data.copy())

    def __lt__(self, other):
        return self.h() + self.depth < other.h() + other.depth

    def h(self):
        if self.h_value == -1:
            self.h_value = h_heuristics(self)
        return self.h_value


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


# </CLASS>


# <COMMON_CODE>
def can_spend(state, spending):
    data = state.data
    cost = 0
    if spending['clinic'] == 100:
        cost = 1000000
    if spending['awareness'] == 100:
        cost = 200000
    if spending['safe_sex'] == 100:
        cost = 500000
    if spending['mosquito'] == 100:
        cost = 100000

    # Funding every 4 state
    additional_fund = 1000000 if state.depth % 4 == 0 and state.depth != 0 else 0

    # If the fund still remains and there's still infected
    return data['fund'] + additional_fund >= cost and data['infected'] > 0


def spend(state, spending):
    data = state.data
    cost = 0
    if spending['clinic'] == 100:
        cost = 1000000
    if spending['awareness'] == 100:
        cost = 200000
    if spending['safe_sex'] == 100:
        cost = 500000
    if spending['mosquito'] == 100:
        cost = 100000

    # Funding every 4 state
    additional_fund = 1000000 if state.depth % 4 == 0 and state.depth != 0 else 0

    new_data = data.copy()
    new_state = State(new_data, state)
    new_data['fund'] += additional_fund - cost

    return new_state


def create_spending():
    """
    :return: a list of spending map. Each map should have category to cost
    that the total cost of categories must be 100.
    
    For ex: {'clinic': 100, 'awareness': 0, 'mosquito': 0, 'safe_sex': 0}
    """
    spending_list = []
    # create_spending_helper(spending_list, [], 0, len(CATEGORIES))

    for i in range(len(CATEGORIES)):
        spending = {}
        for k in range(len(CATEGORIES)):
            category = CATEGORIES[k]
            cost = 100 if i == k else 0
            spending[category] = cost
        spending_list.append(spending)

    return spending_list


def create_spending_helper(spending_list, spending, total_cost, category_number):
    """
    Helper for creating more spending cases depending on cost step. One of spending map could be:
    {'clinic': 40, 'awareness': 30, 'mosquito': 10, 'safe_sex': 20}
    
    REMOVE THIS NOTE: This function can be useful later
    """
    if category_number == 0:
        if total_cost == 100:
            spending_map = {}
            for i in range(len(CATEGORIES)):
                category = CATEGORIES[i]
                cost = spending[i]
                spending_map[category] = cost
            spending_list.append(spending_map)
    else:
        step = 100 # Change step to create more spending list
        for cost in range(100, -1, -step):
            spending.append(cost)
            create_spending_helper(spending_list, spending, total_cost + cost, category_number - 1)
            del spending[-1]


def create_operators():
    spending_list = create_spending()
    operators = []

    for spending_item in spending_list:
        name = ""
        operand = lambda state, spending=spending_item: can_spend(state, spending)
        transf = lambda state, spending=spending_item: spend(state, spending)
        operators.append(Operator(name, operand, transf))

    return operators


def goal_test(state):
    return False


def goal_message(state):
    # TODO
    return True


def h_heuristics(state):
    # TODO
    return 0


# </COMMON_CODE>

# <INITIAL_STATE>
INITIAL_STATE = State({'population': 7000000000, 'infected': 1000000, 'fund': 1000000})
CREATE_INITIAL_STATE = lambda: INITIAL_STATE
# </INITIAL_STATE>

# <OPERATORS>

OPERATORS = create_operators()
# </OPERATORS>

# <GOAL_TEST>
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>

# <GOAL_MESSAGE_FUNCTION>
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# </GOAL_MESSAGE_FUNCTION>

# <HEURISTICS>

# </HEURISTICS>
