import multiprocessing
import time

# def worker():
#     name = multiprocessing.current_process().name
#     print(name, 'Starting')
#     time.sleep(2)
#     print(name, 'Exiting')

# def my_service():
#     name = multiprocessing.current_process().name
#     print(name, 'Starting')
#     time.sleep(3)
#     print(name, 'Exiting')

# if __name__ == '__main__':
#     service = multiprocessing.Process(name='my_service', target=my_service)
#     worker_1 = multiprocessing.Process(name='worker 1', target=worker)
#     worker_2 = multiprocessing.Process(target=worker) # use default name

#     worker_1.start()
#     worker_2.start()
#     service.start()

import pickle
import random

from train import train
from play import play
from q_connect4_agent import QConnect4Agent

def worker(q_agent_q):
    # print(queue.get())
    # q_agent_q = queue.get()

    q_agent_q.update({((' ', 0, '1'), 3): 0.25})
    print(q_agent_q)


    # queue.put(q_agent_q)

    # print(f"Data: {[v for v in list(q_agent_q.values())[:10]]}")

if __name__ == "__main__":
    alpha = 0.5
    epsilon = 0.5

    q_agent = QConnect4Agent(alpha=alpha, epsilon=epsilon)

    # q_agent.q = pickle.load(open('q_agent_q.pkl', 'rb'))
    # q_agent.q.update(train(q_agent=q_agent, n=1000))

    # queue = multiprocessing.Queue()
    # queue.put(q_agent.q)

    threads = [multiprocessing.Process(name=f"Process {i}", target=worker, args=(q_agent.q,)) for i in range(3)]
    
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(q_agent.q)

    # pickle.dump(q_agent.q, open('q_agent_dict.pkl', 'wb'))


    # play(q_agent=q_agent, human=random.randint(0, 1), helper=False)