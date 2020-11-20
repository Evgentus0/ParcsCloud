# import gmpy2
from Pyro4 import expose
import random


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))

        client_number = self.read_input()

        step = client_number / len(self.workers)

        # map
        mapped = []
        for i in range(0, len(self.workers)):
            print("map %d" % i)
            mapped.append(self.workers[i].mymap(client_number, i * step, (i+1) * step))

        # reduce
        result = self.myreduce(mapped)

        # output
        self.write_output(result)

    @staticmethod
    @expose
    def mymap(amount, left, right):
        smo_two = [SMO(1, 1, 1.000000000000123), SMO(1, 1, 0.999999952342)]

        if left != 0:
            left += 1
        print(left)
        print(right)

        result = 0
        counter = left

        while counter <= right:
            result += smo_two[0].get_p(counter) * smo_two[1].get_p(amount - counter)
            counter += 1

        return result

    @staticmethod
    @expose
    def myreduce(mapped):
        print("reduce")
        reverse_result = 1
	
        for sub_result in mapped:
            print("reduce loop")
            reverse_result += sub_result.value
        print("reduce done")

        return 1 / reverse_result

    def read_input(self):
        f = open(self.input_file_name, 'r')
        n = int(f.readline())
        f.close()
        return n

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()
        print("output done")


class SMO:
    def __init__(self, r, e, mu):
        self.r = r
        self.e = e
        self.mu = mu

    @staticmethod
    def factorial(number):
        if number == 0:
            return 1
        else:
            return number * SMO.factorial(number - 1)

    def get_p(self, k):
        first_part = (self.e / self.mu) ** k
        second_part = 0

        if k <= self.r:
            second_part = 1 / SMO.factorial(k)
        else:
            second_part = 1 / (SMO.factorial(self.r) * (self.r ** (k-self.r)))

        return first_part * second_part
