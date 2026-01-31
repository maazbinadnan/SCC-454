### Pre-processing
Transforming raw data into understandable format. Data should be:
1. Correct
2. Consistent: e.g units being used

>[!important] always backup the raw data and organize files logically

>[!important]  Delimiter character may be present in the row itself, hence we should try to break the column with that delimiter.

##### Dates
what format to use in date? is it local or based on some international rule

###  How/When to Address pre-processing issues?
1. **Pre - Ingestion:** perform pre-processing before uploading to database, its potentially quicker but is more complex and might have scaling issues
2. **Post- Ingestion:** Where you upload data into database and then fix it, its potentially easier to spot the problems, however has resource and computational constraints

####  Good Practice
Start with small samples first 
• Automate checks once you know what to look for 
• Script your pre-processing steps for reproducibility

#### Pearson Correlation
-> The values depends on the domain itself,

### Different Databases
![[Pasted image 20260130144221.png]]



