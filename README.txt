-----SCTESeeker Notes-----


Description: This application goes through a log file and gets the
lines that include SCTE messages and their corresponding 
break windows.


Instructions:
1. Copy necessary log files to a local drive (for speed)
2. Enter ITX number, choose a log file to search
3. Pick a 2-hour interval in GMT (Greenwich Mean Time)
4. (Optional) Apply filters
5. Click 'Search'


Applying filters:
1. Look for single word or phrase within the messages 
	(not case-sensitive)
2. Filter out by opcodes
3. Filter out by main or backup machines (i.e. 1050A vs 1050B)
4. Click 'Filter'


Color coding:
1. Green corresponds to opcode 1 and 2 messages that are not ignored
2. Yellow corresponds to "TAKE initiated," "Take next sequence,"
	and "AddAuxElements" messages
3. Red corresponds to opcode 3, 4, and 5 messages that are not
	ignored
3. Gray corresponds to opcode 0 messages, ignored messages, and
	miscellaneous messages


To search another log file, just choose the file and search again.


Issues:
- After a filter, the Quickview scrollbar does not reset to the top
	or resize
- Window size is fixed at 800x600 due to difficulties getting boxes to
	automatically fit the window size
- Time interval is limited to 2 hours due to large memory usage