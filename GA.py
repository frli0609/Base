import random
import copy
import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class FJSP:
    def __init__(self, job_machine_time):
        self.job_machine_time = job_machine_time
        self.job_number = len(self.job_machine_time)
        self.machine_number = len(self.job_machine_time[0][0])
        self.job_machien = [[[k for k in range(len(self.job_machine_time[i][j]))
                              if self.job_machine_time[i][j][k] != -1] for j in range(len(self.job_machine_time[i]))]
                            for i in range(len(self.job_machine_time))]
        self.job_time = [[[self.job_machine_time[i][j][k] for k in range(len(self.job_machine_time[i][j]))
                           if self.job_machine_time[i][j][k] != -1] for j in range(len(self.job_machine_time[i]))]
                         for i in range(len(self.job_machine_time))]
        self.job_start_time = [[0 for j in range(len(self.job_machine_time[i]))] for i in range(self.job_number)]
        self.job_end_time = [[0 for j in range(len(self.job_machine_time[i]))] for i in range(self.job_number)]
        self.machine_start_time = [0 for i in range(self.machine_number)]
        self.machine_end_time = [0 for i in range(self.machine_number)]
        self.job_process_record = [0 for i in range(self.job_number)]
        self.job_what_machine = [[0 for j in range(len(self.job_machine_time[i]))] for i in range(self.job_number)]

    def double_code(self):
        record = [0 for i in range(self.job_number)]
        codes = []
        for i in range(self.job_number):
            for j in range(len(self.job_start_time[i])):
                codes.append(i)
        random.shuffle(codes)
        machines = []
        for i in range(len(codes)):
            # codes[i] 是工件 record[codes[i]]是工序
            machines.append(random.choice(self.job_machien[codes[i]][record[codes[i]]]))
            record[codes[i]] += 1
        return [codes, machines]

    def decode(self, codes):
        # codes = [[工件编码], [机器编码]]
        for i in range(len(codes[0])):
            # codes[0][i] 工件    codes[1][i] 机器    self.job_process_record[codes[i]] 工序
            job = codes[0][i]
            machine = codes[1][i]
            process = self.job_process_record[codes[0][i]]
            if process == 0:
                self.job_start_time[job][process] = self.machine_end_time[machine]
            else:
                self.job_start_time[job][process] = max(self.machine_end_time[machine],
                                                        self.job_end_time[job][process - 1])
            self.job_what_machine[job][process] = machine
            machine_index = self.job_machien[job][process].index(machine)
            self.job_end_time[job][process] = self.job_start_time[job][process] + \
                self.job_time[job][process][machine_index]
            self.machine_start_time[machine] = self.job_start_time[job][process]
            self.machine_end_time[machine] = self.job_end_time[job][process]
            self.job_process_record[job] += 1

    def get_fitness(self):
        return 1 / max(self.machine_end_time)

    def reset(self):
        self.__init__(self.job_machine_time)

    @staticmethod
    def job_mutation(codes):
        a = random.randint(0, len(codes[0]) - 1)
        b = random.randint(0, len(codes[0]) - 1)
        record1 = []
        recode2 = []
        for i in range(len(codes[0])):
            if codes[0][i] == codes[0][a]:
                record1.append(codes[1][i])
            if codes[0][i] == codes[0][b]:
                recode2.append(codes[1][i])
        record1.reverse()
        recode2.reverse()
        tem = codes[0][a]
        codes[0][a] = codes[0][b]
        codes[0][b] = tem
        for i in range(len(codes[0])):
            if codes[0][i] == codes[0][a]:
                codes[1][i] = recode2.pop()
            if codes[0][i] == codes[0][b]:
                codes[1][i] = record1.pop()
        return codes

    def machines_mutation(self, codes):
        rand = random.randint(0, len(codes[0]) - 1)
        pro = 0
        for i in range(rand):
            if codes[0][i] == codes[0][rand]:
                pro += 1
        codes[1][rand] = random.choice(self.job_machien[codes[0][rand]][pro])
        return codes

    @staticmethod
    def pox_crossover(code1, code2):
        a = random.choice(list(set(code1[0])))
        code11 = [i if i != a else -1 for i in code1[0]]
        code12 = [a if i == a else -1 for i in code1[0]]
        code21 = [i if i != a else -1 for i in code2[0]]
        code22 = [a if i == a else -1 for i in code2[0]]
        code1m = copy.deepcopy(code1[1])
        code2m = copy.deepcopy(code2[1])
        code11.reverse()
        code21.reverse()
        code1m.reverse()
        code2m.reverse()
        codem1 = []
        codem2 = []
        for i in range(len(code1[0])):
            codem1.append(code1[1][i])
            codem2.append(code2[1][i])
            while code12[i] == -1:
                code12[i] = code21.pop()
                codem1[i] = code2m.pop()
            while code22[i] == -1:
                code22[i] = code11.pop()
                codem2[i] = code1m.pop()
        return [code12, codem1], [code22, codem2]

    @staticmethod
    def selection(fitness):
        new_pop = []
        max_f = max(fitness)
        min_f = min(fitness)
        for i in range(len(fitness)):
            fitness[i] = (fitness[i] - min_f) / (max_f - min_f)
        temp = 0
        while len(new_pop) != len(fitness):
            if fitness[temp] > random.random():
                new_pop.append(temp)
            temp += 1
            if temp == len(fitness):
                temp = 0
        return new_pop

    def draw_gantte(self):
        colors = ['b', 'c', 'g', 'k', 'm', 'r', 'y', 'w']
        for i in range(len(self.job_start_time)):
            for j in range(len(self.job_start_time[i])):
                plt.barh(self.job_what_machine[i][j] + 1, self.job_end_time[i][j] - self.job_start_time[i][j],
                         left=self.job_start_time[i][j], color=colors[i])
        label_name = ['JOB' + str(i + 1) for i in range(self.job_number)]
        patches = [mpatches.Patch(color=colors[i], label=label_name[i]) for i in range(len(label_name))]
        plt.legend(handles=patches, loc=4)
        plt.yticks([i + 1 for i in range(self.machine_number)])
        plt.show()


