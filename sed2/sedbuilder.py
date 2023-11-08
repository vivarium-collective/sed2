import json
import os

from sed2.builder import pf, Builder, Node



class SEDBuilder(Builder):
    def __init__(self, bigraph_dict=None):
        # Initialize with the specific schema keys for SED
        super().__init__(
            schema_keys=['annotations', ],
            bigraph_dict=bigraph_dict,
            node_class=SEDNode,
        )

        self.models = {}
        self.simulators = {}

    def add_model(
            self,
            name,
            source,
            type=None,
            changes=None,
    ):
        # Ensure the model ID is unique
        assert name not in self.models, f"Model '{name}' already exists."

        # TODO -- apply changes to model

        # Add a model to the 'models' dictionary
        self.models[name] = {
            'source': source,
            'language': f'urn:sedml:language:{type}'
        }

    def add_task(self, task_id='1'):
        self.add_process(process_id=task_id)

    def add_dataset(self):
        pass

    def add_simulator(self, name, simulator, version, kisao_id):
        # Ensure the simulator ID is unique
        assert name not in self.simulators, f"Simulator '{name}' already exists."
        # Add a simulator to the 'simulators' dictionary
        self.simulators[name] = {
            'simulator': simulator,
            'version': version,
            'kisao_id': f'KISAO:{kisao_id}'
        }

    # def add_simulation(
    #         self,
    #         simulation_id,
    #         simulator_id,
    #         model_id,
    #         start_time=None,
    #         end_time=None,
    #         number_of_points=None,
    #         observables=None,  # TODO to capture all model variables, omit this or have a method to specify all.
    # ):
    #     model_source = self.models[model_id]['source']
    #     simulator_name = self.simulators[simulator_id]['name']
    #     address = f'local:{simulator_name}'
    #     config = {  # TODO -- this has to be the standardized config of a given simulator instance
    #         'model_file': model_source,
    #         'kisao_id': self.simulators[simulator_id]['kisao_id'],  # TODO -- kisao ID should set the config shape and ports,
    #         # 'start_time': start_time,
    #         # 'end_time': end_time,
    #         # 'number_of_points': number_of_points,
    #         'observables': observables,
    #     },
    #     self.add_process(
    #         process_id=simulation_id,
    #         type='step',
    #         address=address,
    #         config=config, )


    def add_data_generator(
            self,
            data_id,
            simulation_id=None,  # TODO
            observables=None,
            operations=None,
            generator_id='data_operation',
    ):
        pass

    def add_visualization(
            self,
            plot_id,
            plot_type=None,
            title=None,
            x_label=None,
            y_label=None,
            legend=None,
    ):
        pass

    def print_sed_doc(self):
        print(pf(self._bigraph))

    def save_sed_doc(self, filename=None, out_dir='out'):
        composite_dict = self._bigraph
        file_path = os.path.join(out_dir, filename)
        with open(file_path, 'w') as file:
            json.dump(composite_dict, file, indent=4)

    def save_archive(self):
        """save all the models and metadata in an archive"""
        pass



def test_sedbuilder():
    sed = SEDBuilder()
    sed


if __name__ == '__main__':
    test_sedbuilder()
