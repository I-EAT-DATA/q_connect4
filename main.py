import pickle
import random

from train import train
from play import play
from q_connect4_agent import QConnect4Agent

alpha = 0.5
epsilon = 0.5

q_agent = QConnect4Agent(alpha=alpha, epsilon=epsilon)

# q_agent.q = pickle.load(open('q_agent_q.pkl', 'rb'))
q_agent.q.update(train(q_agent=q_agent, n=1000))

# pickle.dump(q_agent.q, open('q_agent_dict.pkl', 'wb'))

print(q_agent.q)

play(q_agent=q_agent, human=random.randint(0, 1), helper=False)