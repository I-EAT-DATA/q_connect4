import pickle
import multiprocessing
import random

from train import train
from play import play
from q_connect4_agent import QConnect4Agent

def worker(q_agent):
    updated_q = train(q_agent=q_agent, n=1000)
    q_agent.q.update(updated_q)
    # print("worker: q size: ",len(q_agent.q))
    # shared_q = queue.get()

    # trained_agent = train(n=10, alpha=alpha, epsilon=epsilon)
    # shared_q.update(trained_agent.q)

    # print(f"Length of data: {len(shared_q)}")

    # queue.put(shared_q)
    return(q_agent.q)


def main():
    alpha = 0.5
    epsilon = 0.5

    q_agent = QConnect4Agent(alpha=alpha, epsilon=epsilon)
    try:
        q_agent.q = pickle.load(open('q_agent_dict.pkl', 'rb'))
        print("pkl loaded")
    except:
        print("pkl not loaded")
        pass
    n_cpus = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(n_cpus)

    q = dict()
    for _ in range(2):
        print("len q=", len(q_agent.q))
        qs = [q_agent] * n_cpus
        results = pool.map(worker, qs)
        for i,r in enumerate(results):
            # print(i, "=", len(r))
            q_agent.q.update(r)

    pool.close()
    print("len q=", len(q_agent.q))
    print("Ready To Play")

    pickle.dump(q_agent.q, open('q_agent_dict.pkl', 'wb'))

    play(q_agent=q_agent, human=random.randint(0, 1), helper=True)

if __name__ == "__main__":
    main()

