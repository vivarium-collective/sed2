"""
SED2 builder

demos are according to this:
    - https://docs.google.com/document/d/1jZkaNhM_cOqMWtd4sJZ9b0VGXPTLsDKsRNI5Yvu4nOA/edit
"""
from sed2.builder import SEDBuilder
from demo_processes import process_registry  # this triggers the demo processes to register


def test_builder():
    # Example usage:
    sed = SEDBuilder()

    # Load an SBML model
    sed.add_model(
        model_id='model1',
        path='demo_processes/BIOMD0000000061_url.xml',  # TODO -- this should also move the file into an archive
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
    sed.plot(
        plot_id='stats_glc',
        plot_type='line',
        title='Statistics of Glucose Concentration',
        x_label='Time',
        y_label='Concentration',
        legend=['Mean', 'Standard Deviation']
    )

    # print to console
    sed.print()

    # save the sed2 file
    sed.save_file(filename='sed2demo')
    # sed.save_xml()
    # sed.save_json()

    # execute all the steps in the simulation experiment
    sed.execute()



if __name__ == '__main__':
    test_builder()
