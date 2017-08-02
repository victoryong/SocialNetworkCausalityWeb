#python2.7
#Written by Greg Ver Steeg
#See readme.pdf for documentation
#Or go to http://www.isi.edu/~gregv/npeet.html


from math import log
import numpy as np

#####DISCRETE ESTIMATORS
def entropyd(sx,base=2):
  """ Discrete entropy estimator
      Given a list of samples which can be any hashable object
  """
  try:
      sx=[tuple(s) for s in sx]
      return entropyfromprobs(hist(sx),base=base)
  except:
      return entropyfromprobs(hist(sx),base=base)

def midd(x,y):
  """ Discrete mutual information estimator
      Given a list of samples which can be any hashable object
  """
  return -entropyd(list(zip(x,y)))+entropyd(x)+entropyd(y)

def cmidd(x,y,z):
  """ Discrete mutual information estimator
      Given a list of samples which can be any hashable object
  """
  if len(z):
      z = np.array(list(z.values()))
      x_z = np.append([x],z,axis=0)
      y_z = np.append([y],z,axis=0)
      x_y_z = np.append([x,y],z,axis=0)
      return entropyd(y_z.T)+entropyd(x_z.T)-entropyd(x_y_z.T)-entropyd(z.T)
  else:
      return midd(x,y)

def hist(sx):
  #Histogram from list of samples
  d = dict()
  for s in sx:
    d[s] = d.get(s,0) + 1
  return [float(z)/len(sx) for z in list(d.values())]

def entropyfromprobs(probs,base=2):
#Turn a normalized list of probabilities of discrete outcomes into entropy (base 2)
  return -sum(map(elog,probs))/log(base)

def elog(x):
#for entropy, 0 log 0 = 0. but we get an error for putting log 0
  if x <= 0. or x>=1.:
    return 0
  else:
    return x*log(x)

def zip2(*args):
  #zip2(x,y) takes the lists of vectors and makes it a list of vectors in a joint space
  #E.g. zip2([[1],[2],[3]],[[4],[5],[6]]) = [[1,4],[2,5],[3,6]]
  return [sum(sublist,[]) for sublist in zip(*args)]
