import numpy as np
from .generate_chain import generate_closed_chain, chain_to_JSON, is_self_intersecting

# The length of every polymer is the same: we will use three experimental
# cases: N = 20, 40, 60, and 80

N = 10

print("generating a closed chain...")
chain = generate_closed_chain(N)
if is_self_intersecting(chain[0]):
    print("That's a self-intersection!")
num_attempts = chain[1]
chain_to_JSON(chain[0])
print("\nNumber of attempts was: {}".format(num_attempts))
