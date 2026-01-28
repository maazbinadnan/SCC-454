Why Pandas isn't enough
- **Single-threaded execution:** pandas uses only one CPU core for computations. On modern machines with 4, 8, or even more cores, this means leaving significant processing power unused. 
- **In-memory requirement:** The entire dataset must fit in RAM. A general rule is that you need 5 10x the dataset size in available RAM to work comfortably with pandas. 
- **No lazy evaluation:** Every operation executes immediately. When you chain multiple operations, each one processes the entire dataset before moving to the next. 
- **Scaling challenges:** As your data grows from megabytes to gigabytes, pandas operations become increasingly slow, and you may run out of memory entirely.
Hence, we use Modin, which parallelizes all tasks by splitting your data based on how many cores and then joins it.