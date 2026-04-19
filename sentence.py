import string
import numpy as np
from numpy.typing import NDArray

class Sentence:
    GENE_VALUES: NDArray[np.int16] = np.array([
        # *string.ascii_lowercase, *string.digits, ' '
        *[ord(al) for al in string.ascii_lowercase],
        ord(' ')
    ], dtype=np.int16)

    def __init__(self, sent: NDArray[np.int16]) -> None:
        self.letters: NDArray[np.int16] = sent
        self.fitness: float = float("inf")

    def __str__(self):
        return ''.join([chr(lt) for lt in self.letters])

    def __repr__(self):
        return f"'{str(self)}'; fitness = {self.fitness}"

    @classmethod
    def random(cls, rng: np.random.Generator, n: int) -> 'Sentence':
        return cls(np.array(
            rng.choice(Sentence.GENE_VALUES, size=n), dtype=np.int16))

    @classmethod
    def from_string(cls, s: str) -> 'Sentence':
        out = []
        for ltr in s:
            # if ltr not in Sentence.GENE_VALUES:
            #     raise ValueError(f"Char '{ltr}' is not a valid value")

            out.append(ord(ltr))

        return cls(np.array(out, dtype=np.int16))

    @property
    def length(self) -> int: return len(self.letters)

    def update_fitness(self, target: 'Sentence') -> None:
        self.fitness = np.sum(np.abs(self.letters - target.letters))

POP_COUNT: int = 50
GENOME_LEN: int = 20
MAX_GEN_COUNT: int = 100000
DUP_RATE: float = 0.05
MUT_RATE: float = 0.9

def main():
    rng = np.random.default_rng(20)

    target = Sentence.from_string("what you doing today")
    pop: list[Sentence] = [
        Sentence.random(rng, GENOME_LEN) for _ in range(POP_COUNT)]

    for indiv in pop: indiv.update_fitness(target)

    epoch: int = 0
    best_str = ""
    best_fit: float = float("inf")
    while best_fit:
        # print(f"In epoch {epoch}")
        if epoch % 1000 == 0:
            print(f"[ep. {epoch:7}] '{best_str}'; best = {best_fit}")

        pop.sort(key=lambda s: s.fitness)
        if pop[0].fitness < best_fit:
            best_str = str(pop[0])
            best_fit = pop[0].fitness

        # Duplicate top 30% into next generation
        new_pop: list[Sentence] = [Sentence.from_string(best_str)]
        dup_count = int(DUP_RATE * len(pop)) - 1
        for i in range(dup_count):
            new_pop.append(pop[i])

        # Crossover to get sentences for the remaining slots
        for indA in range(dup_count + 1, len(pop)):
            # NOTE: indB might potentially be equal to indA, which is fine
            # for now
            indB = np.random.randint(dup_count, len(pop) - 1)
            # pA_fitness = pop[indA].calc_fitness(target)
            # pB_fitness = pop[indB].calc_fitness(target)
            # split_point = random.randint(4, 16)
            split_point = int(len(pop[indA].letters) / 2)

            new_pop.append(Sentence(np.concatenate((
                pop[indA].letters[:split_point],
                pop[indB].letters[split_point:]
            ))))

        # Mutate
        for sent in new_pop:
            for i in range(sent.length):
                if np.random.random() < MUT_RATE:
                    sent.letters[i] = np.random.choice(Sentence.GENE_VALUES)

        # Replace old population with new one
        pop = new_pop
        print("len(pop) =", len(pop))
        for indiv in pop: indiv.update_fitness(target)

        epoch += 1


    print("---------------------")

    # Print out the best after the evolution process
    pop = sorted(pop, key=lambda s: s.fitness, reverse=False)
    print(f"Last best string : {pop[0]}")
    print(f"Last best fitness: {pop[0].fitness}\n")

    print(f"Best best string : {best_str}")
    print(f"Best best fitness: {best_fit}\n")



if __name__ == "__main__":
    main()
