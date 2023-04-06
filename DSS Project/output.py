from tabulate import tabulate
import matplotlib.pyplot as plt
from matplotlib import style

def print_result(population, loop, avg_fitness_list):
    print()
    print("Best individual in the final population: ")
    sem_1, sem_2, sem_3, sem_4, sem_5, sem_6, sem_7, sem_8 = [], [], [], [], [], [], [], []
    count = 0
    for course in population[0].courses:
        if count < 6:
            sem_1.append(course['course_name'])
        elif count < 12:
            sem_2.append(course['course_name'])
        elif count < 18:
            sem_3.append(course['course_name'])
        elif count < 24:
            sem_4.append(course['course_name'])
        elif count < 30:
            sem_5.append(course['course_name'])
        elif count < 35:
            sem_6.append(course['course_name'])
        elif count < 40:
            sem_7.append(course['course_name'])
        else:
            sem_8.append(course['course_name'])
        count += 1

    data = [[sem_1[0], sem_2[0], sem_3[0], sem_4[0], sem_5[0], sem_6[0], sem_7[0], sem_8[0]],
            [sem_1[1], sem_2[1], sem_3[1], sem_4[1], sem_5[1], sem_6[1], sem_7[1], sem_8[1]],
            [sem_1[2], sem_2[2], sem_3[2], sem_4[2], sem_5[2], sem_6[2], sem_7[2], ''],
            [sem_1[3], sem_2[3], sem_3[3], sem_4[3], sem_5[3], sem_6[3], sem_7[3], ''],
            [sem_1[4], sem_2[4], sem_3[4], sem_4[4], sem_5[4], sem_6[4], sem_7[4], ''],
            [sem_1[5], sem_2[5], sem_3[5], sem_4[5], sem_5[5], '', '', '']]

    print(tabulate(data, headers=['Semester 1', 'Semester 2', 'Semester 3', 'Semester 4', 'Semester 5', 'Semester 6', 'Semester 7', 'Semester 8'], tablefmt='orgtbl'))

    plt.figure(figsize=(20, 10))
    plt.rc('xtick', labelsize=26)
    plt.rc('ytick', labelsize=26)
    plt.plot(loop, avg_fitness_list, linewidth=6)
    plt.xlabel('Loop number', fontsize=26, labelpad=10, fontweight='bold')
    plt.ylabel('Fitness average', fontsize=26, labelpad=15, fontweight='bold')
    plt.title('Fitness average vs Loop number', fontsize=30, pad=20, fontweight='bold')
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.grid(True, linewidth=1.5, linestyle='--')
    plt.show()
