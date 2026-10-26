import random
from contestants import Contestant, GroupedContestants

def main():
    cs = GroupedContestants()
    cs.add([Contestant(i) for i in range(10)])

    while len(cs.get_living()) > 1:
        random.choice(cs.get_living()).take_damage(10)
        print(cs)

if __name__ == "__main__":
    main()