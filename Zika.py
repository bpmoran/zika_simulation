'''
Brian Moran, Uyen Tran
Assignment 4 - Wicked Problem - Reducing Zika Virus
'''

'''
Brian TO DO:
1) infection functions
2) h function
3) .pdf 
'''
import math

# <METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Zika Simulation"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['Uyen Tran', 'Brian Moran']
PROBLEM_CREATION_DATE = "27-APR-2017"
PROBLEM_DESC = ""

# </METADATA>


CATEGORIES = ['clinic', 'awareness', 'mosquito', 'safe_sex']  # and maybe 'fundraising'
DESCRIPTIONS = {
    'none': 'none',
    'clinic': 'clinic',
    'awareness': 'awareness',
    'mosquito': 'mosquito termination',
    'safe_sex': 'safe sex practice'
}
INITIAL_SPENDING = {category: 0 for category in CATEGORIES}
INITIAL_DATA = {'population': 1000000, 'infected': 0, 'incidence_rate': (114 / 100000), 'fund': 10000000}


# <CLASS>
class State:
    def __init__(self, data, spending, upper_state=None):
        """
        :param data: A map of variables: total_population, population_infected, incidence_rate, funds_remaining
        """
        self.data = data
        self.spending = spending;
        self.data['infected'] = self.data['population'] * self.data['incidence_rate']
        self.depth = 0
        self.op_applied = None
        self.h_value = -1
        if upper_state is not None:
            self.depth = upper_state.depth + 1

    def __str__(self):
        clone_data = {k: round(v, 2) for k, v in self.data.items()}
        category = 'none'
        for c in CATEGORIES:
            if self.spending[c] == 100:
                category = c
                break
        return 'Status: ' + str(clone_data) + '\nPrevious funding on ' + DESCRIPTIONS[category] + '\n'

    def __eq__(self, other):
        if not (type(self) == type(other)):
            return False
        else:
            return self.data == other.data

    def __hash__(self):
        return (str(self)).__hash__()

    def __copy__(self):
        return State(self.data.copy(), self.spending.copy())

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
    """
    :spending: a map of category to cost. It must includes 4 key: clinic, awareness, safe_sex, mosquito
    """
    data = state.data
    cost = 0
    if spending['clinic'] == 100:
        cost = state.data['infected'] * 10000
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


# spend does a lot of the actual work.
def spend(state, spending):
    """
    :spending: a map of category to cost. It must includes 4 key: clinic, awareness, safe_sex, mosquito
    """
    data = state.data
    cost = 0
    if spending['clinic'] == 100:
        cost = state.data['infected'] * 10000  # cost ='s the number of people infected * $5000 for treatment
    if spending['awareness'] == 100:
        cost = 200000
    if spending['safe_sex'] == 100:
        cost = 500000
    if spending['mosquito'] == 100:
        cost = 100000

    # Funding every 4 state
    additional_fund = 1000000 if state.depth % 4 == 0 and state.depth != 0 else 0

    new_data = data.copy()
    new_data['fund'] += additional_fund - cost

    ''' 
    NOTE: The base infection rate is a function of what "season" it currently is. Season 0 and 1 are Spring / Summer
    and therefore their rates are higher. This is reflective of the actual zika data obtained from the CDC and cited in 
    Our-Wicked-Problem.pdf 
    '''

    # updates the infection rate
    base_rate = INCIDENCE_RATES[(state.depth + 1) % 4]  # new_state hasn't been generated yet, so state.depth + 1
    new_data['incidence_rate'] = base_rate - (base_rate * reduction_of_rate(spending))

    # updates the number of people infected
    new_data['infected'] = round(new_data['population'] * new_data['incidence_rate'])
    new_state = State(new_data, spending, state)  # Assign parent State to new State for depth increment

    # updates op_applied

    return new_state


''' 
the create_spending function was made such that it is expandable in a manner which allows the blending of 
zika containment strategies. Currently, the function sets the strategy-blend to 100% for one strategy and 0% for the rest. 
Subsequent versions of this program would all for the allocation of funds to multiple stragegies in a quarter in order to 
produce the most effective results, balancing cost and efficacy. 
'''