class GAstep:
    def __init__(self, population_number, crossover_odd, mutation_odd, loop_time, breek_value, fjsp):
        self.fjsp = fjsp
        self.population_number = population_number
        self.mutation_odd = mutation_odd
        self.crossover_odd = crossover_odd
        self.loop_time = loop_time
        self.break_value = breek_value
        self.population = [self.fjsp.double_code() for i in range(self.population_number)]

    def one_loop(self):
        fitness = []
        for i in self.population:
            self.fjsp.decode(i)
            fitness.append(self.fjsp.get_fitness())
            self.fjsp.reset()
            if 1 / max(fitness) <= self.break_value:
                return i, True
        # noinspection PyBroadException
        try:
            index = self.fjsp.selection(fitness)
            new_pop = [self.population[i] for i in index]
            for i in range(len(new_pop)):
                a = random.randint(0, len(new_pop) - 1)
                if self.crossover_odd > random.random():
                    new_pop[i], new_pop[a] = self.fjsp.pox_crossover(new_pop[i], new_pop[a])
                if self.mutation_odd > random.random():
                    new_pop[i] = self.fjsp.job_mutation(new_pop[i])
            return new_pop, False
        except:
            return self.population[0], True

    def main(self):
        for i in range(self.loop_time):
            self.population, flag = self.one_loop()
            if flag:
                self.fjsp.decode(self.population)
                return 1 / self.fjsp.get_fitness(), self.population
        final_fitness = []
        for i in self.population:
            self.fjsp.decode(i)
            final_fitness.append(1 / self.fjsp.get_fitness())
            self.fjsp.reset()
        return min(final_fitness), self.population[final_fitness.index(min(final_fitness))]

    def reset(self):
        self.__init__(self.population_number, self.crossover_odd,
                      self.mutation_odd, self.loop_time, self.break_value, self.fjsp)
        self.fjsp.reset()


# 最小 38
job_machine = [
    [[5, 8, 11, -1, -1, -1, -1, -1, 9],
     [-1, -1, -1, 4, 6, 4, -1, -1, -1],
     [6, -1, -1, -1, 5, -1, -1, 7, -1],
     [-1, -1, 5, -1, -1, 5, -1, 8, -1],
     [11, -1, -1, 9, 4, 8, -1, -1, -1]],
    [[5, 4, -1, -1, -1, -1, -1, -1, 7],
     [-1, 7, -1, 6, -1, -1, 10, -1, -1],
     [-1, -1, -1, 5, -1, -1, 6, -1, -1],
     [10, -1, -1, -1, 9, -1, 11, -1, -1]],
    [[15, 9, -1, -1, -1, -1, -1, -1, 13],
     [14, -1, 17, -1, -1, -1, 19, -1, -1]],
    [[-1, -1, -1, 7, -1, -1, -1, -1, 5],
     [-1, -1, 13, -1, 10, -1, -1, 8, -1],
     [13, -1, 11, -1, -1, -1, 10, -1, -1],
     [-1, -1, 12, -1, -1, -1, -1, 9, -1],
     [-1, 9, -1, -1, -1, -1, 15, 6, -1]]]
f = FJSP(job_machine)
test = []
ga = GAstep(100, 0.8, 0.1, 200, 30, f)
time_1 = time.time()
for its in range(1):
    f_fit, gens = ga.main()
    test.append([f_fit, gens])
    ga.reset()
test = sorted(test, key=lambda x: x[0])
print('遗传算法求解结果为:', '\n',
      '最短时间:', test[0][0], '\n',
      '最佳染色体:', test[0][1], '\n',
      '耗时:', time.time() - time_1)
f.reset()
f.decode(test[0][1])
f.draw_gantte()

