import numpy as np


def clusterVal(y, clusterid):
    '''
    CLUSTERVAL Estimate cluster validity using Entropy, Purity, Rand Statistic,
    and Jaccard coefficient.

    Usage:
      Entropy, Purity, Rand, Jaccard = clusterval(y, clusterid);

    Input:
       y         N-by-1 vector of class labels
       clusterid N-by-1 vector of cluster indices

    Output:
      Entropy    Entropy measure.
      Purity     Purity measure.
      Rand       Rand index.
      Jaccard    Jaccard coefficient.
    '''
    y = np.asarray(y).ravel()
    clusterid = np.asarray(clusterid).ravel()
    C = np.unique(y).size
    K = np.unique(clusterid).size
    N = y.shape[0]
    EPS = 2.22e-16

    p_ij = np.zeros((K, C))
    # probability that member of i'th cluster belongs to j'th class
    m_i = np.zeros((K, 1))
    # total number of objects in i'th cluster
    for k in range(K):
        m_i[k] = (clusterid == k).sum()
        yk = y[clusterid == k]
        for c in range(C):
            m_ij = (yk == c).sum()
            # number of objects of j'th class in i'th cluster
            p_ij[k, c] = m_ij.astype(float)/m_i[k]
    entropy = ((1-(p_ij*np.log2(p_ij+EPS)).sum(axis=1))*m_i.T).sum() / (N*K)
    purity = (p_ij.max(axis=1)).sum() / K

    f00, f01, f10, f11 = 0, 0, 0, 0
    for i in range(N):
        for j in range(i):
            if y[i] != y[j] and clusterid[i] != clusterid[j]:
                f00 += 1
                # different class, different cluster
            elif y[i] == y[j] and clusterid[i] == clusterid[j]:
                f11 += 1
                # same class, same cluster
            elif y[i] == y[j] and clusterid[i] != clusterid[j]:
                f10 += 1
                # same class, different cluster
            else:
                f01 += 1
                # different class, same cluster
    rand = np.float(f00+f11)/(f00+f01+f10+f11)
    jaccard = np.float(f11)/(f01+f10+f11)

    return entropy, purity, rand, jaccard
