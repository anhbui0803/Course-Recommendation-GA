import random
from myclass import Individual
import output
from globals import *

def generate_population():
    global POP_SIZE
    global CREDITS
    global AVAILABLE_COURSES
    global MANDATORY_COURSES
    global BASIC_COURSES
    global INDEPTH_COURSES
    global NUM_COURSES
    global UNBOUND_COURSES

    population = []
    for i in range(POP_SIZE):
        courses = []
        credit = 0
        while len(courses) < NUM_COURSES - 1:
            rand_course = random.choice(AVAILABLE_COURSES)
            while rand_course in courses:
                rand_course = random.choice(AVAILABLE_COURSES)
            courses.append(rand_course)
            credit += rand_course['credits']

        courses.append(MANDATORY_COURSES[30])
        credit += MANDATORY_COURSES[30]['credits']
        population.append(Individual(courses, credit))
    return population

def genetic_algorithm():
    global NUM_GENERATIONS
    global POP_SIZE
    global MUTATION_PROB

    population = generate_population()
    found = False
    loop_num = 0
    loop = []
    avg_fitness_list = []
    while not found:
        loop_num += 1
        loop.append(loop_num)
        # Selection
        population = sorted(population, key=lambda x: x.fitness)
        new_generation = []
        s = (len(population) * 10) // 100
        new_generation.extend(population[:s])

        s = (len(population) * 90) // 100
        half = len(population) * 50 // 100

        for _ in range(s):
            # Crossover for the first half of the population
            parent1 = random.choice(population[:half])
            parent2 = random.choice(population[:half])
            child = parent1.crossover(parent2)
            # Mutation
            rand_num = random.random()
            if rand_num <= MUTATION_PROB:
                child = child.mutate()
            new_generation.append(child)

        population = new_generation
        avg_fitness = 0
        for individual in population:
            avg_fitness += individual.fitness
        avg_fitness = avg_fitness / len(population)
        avg_fitness_list.append(avg_fitness)

        if population[0].fitness == 0:
            found = True
            break

        print()
        print('Best individual in the current population: ')
        course_list = []
        for course in population[0].courses:
            course_list.append(course['course_name'])
        print(course_list)
        print('Fitness: ' + str(population[0].fitness))
        print('Fitness average: ' + str(avg_fitness))
        print('Loop number: ' + str(loop_num))
    output.print_result(population, loop, avg_fitness_list)
