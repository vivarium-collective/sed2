

class SED:

    def __init__(self):
        self.state = {}



def test_api():
    sed = SED()
    sed.model("urn:sedml:language:sbml", "munz2000.xml")
    sed.steady_state(selectionList=["Susceptible", "Zombie"])
    sed.report(name="SteadyStates")

    # TODO -- tellurium? copasi?

    sed.bigraph()  # returns the Python tree

    sed.run()  # this would run at this point


def test_api4():
    # Repeat simulations    any    number    of    times and    with any degree of nesting.Any changes may be applied to parameters, initial conditions etc within the repeated simulations.The results of the simulation will be collected into arrays.
    sed = SED()
    sed.model("urn:sedml:language:sbml", "munz2000.xml")


    sed.begin_loop()
    for i in range(10):
        # add ten steps, which will run in parallel
        sed.reset()
        sed.set('zombie', i)
        sed.uniform_time_course(0, 0, 5, 50, selectionList=["Susceptible", "Zombie"])  # This would add a new ste
    sed.end_loop()

    sed.report("Different    starting    Z    values")




    if __name__ == '__main__':
    test_api()
