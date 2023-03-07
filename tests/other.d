LeGo_Init(LeGo_Focusname);
func void MEM_SendToSpy(var int errorType, var string text) {};
MEM_SendToSpy(1, "a");
CALL_TEST_WORKING(111);
call_test_notworking(222);