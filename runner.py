from tests import strategy, agent_type
import csv
import os
import numpy

RUNS = 100

TESTS = [
    # strategy
    agent_type
]
for test in TESTS:
    for i in range(RUNS):
        print("Running %s for %d iteration ..." % (test.name, i))
        with open("out/%s_%d.csv" % (test.name, i), 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            test.test(csvwriter)

    print("Computing average")

    files = [i for i in os.listdir("out") if test.name in i]
    data = None

    for file in files:
        d = numpy.genfromtxt("out/%s" % file, delimiter=',')
        if data is None:
            data = d
        else:
            data += d

    data = data / len(files)
    numpy.savetxt("out/%s_merged.csv" % (test.name), data, delimiter=",")
