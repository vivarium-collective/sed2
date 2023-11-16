from sed2.builder import Builder, Node
import json
class SEDBuilder(Builder):
    def __init__(self, ontologies, tree=None):
        super().__init__(tree)
        self["ontologies"] = ontologies
        self["models"] = Node()
        self["simulators"] = Node()
        self["tasks"] = Node()

    def add_model(self, model_id, source):
        self["models"][model_id] = {
            "id": model_id,
            "source": source
        }

    def add_simulator(self, simulator_id, _type):
        self["simulators"][simulator_id] = {
            "id": simulator_id,
            "_type": _type
        }
    def add_task(self, task_path, task_id, inputs=None, outputs=None):
        # assign the result of add_process back to the task
        self[task_path + (task_id,)] = Node().add_process(
            process_id=task_id,
            process_type='task',
            inputs=inputs,
            outputs=outputs
        )

    def add_simulation_to_task(self, task_path, simulation_id, simulator_id, model_id, start_time, end_time, number_of_points, observables):
        simulation = Node().add_process(
            process_id=simulation_id,
            process_type='simulation',
            config={
                "simulator_id": simulator_id,
                "model_id": model_id,
                "start_time": start_time,
                "end_time": end_time,
                "number_of_points": number_of_points,
                "observables": observables
            }
        )
        # Ensure the task path exists and then add simulation to the specified task
        task_node = self[task_path]
        if "simulations" not in task_node:
            task_node["simulations"] = Node()
        task_node["simulations"][simulation_id] = simulation

    def to_json(self, filename):
        with open(f'{filename}.json', 'w') as file:
            json.dump(self.tree, file, indent=4)


def test_builder():
    demo_workflow = SEDBuilder(ontologies=['KISAO', 'sbml', 'biomodels'])
    demo_workflow.add_model('model1', 'biomodels:BIOMD0000000246')
    demo_workflow.add_simulator('simulator1', 'KISAO:CVODE')

    # Task paths are tuples indicating where to place the tasks
    demo_workflow.add_task(('tasks',), 'initial_simulation', inputs=[], outputs=[])
    demo_workflow.add_task(('tasks',), 'modify_model', inputs=[], outputs=[])

    demo_workflow.add_simulation_to_task(('tasks', 'initial_simulation'), 'initial_run', 'simulator1', 'model1', 0, 100,
                                         1000, ['observable1', 'observable2'])
    demo_workflow.add_simulation_to_task(('tasks', 'modify_model'), 'second_run', 'simulator1', 'model2', 0, 100, 1000,
                                         ['observable1', 'observable2'])

    demo_workflow.to_json('sed2demo')



if __name__ == '__main__':
    test_builder()
