import numpy as np
from generate_chain import generate_closed_chain, chain_to_JSON, is_self_intersecting
# The length of every polymer is the same: we will use three experimental
# cases: N = 20, 40, 60, and 80
N = 10
trials = 100

if __name__ == "__main__":
    all_attempts = np.empty(trials)
    for i in np.arange(trials):
        print("generating a closed chain...")
        chain = generate_closed_chain(N)
        if is_self_intersecting(chain[0]):
            print("There is a self-intersection! That's a bug")
        num_attempts = chain[1]
        chain_to_JSON(chain[0])
        print("trial " + str(i+1) + " took " + str(num_attempts) + " attempts")
        all_attempts[i] = num_attempts

    average_attempts = np.sum(all_attempts) / all_attempts.size

    print("\nAverage number of attempts was: {}".format(average_attempts))