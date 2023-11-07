"""
SED2 builder

demos are according to this:
    - https://docs.google.com/document/d/1jZkaNhM_cOqMWtd4sJZ9b0VGXPTLsDKsRNI5Yvu4nOA/edit
"""
from sed2.builder import SEDBuilder
from demo_processes import process_registry  # this triggers the demo processes to register


MODEL_PATH = 'demo_processes/Caravagna2010.xml'


def test_builder():
    # Example usage:
    sed = SEDBuilder()

    # Load an SBML model
    sed.add_model(
        model_id='model1',
        source='demo_processes/BIOMD0000000061_url.xml',  # TODO -- this should also move the file into an archive
        language='sbml',
    )

    # Set up the simulator
    sed.add_simulator(
        simulator_id='simulator1',
        name='tellurium',
        version='',
        kisao_id='0000029',  # Gillespie direct algorithm
    )

    # make the first step
    sed.start_step(step_id='1')

    # run 100 simulations
    n_simulations = 100
    for i in range(n_simulations):
        sed.add_simulation(
            simulation_id=f'simulation_{i}',
            simulator_id='simulator1',
            model_id='model1',
            start_time=0,
            end_time=100,
            number_of_points=1000,
            observables=['mol1', 'mol2'],  # this will be stored in a dict: {step_id: {sim_id: {observable_id: [...]}}}
        )

    # make the second step
    sed.start_step(step_id='2')

    # calculate the mean and standard deviation for 'mol1' across all simulations in step 1
    sed.add_data_generator(
        data_id='stats_glc',
        observables='mol1',
        operations=['mean', 'standard_deviation']
    )

    # make the third step
    sed.start_step(step_id='3')

    # plot the mean and standard deviation of 'glc'
    sed.add_visualization(
        plot_id='stats_glc',
        plot_type='line',
        title='Statistics of Glucose Concentration',
        x_label='Time',
        y_label='Concentration',
        legend=['Mean', 'Standard Deviation']
    )

    # print to console
    sed.print_sed_doc()

    # save the sed2 file
    sed.save_sed_doc(filename='sed2demo')
    # sed.save_xml()
    # sed.save_json()

    # execute all the steps in the simulation experiment
    sed.execute()


def test1():
    """Run a simulation from time start to time end with a given number of points/steps. The run will return a 2D array of results."""

    # Initialize the SEDBuilder
    sed = SEDBuilder()

    # Load a model
    sed.add_model(
        model_id='model1',
        source='demo_processes/Caravagna2010.xml',
        language='sbml',
    )

    # Set up the simulator
    sed.add_simulator(
        simulator_id='simulator1',
        name='copasi',
        version='',
        kisao_id='',
    )

    # Begin the simulation experiment step
    sed.start_step(step_id='run_simulation')

    # Add a simulation run configuration
    sed.add_simulation(
        simulation_id='run1',
        simulator_id='simulator1',
        model_id='model1',
        start_time=0,
        end_time=100,
        number_of_points=1000,
        observables=['observable1', 'observable2'],
    )

    # Execute the simulation
    results = sed.execute()

    # Assuming the 'execute' method returns the results directly.
    # These results would be the 2D array with each row representing a time point
    # and each column representing an observable's value at that time point.

    # If you want to print or otherwise process the results, you can do so here.
    # For example, you could print the results to the console or write them to a file.
    print(results)


def test19():
    # Initialize
    sed = SEDBuilder()

    # Load an SBML model
    sed.add_model(
        model_id='model1',
        source=MODEL_PATH,
        language='sbml',
    )

    # Set up copasi with the Gillespie algorithm
    sed.add_simulator(
        simulator_id='gillespie_simulator',
        name='copasi',
        version='',
        kisao_id='0000029',  # Gillespie algorithm
    )

    # Begin the first step - running stochastic simulations
    sed.start_step(step_id='stochastic_simulations')

    # Define the number of simulations
    n_simulations = 100
    # Run the defined number of stochastic simulations
    for i in range(n_simulations):
        sed.add_simulation(
            simulation_id=f'simulation_{i}',
            simulator_id='gillespie_simulator',
            model_id='model1',
            start_time=0,
            end_time=100,
            number_of_points=1000,
            # Assuming that 'observables' are the species or parameters of interest
            observables=['species1', 'species2'],
        )

    # Begin the second step - data processing for mean and standard deviation
    sed.start_step(step_id='data_processing')

    # Add data generator for mean and standard deviation for the observables
    # We are assuming that the SEDBuilder will internally handle the retrieval of
    # simulation results and compute the required statistics
    for observable in ['species1', 'species2']:
        sed.add_data_generator(
            data_id=f'stats_{observable}',
            observables=observable,
            operations=['mean', 'standard_deviation']
        )

    # Begin the third step - plotting the results
    sed.start_step(step_id='plotting')

    # Plot the mean and standard deviation for each observable
    for observable in ['species1', 'species2']:
        sed.add_visualization(
            plot_id=f'plot_stats_{observable}',
            plot_type='line',
            title=f'Statistics of {observable} Concentration',
            x_label='Time',
            y_label='Concentration',
            legend=['Mean', 'Standard Deviation']
        )

    # Execute the simulation experiment
    sed.execute()


if __name__ == '__main__':
    # test_builder()
    # test1()
    test19()
