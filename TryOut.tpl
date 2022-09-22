--YOlo

Proc @trep (
New @variable2,(Num, 5);
New @variable1,(Num, 5);
New @fium, (Num, 2);
Values(@variable2, Alter(@fium, SUB, 3));
PrintValues(@variable2);
);

Proc @proc(
New @variable2,(Num, 3);
New @variable1,(Num, 5);
New @trululu, (Num, 5);
Values(@variable2, Alter(@trululu, ADD, 3));
);

Proc @principal(
New @bool, (Bool, true);
New @trululu,(Num, 3);
New @fium,(Num, 5);
Values(@trululu, Alter(@fium, ADD, 3));
CALL(@trep);
CALL(@proc);
);

CALL (@principal);


