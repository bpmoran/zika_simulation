import zika as z # probably the only time anyone will ever explicitly import zika on purpose.
import copy
def test():

    # assigning a state
    a = z.State([['Jamestown',100,10, 0.66],['Coventry',1000,200, 0.30]])

    # copy example (deep copy) 
    b = z.State([])
    b = a

    # print example
    print(b)

    # infect_population example
    z.infect_population(a)

    print(a)


    return 0


if __name__ == '__main__':
    test()