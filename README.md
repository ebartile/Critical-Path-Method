# Critical Path Method (CPM)

## **Problem Statement**
[Link to Question](https://cloudchef.notion.site/CloudChef-problem-statement-67609eabef714a78a4e4370a7367698c)

## **Solution**

The Critical Path Method (CPM) is a project management technique used to plan and manage complex projects composed of multiple interdependent tasks. In the context of the task scheduling problem described in problem statement, CPM can be utilized to optimize the scheduling of tasks to minimize the total completion time.

## **How to run the code**
```bash
python main.py <json_file_path> <num_resources>
```

## **🛠️ Explanation for the code**
To tackle this problem, i used a scheduling algorithm Critical Path Method (CPM). Here's a high-level approach:

1. **Parse Input**: Read the JSON file to extract task information including IDs, time required, and dependencies.

2. **Topological Sorting**: Perform a topological sorting of the tasks to determine the order in which they should be executed. This ensures that no task is scheduled before its dependencies are completed.

3. **Calculate Earliest Start Time**: For each task, calculate the earliest start time considering the completion times of its dependencies and the availability of resources.

4. **Schedule Tasks**: Assign tasks to resources based on their earliest start times and resource availability. This step may involve heuristic methods to optimize resource allocation.

5. **Calculate Total Completion Time**: Sum up the completion times of all tasks to obtain the total completion time.

### **Why DFS**
Depth-first search (DFS) is used in the solution to perform topological sorting of tasks. Topological sorting ensures that tasks are scheduled in an order that respects their dependencies, i.e., no task is scheduled before its prerequisites are completed. Here's why DFS is employed for this purpose:

1. **Dependencies Representation**: The tasks and their dependencies are represented as a graph, where each task is a node, and the dependencies between tasks are edges. DFS is well-suited for traversing such graph structures efficiently.

2. **Visit Order**: DFS explores as far as possible along each branch of the graph before backtracking. This property ensures that tasks are visited in a specific order, allowing us to determine their scheduling order.

3. **Topological Sorting**: By using DFS, we can perform a topological sort on the graph of tasks and dependencies. In a topological sort, tasks are ordered such that for every directed edge from task A to task B, A appears before B in the sorted order. This property ensures that tasks are scheduled in a way that respects their dependencies.

4. **Time Complexity**: DFS has a time complexity of O(V + E), where V is the number of vertices (tasks) and E is the number of edges (dependencies). For the task scheduling problem, the time complexity is proportional to the number of tasks and their dependencies, making DFS an efficient choice.

### **Why  Calculate the earliest start time for each task**
Calculating the earliest start time for each task is crucial in task scheduling for several reasons:

1. **Dependency Constraints**: Tasks often have dependencies, meaning that certain tasks must be completed before others can start. By calculating the earliest start time for each task, we ensure that no task starts before its dependencies are completed. This prevents conflicts and ensures the correctness of the scheduling plan.

2. **Optimal Resource Utilization**: Knowing the earliest start time allows us to allocate resources efficiently. By starting tasks as soon as their dependencies are met, we minimize resource idle time and maximize resource utilization, leading to a more efficient overall schedule.

3. **Minimizing Total Completion Time**: The goal of task scheduling is often to minimize the total completion time, i.e., the time taken to complete all tasks. By starting tasks as early as possible while respecting dependencies, we can achieve this objective, as tasks can be completed sooner without unnecessary delays.

4. **Determining Critical Path**: The earliest start time calculation is also essential for identifying the critical path in the project. The critical path consists of tasks that, if delayed, would directly impact the overall project duration. By understanding the earliest start times, we can identify which tasks are on the critical path and focus on optimizing their execution.


## **Performance with Gannt Chart**
## **Performance for 1 reource provided**
![Alt text](/graphs/Figure_1.png)

## **Performance for 2 reource provided**
![Alt text](/graphs/Figure_2.png)

## **Performance for 3 reource provided**
![Alt text](/graphs/Figure_3.png)

## **Performance for 4 reource provided**
![Alt text](/graphs/Figure_4.png)
