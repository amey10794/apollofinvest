import matplotlib.pyplot as plt
import random
from datetime import datetime
fig, ax = plt.subplots(nrows=1, ncols=1)
# for i in (1,100):
ax.scatter([1,2,3],[1,2,3])
number =datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
fig.savefig('C:\\Users\\Priyank\\PycharmProjects\\untitled12\\plots2\\' + str(number) + '.png')