def create_spending():
    """
    :return: a list of spending map. Each map should have category to cost
    that the total cost of categories must be 100.

    For ex: {'clinic': 100, 'awareness': 0, 'mosquito': 0, 'safe_sex': 0}
    """
    spending_list = []
    # create_spending_helper(spending_list, [], 0, len(CATEGORIES))

    for category in CATEGORIES:
        spending = INITIAL_SPENDING.copy()
        spending[category] = 100
        spending_list.append(spending)
    print(spending_list)
    return spending_list


def create_spending_helper(spending_list, spending, total_cost, category_number):
    """
    Helper for creating more spending cases depending on cost step. One of spending map could be:
    {'clinic': 40, 'awareness': 30, 'mosquito': 10, 'safe_sex': 20}

    REMOVE THIS NOTE: This function can be useful later.
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
        step = 100  # Change step to create more spending list
        for cost in range(100, -1, -step):
            spending.append(cost)
            create_spending_helper(spending_list, spending, total_cost + cost, category_number - 1)
            del spending[-1]


def create_operators():
    """
    :return: A list of Operator object from function can_spend, function spend, and a list of spending map
    """
    spending_list = create_spending()
    operators = []

    for i, spending_item in enumerate(spending_list):
        name = str(
            spending_item)  # the name of the OPERATOR reflects the blend of strategies implemented. See def create_spending for details
        operand = lambda state, spending=spending_item: can_spend(state, spending)
        transf = lambda state, spending=spending_item: spend(state, spending)
        operators.append(Operator(name, operand, transf))

    return operators


'iteration_count is a var that is used to terminate the DFS at a certain depth level. '
iteration_count = 0


def goal_test(state):
    global iteration_count
    if iteration_count < 20:
        iteration_count += 1
        return False
    return True

def goal_message(state):
    return "We can reduce the outbreak this way: "


''' 
This function returns a positive integer inverse to how proper a given operator 
'''


def h_heuristics(state):
    return state.data['infected']


# Incidence rates related code
INCIDENCE_RATES = [(114 / 100000), (70 / 100000), (40 / 100000),
                   (20 / 100000)]  # incidence rates reflective of Brazil values 2016


# THE FOLLOWING CODE CALCULATES THE INCIDENCE RATE REDUCTION OF SOME GIVEN STRATGY PASSED BY THE VARIABLE 'SPENDING'
def reduction_of_rate(SPENDING):  # bookmark@
    ' each of the following variables is the relative amount of money (and therefore effort) being put towards the eponymous campaign'
    a, b, c, d = SPENDING['clinic'], SPENDING['awareness'], SPENDING['safe_sex'], SPENDING['mosquito']
    ''' the numbers for the reduction rates were derived in the following way:
    1) a - clinical visits are a way of isolating sick patients from others, thereby limiting the possibility of transmission through
    sexual contact or mosquito to human to mosquito transmission, however it's estimated that only 20% of people infected with zika 
     show symptoms and surely only a fraction of those end up at the clinic. It reduces the infection rate by up to 15% 
     
     2) b - awareness campaigns are possibly the most effective way to manage zika outbreaks in lieu of a vacccine. These are estimated 
     to reduce transmission rates by up to 30%
     
     3) c - safe_sex represents the funding of a "safe-sex" campaign to reduce the sexual transmission. Since a markedly small number
     of cases are transmitted this way, it is at most 5% effective
     
     4)  Spraying for mosquitos is kind of a scorched earth method of getting rid of the disease, and reportedly not all that effective
     for this reason it is given a maximum reduction rate of 8%
     
     - dividing the numbers gained from SPENDING['key] by 100 will give us the percent of the budget spent on that particular strategy
     that is then multiplied by the estimated efficacy of the given strategy and added to outcome of the others. 
     
    '''
    return (a / 100) * .15 + (b / 100) * .3 + (c / 100) * .05 + (d / 100) * .08


# </COMMON_CODE>

# <INITIAL_STATE>
INITIAL_STATE = State(INITIAL_DATA, INITIAL_SPENDING)
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
HEURISTICS = {'h_heuristics': h_heuristics}
# </HEURISTICS>
