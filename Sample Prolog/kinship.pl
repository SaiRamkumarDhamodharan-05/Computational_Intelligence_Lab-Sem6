male(motilal_nehru).
male(jawaharlal_nehru).
male(feroze_gandhi).
male(rajiv_gandhi).
male(sanjay_gandhi).
male(rahul_gandhi).
male(varun_gandhi).
male(robert_vadra).
male(raihan_vadra).
female(swarup_rani_nehru).
female(kamala_nehru).
female(indira_gandhi).
female(sonia_gandhi).
female(maneka_gandhi).
female(priyanka_gandhi).
female(miraya_vadra).
female(vijaya_lakshmi_pandit).
female(krishna_hutheesing).
married(motilal_nehru, swarup_rani_nehru).
married(jawaharlal_nehru, kamala_nehru).
married(feroze_gandhi, indira_gandhi).
married(rajiv_gandhi, sonia_gandhi).
married(sanjay_gandhi, maneka_gandhi).
married(robert_vadra, priyanka_gandhi).
spouse(X, Y) :- married(X, Y).
spouse(X, Y) :- married(Y, X).
parent(motilal_nehru, jawaharlal_nehru).
parent(swarup_rani_nehru, jawaharlal_nehru).
parent(motilal_nehru, vijaya_lakshmi_pandit).
parent(swarup_rani_nehru, vijaya_lakshmi_pandit).
parent(motilal_nehru, krishna_hutheesing).
parent(swarup_rani_nehru, krishna_hutheesing).
parent(jawaharlal_nehru, indira_gandhi).
parent(kamala_nehru, indira_gandhi).
parent(indira_gandhi, rajiv_gandhi).
parent(feroze_gandhi, rajiv_gandhi).
parent(indira_gandhi, sanjay_gandhi).
parent(feroze_gandhi, sanjay_gandhi).
parent(rajiv_gandhi, rahul_gandhi).
parent(sonia_gandhi, rahul_gandhi).
parent(rajiv_gandhi, priyanka_gandhi).
parent(sonia_gandhi, priyanka_gandhi).
parent(sanjay_gandhi, varun_gandhi).
parent(maneka_gandhi, varun_gandhi).
parent(priyanka_gandhi, raihan_vadra).
parent(robert_vadra, raihan_vadra).
parent(priyanka_gandhi, miraya_vadra).
parent(robert_vadra, miraya_vadra).
father(F, C) :- parent(F, C), male(F).
mother(M, C) :- parent(M, C), female(M).
sibling(X, Y) :-
    parent(P, X),
    parent(P, Y),
    X \= Y.
brother(B, X) :- sibling(B, X), male(B).
sister(S, X) :- sibling(S, X), female(S).
uncle(U, C) :-
    parent(P, C),
    brother(U, P).
aunt(A, C) :-
    parent(P, C),
    sister(A, P).
grandparent(GP, C) :-
    parent(GP, P),
    parent(P, C).
grandfather(GF, C) :- grandparent(GF, C), male(GF).
grandmother(GM, C) :- grandparent(GM, C), female(GM).

OUTPUT:
?- father(F, rahul_gandhi).
F = rajiv_gandhi .

?- sibling(S, rajiv_gandhi).
S = sanjay_gandhi .

?- uncle(U,raihan_vadra).
U = rahul_gandhi .

?- spouse(motilal_nehru, swarup_rani_nehru).
true .

?- grandparent(GP, priyanka_gandhi).
GP = indira_gandhi ;
GP = feroze_gandhi .

?- uncle(sanjay_gandhi,raihan_vadra).
false.

?- aunt(A,raihan_vadra).
false.