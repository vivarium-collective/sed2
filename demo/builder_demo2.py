"""
SED2 builder
"""
import os
import json
import uuid
from process_bigraph import Composite
from sed2.builder import Builder
from sed2 import pf


class SEDBuilder(Builder):
    def __init__(self, tree_dict=None):
        # Initialize with the specific schema keys for SED
        super().__init__(
            schema_keys=['annotations', ],
            tree_dict=tree_dict)

        self.models = {}
        self.simulators = {}
        self.current_step_id = None
        self.previous_step_id = None

    def start_step(self, step_id=None):
        self.previous_step_id = self.current_step_id
        self.current_step_id = step_id or str(uuid.uuid1())
        self.bigraph[self.current_step_id] = {}

    def check_init_step(self):
        if not self.current_step_id:
            self.start_step()

    def add_model(self, model_id, path, language):
        # Ensure the model ID is unique
        assert model_id not in self.models, f"Model '{model_id}' already exists."
        # Add a model to the 'models' dictionary
        self.models[model_id] = {
            'path': path,
            'language': f'urn:sedml:language:{language}'
        }

    def add_simulator(self, simulator_id, name, version, kisao_id):
        # Ensure the simulator ID is unique
        assert simulator_id not in self.simulators, f"Simulator '{simulator_id}' already exists."
        # Add a simulator to the 'simulators' dictionary
        self.simulators[simulator_id] = {
            'name': name,
            'version': version,
            'kisao_id': f'KISAO:{kisao_id}'
        }

    def add_simulation(
            self,
            simulation_id,
            simulator_id,
            model_id,
            start_time,
            end_time,
            number_of_points,
            observables,
    ):
        self.check_init_step()

        # get the model
        model = self.models[model_id]

        # TODO -- kisao ID should set the config shape and ports
        kisao_id = self.simulators[simulator_id]['kisao_id']

        # build up the bigraph
        self.bigraph[self.current_step_id][simulation_id] = {
            '_type': 'step',
            'address': f'local:{simulator_id}',  # TODO -- make protocol configurable
            'config': {  # TODO -- this has to be the standardized config of a given simulator instance
                'model': model,
                'kisao_id': kisao_id,
                'start_time': start_time,
                'end_time': end_time,
                'number_of_points': number_of_points,
                'observables': observables,
            },
            '_depends_on': self.previous_step_id
        }

    def add_data_generator(
            self,
            data_id,
            observables,
            operations,
    ):
        self.check_init_step()

        # build up the bigraph
        self.bigraph[self.current_step_id][data_id] = {
            '_type': 'step',
            'address': f'local:{data_id}',
            'config': {
                'observables': observables,
                'operations': operations,
            },
            '_depends_on': self.previous_step_id
        }

    def plot(
            self,
            plot_id,
            plot_type,
            title,
            x_label,
            y_label,
            legend,
    ):
        self.check_init_step()

        # build up the bigraph
        self.bigraph[self.current_step_id][plot_id] = {
            '_type': 'step',
            'address': f'local:{plot_id}',
            'config': {
                'plot_type': plot_type,
                'title': title,
                'x_label': x_label,
                'y_label': y_label,
                'legend': legend,
            },
        }

    def print(self):
        print(pf(self.bigraph))

    def save_file(self, filename=None, out_dir='out'):
        composite_dict = self.bigraph
        file_path = os.path.join(out_dir, filename)
        with open(file_path, 'w') as file:
            json.dump(composite_dict, file, indent=4)


    def execute(self):
        experiment = Composite({'state': self.bigraph})



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
        name='Tellurium',
        version='2.1',
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
    sed.start_step()

    # calculate the mean and standard deviation for 'mol1' across all simulations in step 1
    sed.add_data_generator(
        data_id='stats_glc',
        observables='mol1',
        operations=['mean', 'standard_deviation']
    )

    # make the third step
    sed.start_step()

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

    # execute all the steps in the simulation experiment design
    sed.execute()



if __name__ == '__main__':
    test_builder()
