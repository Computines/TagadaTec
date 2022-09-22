--Yolo
Proc @principal(
New @var1, (Num, 1);
New @var2, (Num, 2);
New @var3, (Num, 3);
New @var4, (Num, 4);
New @varT, (Bool, true);
New @varF, (Bool, false);
Repeat(
New @variable1, (Num, 5);
MoveLeft;
MoveRight;
Break;
);

Until(
MoveLeft;
MoveRight;
-- Aumenta en 1 a la variable;
Values (@variable1, Alter (@variable1, ADD, 1));
)@variable1 > 10;

While IsTrue(@varT)(
MoveLeft;
MoveRight;
-- Cambia variable a False;
AlterB (@varT);
);

Case When ( @var1 > 2) Then (
MoveLeft;
MoveRight;
);

Case When IsTrue(@varT) Then (
MoveLeft;
MoveRight;
) Else ( 
MoveLeft;
MoveLeft;
);

Case @variable1
 When 1 Then
 ( MoveLeft;)
 When 2 Then
 ( MoveRight;)
 When 3 Then
 ( MoveLeft;);


Case @varF
 When true Then
 ( MoveLeft;)
 Else
 ( MoveRight;);

);














