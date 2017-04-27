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
            return self.data == other.tiles

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
def can_spend(state):
    # TODO

    # If the fund still remains

    # If there's remain infected

    return True


def spend(state):
    """
    
    """

    return State({})


def create_spending():
    """
    :return: a list of spending map. Each map should have category to cost
    that the total cost of categories must be 100.
    
    For ex: {'clinic': 100, 'awareness': 0, 'mosquito': 0, 'safe_sex': 0}
    """
    spending_list = []
    # create_spending_helper(spending_list, [], 0, len(CATEGORIES))

    for i in range(len(CATEGORIES)):
        spending_map = {}
        for k in range(len(CATEGORIES)):
            category = CATEGORIES[k]
            cost = 100 if i == k else 0
            spending_map[category] = cost
        spending_list.append(spending_map)

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
    # TODO
    return operators


def goal_test(state):
    # TODO
    return True


def goal_message(state):
    # TODO
    return True


def h_heuristics(state):
    # TODO
    return 0


# </COMMON_CODE>

# <INITIAL_STATE>
INITIAL_STATE = State({'population': 7000000000, 'infected': 1000000, 'fund': 1000000})
CREATE_INITIAL_STATE = lambda data: State(data) if data is not None else INITIAL_STATE
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
