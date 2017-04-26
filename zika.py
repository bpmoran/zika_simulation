''' 
READ_ME:
 1) Class input template:
 [['city_nameA', population, number_infected, infection_rate(poss re-calculated from last 'cycle'],
 ['city_nameB', population, number_infected, infection_rate(poss re-calculated from last 'cycle'],
 ['city_nameC', population, number_infected, infection_rate(poss re-calculated from last 'cycle']]
 
 2) Class currently supports:
 stringification (for printing)
 copy (for variable assignment) 
 feel free to add any overloads we need
 
 3) Counter-operator idea: 
    Regardless of how we do it, I think we need to apply an infect_population function each turn. This makes our problem dynamic
    rather than static, like the puzzles we were working on. 
    We can apply it in two ways: 
    1) Just apply infect_population every turn
    2) delineate between the causes such as 'sezual contact' and 'mosquito bites' and put those counter-operators in a list
    3) Whether we break it up or not, our infection rate can be static, or osillate between two values, giving it some 
    variability. 
     
    Functions in the counter operator list could delineate the various ways that a population can be infected and reflect the 
    probability of each occuring. 
    Possible counter-operators: 
    a) mosquito_transmission
    b) sexual_contact
    c) that's pretty much it
    
    
 4) infect_population function: the simpler version of having 'counter operators' would be just to apply a static 'infect_population' 
    function. We'll probably go with this one. I already made a prototype (see below). If we decide to go with counter operators,
    then infect_population can just apply counter operators. 
    

 
'''
import copy

class State():

    def __init__(self, data):
        self.data = data

    def __str__(self):
        # Produces a brief textual description of a state.
        list = ['City Name: ', 'Population: ', '# Infected: ', 'Infection Rate: ' ]
        txt = "*********\n"
        for j in self.data:
            for i, x in enumerate(j):
                txt += list[i] + str(x) + '\n'
            txt += '\n'
        txt += "*********"
        return txt

    # for deep copy of states
    def __copy__(self):
        news = State([])
        news.data = self.data

        return news


def infect(city):
    print('Infecting ' + city[0])
    if city[2] + (city[2] * city[3]) > city[1]: # if the number of infected would = or > number of total citizens
        return [city[0], city[1], city[1], city[3]]                     # everyone's infected
                                                                        # else
    return [city[0], city[1], round(city[2] + (city[2] * city[3])), city[3]]   # infect some of them.

' applies "infect" fucntion to each city in state class,'
def infect_population(state):
    for i, city in enumerate(state.data):
        state.data[i] = infect(city)
