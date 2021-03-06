import numpy as np


class KHMean:

    def __init__(self):
        pass

    def _get_distance(self, x, centers):
        dist = []
        for i in range(len(centers)):
            dist.append(np.linalg.norm(np.array(centers[i]) - np.array(x)))
        return dist

    def _get_weight(self, d):
        return np.power(d, 3) * (np.power(sum(1./np.power(d, 2)), 2))

    def train(self, rdd, k, maxIterations=100):
        """
        This method trains a model based on the K Harmonic Mean algorithm.
        This method is for implementation using PySpark

        :param rdd: rdd
        a rdd of features vectors, a list of lists or a list of tuples
        Feature vectors should be floating point numbers or integers.
        :param k: integer
        number of clusters
        :param maxIterations: integer
        number of iterations to run, default number of iterations = 100
        :return: list of lists
        centroids of the clusters
        """
        centers = rdd.takeSample('false', k)  # Get initial centers randomly from the range of the input
        print ('initial centers')
        print (centers)
        for i in range(maxIterations):
            d = rdd.map(lambda x: [x, self._get_distance(x, centers)]).map(lambda x: [x[0], np.array(x[1])+1e-6])\
                .map(lambda x: [x[0], x[1].tolist()])
            d_indexed = d.map(lambda x: [x[0], x[1], x[1].index(min(x[1]))])
            q_indexed = d_indexed.map(lambda x: [x[0], self._get_weight(np.array(x[1])), x[2]])
            for l in range(k):
                m = q_indexed.filter(lambda x: x[2] == l).map(lambda x: [x[0], x[1].tolist(), x[2]])\
                    .map(lambda x: [x[0], x[1][l] * np.array(x[0]), x[1][l], x[2]])
                c = m.map(lambda x: x[1].tolist()).reduce(lambda x, y: [x[0] + y[0], x[1] + y[1]])
                q_sum = m.map(lambda x: x[2]).reduce(lambda x, y: x + y)
                center = np.array(c)/q_sum
                centers[l] = center.tolist()
            print ('update centres')
            print (centers)
        return centers

