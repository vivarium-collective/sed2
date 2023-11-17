from sed2.builder import Builder, Node
import json
class SEDBuilder(Builder):
    def __init__(self, ontologies=None, tree=None):
        super().__init__(tree)
        self['ontologies'] = ontologies
        self['models'] = Node()
        self['simulators'] = Node()
        # self['tasks'] = Node()

    def add_model(
            self, 
            model_id, 
            source,  # this should support paths, urls, local
            changes=None,
    ):
        self['models'][model_id] = {
            'id': model_id,
            'source': source,
            'changes': changes,  # apply these changes?
        }

    def add_simulator(self, simulator_id, type):
        self['simulators'][simulator_id] = {
            'id': simulator_id,
            '_type': type
        }

    def to_json(self, filename):
        with open(f'{filename}.json', 'w') as file:
            json.dump(self.tree, file, indent=4)

    def to_archive(self, name):
        pass

def test_builder():
    # Initialize the SEDBuilder with relevant ontologies
    simulation_workflow = SEDBuilder(ontologies=['KISAO', 'sbml', 'biomodels'])

    # Add a biological model, specifying its source (e.g., a BioModels database entry)
    simulation_workflow.add_model(
        model_id='biological_system_model',
        source='biomodels:MODEL12345'  # Replace with actual BioModels ID or file path
    )

    # Add a numerical simulator, specifying the algorithm (e.g., an ODE solver from KISAO)
    simulation_workflow.add_simulator(
        simulator_id='ode_solver',
        type='KISAO:0000019'  # Replace with actual KiSAO ID for the solver
    )

    # Create a simulation task, representing a specific experiment or analysis
    simulation_workflow.add_task(
        task_id='cellular_response_simulation',
        inputs=[],  # Define inputs if any
        outputs=[]  # Define outputs if any
    )

    # Define simulation parameters: start time, end time, number of points
    start_time = 0
    end_time = 100
    number_of_points = 1000
    simulation_workflow['cellular_response_simulation'].add_simulation(
        'time_course_analysis',
        simulator_id='ode_solver',
        model_id='biological_system_model',
        start_time=start_time,
        end_time=end_time,
        number_of_points=number_of_points,
        outputs=['metabolite_concentration', 'gene_expression']  # Replace with actual observables
    )

    # Export the SED-ML document as JSON and as an archive for execution
    simulation_workflow.to_json('cellular_response_experiment')
    simulation_workflow.to_archive('cellular_response_experiment')










if __name__ == '__main__':
    test_builder()
