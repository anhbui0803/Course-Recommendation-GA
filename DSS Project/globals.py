import json
import graph

# Define a list of available courses
AVAILABLE_COURSES = []
MANDATORY_COURSES = []
BASIC_COURSES = []
INDEPTH_COURSES = []
UNBOUND_COURSES_ID = [11, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 18, 23, 28]
UNBOUND_COURSES = []

# Define the number of courses to recommend to each student
NUM_COURSES = 42

# Define the number of credits required for graduation
CREDITS = 128

# Define the population size
POP_SIZE = 600
NUM_GENERATIONS = 10000

# Define the probability of mutation
MUTATION_PROB = 1

# Define graph
G = graph.create_graph()

# Define a function to add courses to the available courses list
def adding_courses():
    global AVAILABLE_COURSES
    global MANDATORY_COURSES
    global BASIC_COURSES
    global INDEPTH_COURSES
    global UNBOUND_COURSES
    global UNBOUND_COURSES_ID
    with open('courses/mandatory_courses.json') as f:
        data = json.load(f)
        for i in data:
            AVAILABLE_COURSES.append(i)
            MANDATORY_COURSES.append(i)
    with open('courses/basic_knowledge_courses.json') as f:
        data = json.load(f)
        for i in data:
            AVAILABLE_COURSES.append(i)
            BASIC_COURSES.append(i)
    with open('courses/indepth_knowledge_courses.json') as f:
        data = json.load(f)
        for i in data:
            AVAILABLE_COURSES.append(i)
            INDEPTH_COURSES.append(i)
