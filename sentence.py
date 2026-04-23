import string
import numpy as np
from numpy.typing import NDArray


Gene = np.int16
Sentence = NDArray[Gene]
GENE_VALUES: NDArray[Gene] = np.array([
    *[ord(al) for al in string.ascii_uppercase],
    *[ord(al) for al in string.ascii_lowercase],
    *[ord(al) for al in string.digits],
    *[ord(pl) for pl in "?. "]
], dtype=Gene)
POP_COUNT: int = 100
MAX_GEN_COUNT: int = 100000
DUP_RATE: float = 0.1
MUT_RATE: float = 0.05

def random(rng: np.random.Generator, n: int) -> Sentence:
    return rng.choice(GENE_VALUES, size=n).astype(Gene)

def from_string(s: str) -> Sentence:
    return np.array([ord(ltr) for ltr in s], dtype=Gene)

def update_fitness(pop_matrix: Sentence, target: Sentence) -> Sentence:
    return np.sum(np.abs(pop_matrix - target), axis=1)
    # return np.sum(np.pow(pop_matrix - target, 2), axis=1)

def main():
    rng = np.random.default_rng(20)

    target = from_string("How are you doing . . . Today?")
    pop_matrix = rng.choice(
        GENE_VALUES, size=(POP_COUNT, len(target))).astype(Gene)

    epoch: int = 0
    best_fit: float = np.inf
    best_genome: Sentence = np.array([])
    while best_fit > 0:
        if epoch % 1000 == 0:
            d = ''.join(chr(c) for c in best_genome)
            print(f"[ep. {epoch:7}] '{d}'; fitness = {best_fit}")

        # Compute fitness
        fitness = update_fitness(pop_matrix, target)

        # Sort by fitness
        indices = np.argsort(fitness)
        pop_matrix = pop_matrix[indices]
        fitness = fitness[indices]
        if fitness[0] < best_fit:
            best_genome = pop_matrix[0]
            best_fit = fitness[0]

        # Allocate space for new population
        new_pop_matrix = np.zeros_like(pop_matrix)

        # Duplicate top performers
        dup_count = int(DUP_RATE * POP_COUNT)
        new_pop_matrix[:dup_count] = pop_matrix[:dup_count]

        # Crossover the remaining ones
        for i in range(POP_COUNT - dup_count):
            p1, p2 = rng.choice(pop_matrix[:dup_count + 10],
                size=2, replace=False)
            split = rng.integers(1, len(target) - 1)
            new_pop_matrix[i, :split] = p1[:split]
            new_pop_matrix[i, split:] = p2[split:]

        # Mutate
        mut_mask = rng.random(size=new_pop_matrix.shape) < MUT_RATE
        # # NOTE: To not mutate top_n performer
        top_n = 3
        mut_mask[top_n - 1, :] = False

        # Generate mutation replacement genes for each slot
        random_genes = rng.choice(GENE_VALUES, size=new_pop_matrix.shape)

        pop_matrix = np.where(mut_mask, random_genes, new_pop_matrix)
        epoch += 1

    print(f"Solved in {epoch} epochs! Final: {''.join(chr(c) for c in best_genome)}; fitness = {best_fit}")


if __name__ == "__main__":
    main()
