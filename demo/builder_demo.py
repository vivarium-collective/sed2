"""
SED2 builder

demos are according to this:
    - https://docs.google.com/document/d/1jZkaNhM_cOqMWtd4sJZ9b0VGXPTLsDKsRNI5Yvu4nOA/edit
"""
from sed2.sedbuilder import SEDBuilder
from demo_processes import process_registry  # this triggers the demo processes to register


MODEL_PATH = 'demo_processes/Caravagna2010.xml'


def test_builder():
    # Example usage:
    sed = SEDBuilder()

    # Load an SBML model
    sed.add_model(
        name='model1',
        type='sbml',
        source='demo_processes/BIOMD0000000061_url.xml',  # TODO -- this should move the file into an archive
    )

    # Set up the simulator
    sed.add_simulator(
        name='simulator1',
        simulator='tellurium',
        version='',
        kisao_id='0000029',  # Gillespie direct algorithm
    )

    # make the first step
    sed.add_task(task_id='1')

    # add a simulation
    sed['1'].add_simulation(
        simulation_id='sim1',
        simulator_id='simulator1',
        model_id='model1',
    )





if __name__ == '__main__':
    test_builder()
