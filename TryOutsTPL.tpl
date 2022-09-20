Proc @trep (
New @variable2,(Num, 5);
New @variable1,(Num, 5);
Values(@variable2, Alter(@variable1, SUB, 3));
);
Proc @proc(
New @variable2,(Num, 3);
New @variable1,(Num, 5);
Values(@variable2, Alter(@variable1, ADD, 3));
);
CALL(@trep);
CALL(@trep);

