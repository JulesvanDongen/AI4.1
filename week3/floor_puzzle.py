import itertools

num_floors = 5
floors = range(num_floors)

def hopper_constraint(hopper, kay, liskov, perlis, ritchie):
    return hopper != num_floors - 1

def kay_constraint(hopper, kay, liskov, perlis, ritchie):
    return kay != 0

def liskov_constraint(hopper, kay, liskov, perlis, ritchie):
    return liskov != num_floors - 1 and liskov != 0 and not (liskov == kay + 1 or liskov == kay - 1)

def perlis_constraint(hopper, kay, liskov, perlis, ritchie):
    return perlis > kay

def ritchie_constraint(hopper, kay, liskov, perlis, ritchie):
    return not (ritchie == liskov + 1 or ritchie == liskov - 1)

for (H, K, L, P, R) in list(itertools.permutations(floors)):
    constraints = [
        hopper_constraint,
        kay_constraint,
        liskov_constraint,
        perlis_constraint,
        ritchie_constraint
    ]

    satisfies_constraints = True
    for constraint in constraints:
        satisfies_constraints = satisfies_constraints and constraint(H,K,L,P,R)

    if satisfies_constraints:
        print(f"Possible permutation: Hopper: {H}, Kay: {K}, Liskov: {L}, Perlis: {P}, Ritchie: {R}")