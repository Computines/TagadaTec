--Primer Script Compilado
Proc @principal (
New @levels, (Bool, true);
New @control, (Num, 0);
While @control < 2(
Case When IsTrue(@levels) Then
(
CALL (@medium);
AlterB(@levels);
)
Else
(
CALL (@easy);
CALL (@hard);
);
Values (@control, Alter(@control, ADD, 1));
);
);

Proc @easy (
New @control, (Num, 0);
While @control < 4(
Case @control 
When 1 Then 
(MoveRight;)
When 2 Then 
(MoveLeft;)
When 3 Then 
(MoveRight;);
Values(@control, Alter(@control, ADD, 1));
);
);

Proc @medium(
--this is medium risk
New @hits, (Num, 0);
Until (
MoveRight;
Hammer(N);
MoveLeft;
Hammer(S);
Values(@hits, Alter(@hits, ADD, 1));
) @hits < 2 ;
);

Proc @hard (
Repeat(
Hammer(N);
Hammer(O);
MoveRight;
Hammer(E);
Hammer(S);
MoveLeft;
Break;
);
);

CALL (@principal);









