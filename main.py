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

    return task_schedule, total_completion_time

def visualize_schedule(schedule, num_resources):
    # Extract task start times and resources
    task_start_times = {task_id: info['start_time'] for task_id, info in schedule.items()}
    resources = {info['resource'] for info in schedule.values()}
    
    # Create a plot for each resource
    fig, axes = plt.subplots(len(resources), 1, figsize=(10, len(resources) * 2))
    if len(resources) == 1:
        axes = [axes]  # Ensure axes is a list for uniformity
    
    for i, resource in enumerate(sorted(resources)):
        # Filter tasks assigned to the current resource
        resource_tasks = {task_id: info for task_id, info in schedule.items() if info['resource'] == resource}
        # Sort tasks by start time
        sorted_tasks = sorted(resource_tasks.items(), key=lambda x: x[1]['start_time'])
        
        # Plot task timeline
        axes[i].set_title(f"Resource {resource} Schedule")
        axes[i].set_xlabel("Time")
        axes[i].set_ylabel("Task")
        for j, (task_id, info) in enumerate(sorted_tasks):
            axes[i].barh(task_id, info['start_time'], info['start_time'] + data[task_id]['timeRequired'] - info['start_time'], left=info['start_time'])
            axes[i].text(info['start_time'] + (data[task_id]['timeRequired'] - info['start_time']) / 2, j, f"{task_id}\n{info['start_time']:.1f}-{info['start_time'] + data[task_id]['timeRequired']:.1f}", ha='center', va='center')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python main.py <json_file_path> <num_resources>")
        sys.exit(1)

    # Get JSON file path and number of resources from command-line arguments
    json_file = sys.argv[1]
    num_resources = int(sys.argv[2])

    # Call the schedule_tasks function with the provided arguments
    schedule, completion_time = schedule_tasks(json_file, num_resources)
    # Print the task schedule and total completion time
    print("Task Schedule:")
    print(json.dumps(schedule, indent=2))
    print("Total Completion Time:", completion_time)
    visualize_schedule(schedule, num_resources)
