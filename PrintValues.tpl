--Yolo
Proc @principal (
	New @var1, (Num, 4);
	New @var2, (Num, 2);
	Values (@var1, Alter (@var2, ADD, 1));
	PrintValues ([hola], @var1, [lol], @var3);
);
CALL(@principal);







