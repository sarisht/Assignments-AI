:-dynamic(frame/2).
:-dynamic(frame/1).
frame(university, [phone(011686971), address(iitd)]).
frame(department, [a_part_of(university), programme([bTech, mTech, phD])]).
frame(hostel, [a_part_of(university), room(100)]).
frame(faculty, [a_part_of(department), age(25-60), nationality(indian), qual(graduate)]).
frame(student, [a_part_of(department), age(17-25), nationality(indian), qual(undergraduate)]).
frame(satpura, [is_a(hostel), phone(contact_no)]).
frame(computer_science_faculty, [ako(faculty), qual(mSc)]).
frame(saroj_kaushik, [is_a(computer_science_faculty), qual(phD), age(45), address(bharti_iitd)]).
frame(computer_science_student, [ako(student),qual(secondary_school)]).
frame(abhishek_yadav, [is_a(computer_science_student), qual(secondary_school), age(19), address(satpura_iitd)]).
frame(abhishek_yadav,[a_part_of(satpura)]).
frame(sarisht_wadhwa, [is_a(computer_science_student), qual(bTech), age(22), address(satpura_iitd)]).
frame(sarisht_wadhwa,[a_part_of(satpura)]).
frame(machli, [is_a(computer_science_student), qual(secondary_school), age(19), address(satpura_iitd)]).
frame(machli,[a_part_of(satpura)]).

equal(X,X).

find(X,Y):-frame(X,Z),search(Y,Z),!.
find(X,Y):-frame(X,[is_a(Z)|_]),find(Z,Y),!.
find(X,Y):-frame(X,[ako(Z)|_]),find(Z,Y),!.
find(X,Y):-frame(X,[a_part_of(Z)|_]),find(Z,Y),!.

query(X,Y):- find(X,Y),!.
query(X,is_a(Y)):- find(X,is_a(Z)),not(equal(Y,Z)),find(Z,ako(Y)).

search(X,[X|_]).
search(X,[_|R]):-search(X,R).

insert(X,Y) :- assert(frame(X,[Y])).

delete(X) :- frame(Z,[ako(X)|_]),delete(Z),delete(X).
delete(X) :- frame(Z,[is_a(X)|_]),delete(Z),delete(X).
delete(X) :- frame(Z,[a_part_of(X)|_]),delete(Z),delete(X).
delete(X) :- frame(X,_),retract(frame(X,_)).

match(is_a(_),is_a(_)).
match(address(_),address(_)).
match(qual(_),qual(_)).
match(age(_),age(_)).
match(room(_),room(_)).
match(nationality(_),nationality(_)).
match(phone(_),phone(_)).

update(X, L) :- old_prop(X, Y), add_prop(L, Y, Z), retract(frame(X, _)), assert(frame(X, Z)), !.

old_prop(X, Y) :- frame(X, Y), !.
old_prop(_, []).

add_prop([], Y, Y).
add_prop(L, [Y|R], [L|R]):- match(L,Y),!.
add_prop(L, [Y|R], [Y|Z]):- add_prop(L, R, Z).