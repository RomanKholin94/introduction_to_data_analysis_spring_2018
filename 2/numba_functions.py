from numba import jit
import numpy as np

@jit(nopython=True)
def matrix_multiply(X, Y):
    """ Matrix multiplication
    Inputs:
      - X: A numpy array of shape (N, M)
      - Y: A numpy array of shape (M, K)
    Output:
      - out: A numpy array of shape (N, K)
    """
    N = X.shape[0]
    M = X.shape[1]
    K = Y.shape[1]
    Z = np.zeros((N, K), dtype=np.float64)
    z = 0.0;
    for i in range(N):
        for j in range(K):
            z = 0.0
            for k in range(M):
                z += X[i, k] * Y[k, j]
            Z[i, j] = z
    return Z


@jit(nopython=True)
def matrix_rowmean(X, weights=np.empty(0)):
    """ Calculate mean of each row.
    In case of weights do weighted mean.
    For example, for matrix [[1, 2, 3]] and weights [0, 1, 2]
    weighted mean equals 2.6666 (while ordinary mean equals 2)
    Inputs:
      - X: A numpy array of shape (N, M)
      - weights: A numpy array of shape (M,)
    Output:
      - out: A numpy array of shape (N,)
    """
    N = X.shape[0]
    M = X.shape[1]
    Y = np.zeros((N), dtype=np.float64)
    s = 0.0;
    d = 0.0;
    W = np.zeros((M), dtype=np.float64)
    if weights.size:
        for l, x in enumerate(weights):
            W[l] = x
            d += x
        for i in range(N):
            s = 0.0
            for j in range(M):
                s += X[i, j] * W[j]
            Y[i] = s / d
    else:
        d = M
        for i in range(N):
            s = 0.0
            for j in range(M):
                s += X[i, j]
            Y[i] = s / d
    return Y


@jit(nopython=True)
def cosine_similarity(X, top_n=10, with_mean=True, with_std=True):
    """ Calculate cosine similarity between each pair of row.
    1. In case of with_mean: subtract mean of each row from row
    2. In case of with_std: divide each row on it's std
    3. Select top_n best elements in each row or set other to zero.
    4. Compute cosine similarity between each pair of rows.
    Inputs:
      - X: A numpy array of shape (N, M)
      - top_n: int, number of best elements in each row
      - with_mean: bool, in case of subtracting each row's mean
      - with_std: bool, in case of subtracting each row's std
    Output:
      - out: A numpy array of shape (N, N)

    Example (with top_n=1, with_mean=True, with_std=True):
        X = array([[1, 2], [4, 3]])
        after mean and std transform:
        X = array([[-1.,  1.], [ 1., -1.]])
        after top n choice
        X = array([[0.,  1.], [ 1., 0]])
        cosine similarity:
        X = array([[ 1.,  0.], [ 0.,  1.]])

    """
    N = X.shape[0]
    M = X.shape[1]
    Z = np.zeros((N, 1), dtype=np.float64)
    ZZ = np.zeros((N, N), dtype=np.float64)
    XX = np.zeros((N, N), dtype=np.float64)
    answer = np.zeros((N, N), dtype=np.float64)
    mean = 0.0;
    std = 0.0;
    d = M;

    if with_mean:
        for i in range(N):
            mean = 0.0
            for j in range(M):
                mean += X[i, j]
            for j in range(M):
                X[i, j] -= mean / d
    if with_std:
        for i in range(N):
            mean = 0.0
            for j in range(M):
                mean += X[i, j]
            mean /= d
            std = 0.0
            for j in range(M):
                std += (X[i, j] - mean) * (X[i, j] - mean)
            std = np.sqrt(std / d)
            for j in range(M):
                X[i, j] /= std
    Y = np.argsort(np.argsort(X, axis=1)[:,0:M - top_n]
    for i in range(N):
        X[i][Y[i]] = 0.0
    for i in range(N):
        a = 0.0
        for j in range(M):
            a += X[i, j] * X[i, j]
        Z[i, 0] = np.sqrt(a)
    ZZ = matrix_multiply(Z, Z.T)
    XX = matrix_multiply(X, X.T)
    for i in range(N):
        for j in range(N):
            answer[i, j] = XX[i, j] / ZZ[i, j]
    return answer
