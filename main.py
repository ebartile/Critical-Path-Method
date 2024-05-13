import sys
import json
import matplotlib.pyplot as plt
import numpy as np

def schedule_tasks(json_file, num_resources):
    # Open and load the JSON file containing task information
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Define a depth-first search (DFS) function for topological sorting
    # Depth-first search (DFS) is used in the solution to perform topological 
    # sorting of tasks. 
    # Topological sorting ensures that tasks are scheduled in an order that 
    # respects their dependencies, i.e., no task is scheduled before its 
    # prerequisites are completed.
    def dfs(node, graph, visited, stack):
        visited.add(node)
        # Visit each neighbor recursively
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor, graph, visited, stack)
        # Add the current node to the stack after visiting all neighbors
        stack.append(node)

    # Create a graph representation of tasks and their dependencies
    graph = {task_id: task['dependencies'] for task_id, task in data.items()}
    visited = set()
    stack = []
    # Perform topological sorting using DFS to determine task execution order
    for node in graph:
        if node not in visited:
            dfs(node, graph, visited, stack)

    # Reverse the stack to get the order of tasks for scheduling
    ordered_tasks = stack[::-1]

    # Calculate the earliest start time for each task
    earliest_start_time = {task_id: 0 for task_id in ordered_tasks}
    for task_id in ordered_tasks:
        # Find the maximum completion time of dependencies
        max_dependency_time = max([earliest_start_time[dependency] for dependency in data[task_id]['dependencies']], default=0)
        # Set the earliest start time as the maximum completion time of dependencies
        earliest_start_time[task_id] = max_dependency_time

    # Allocate resources to tasks based on earliest start times and resource availability
    task_schedule = {}
    resource_availability = {i: 0 for i in range(num_resources)}
    for task_id in ordered_tasks:
        start_time = earliest_start_time[task_id]
        duration = data[task_id]['timeRequired']
        # Find available resources at the start time of the task
        available_resources = [resource for resource, time in resource_availability.items() if time <= start_time]
        if available_resources:
            # Assign the task to the resource with the earliest availability
            resource = min(available_resources, key=lambda x: resource_availability[x])
            resource_availability[resource] = start_time + duration
            task_schedule[task_id] = {'start_time': start_time, 'resource': resource}
        else:
            # If no resources are available, delay the task until a resource becomes available
            delay_time = min(resource_availability.values()) - start_time
            start_time += delay_time
            resource = min(resource_availability, key=resource_availability.get)
            resource_availability[resource] += duration
            task_schedule[task_id] = {'start_time': start_time, 'resource': resource}

    # Calculate the total completion time by finding the maximum completion time across all resources
    total_completion_time = max(resource_availability.values())

    return task_schedule, total_completion_time, data

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python main.py <json_file_path> <num_resources>")
        sys.exit(1)

    # Get JSON file path and number of resources from command-line arguments
    json_file = sys.argv[1]
    num_resources = int(sys.argv[2])

    # Call the schedule_tasks function with the provided arguments
    schedule, completion_time, data = schedule_tasks(json_file, num_resources)
    # Print the task schedule and total completion time
    print("Task Schedule:")
    print(json.dumps(schedule, indent=2))
    print("Total Completion Time:", completion_time)

    # Plotting the Gantt chart
    fig, ax = plt.subplots()

    for task_id, task_info in schedule.items():
        start_time = task_info['start_time']
        duration = data[task_id]['timeRequired']
        resource = task_info['resource']
        ax.barh(task_id, duration, left=start_time, align='center', color='blue', alpha=0.6)
        ax.text(start_time + duration / 2, task_id, f'Resource {resource}', ha='center', va='center', color='black')

    ax.set_xlabel('Time')
    ax.set_ylabel('Task')
    ax.set_title('Task Schedule')
    ax.set_yticks(range(len(schedule)))
    ax.set_yticklabels(schedule.keys())
    ax.grid(True)
    ax.invert_yaxis()  # Invert Y-axis to have Task 1 at the top

    plt.show()