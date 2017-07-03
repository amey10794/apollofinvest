import pickle
with open('iter.pkl', 'rb') as f:
    iter_pk = pickle.load(f)
with open('env_paretos/'+str(iter_pk)+'pareto.pkl', 'wb') as f:
    pickle.dump(l, f)

with open('env_paretos/2pareto.pkl', 'rb') as f:
    iter_pk = pickle.load(f)

print(iter_pk)