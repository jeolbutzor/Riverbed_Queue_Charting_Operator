# Riverbed Queue Charting Operator
This repo hosts files that allow Riverbed AppInternals v9 TTW to group transactions by queue.

To implement:
1) Copy both files to the /<TTW_Data_Dir>/operators directory.  You do not have to restart the TTW for the changes to take effect.  
2) Refresh the browser you are using to search, and you will be able to use the operator
3) Use the operator as part of a search, to make sure it works. Example search: 'server=myserver.company.com' | transactioncount_queue

Note: This script/code was written by Riverbed/OpNet - full credit goes to Riverbed and OpNet, and will only work with Riverbed AppInternals version 9.X. The changes I made were very minor, and run using the example script provided by Riverbed.
