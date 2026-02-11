### Architecture Spark
![[Pasted image 20260121112925.png]]
It basically works on a master-slave architecture where we have a driver program which is called a **Spark Context**

### Components
1. **Driver Program:** The main program that creates the SparkContext and coordinates the execution 
2.  **SparkContext:** The entry point to Spark functionality, connects to the cluster 
3. **Cluster Manager:** Allocates resources across applications (YARN, Mesos, Kubernetes, or standalone) 
4. **Executors:** Processes that run on worker nodes, execute tasks and store data

## RDD (Resilient Distributed Data Storage)
Key Properties of RDDs: 
- **Resilient:** Can recover from node failures through lineage 
- **Distributed:** Data is distributed across multiple nodes in the cluster 
- **Dataset:** Collection of partitioned data with primitive values or custom objects

Immutable and Lazy, aka they can't be changed and data is only transformed if an action is performed

| **Transformation**  | **Description**                                                                                                                                               |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `map(func)`         | Applies a function to each element of the RDD and returns a new RDD.                                                                                          |
| `filter(func)`      | Returns a new RDD containing only the elements that satisfy the predicate.                                                                                    |
| `flatMap(func)`     | Similar to `map`, but each input item can be mapped to 0 or more output items (flattens the result).                                                          |
| `distinct()`        | Returns a new RDD containing only the unique elements of the source RDD.                                                                                      |
| `reduceByKey(func)` | When called on a dataset of $(K, V)$ pairs, returns a dataset of $(K, V)$ pairs where the values for each key are aggregated using the given reduce function. |
| `groupByKey()`      | Groups all values associated with the same key into a single sequence.                                                                                        |
| `sortBy(func)`      | Returns an RDD sorted by the given function.                                                                                                                  |

| **Action**             | **Description**                                                                                                                                                                                                 |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `collect()`            | Returns all elements of the RDD to the driver program as an array. It returns all the elements as a ***row()*** which is a built-in  (Use with caution on large datasets as it loads all the data into memory!) |
| `count()`              | Returns the total number of elements in the RDD.                                                                                                                                                                |
| `first()`              | Returns the first element of the RDD.                                                                                                                                                                           |
| `take(n)`              | Returns an array containing the first $n$ elements of the RDD.                                                                                                                                                  |
| `reduce(func)`         | Aggregates the elements of the RDD using a function (which takes two arguments and returns one).                                                                                                                |
| `saveAsTextFile(path)` | Writes the elements of the dataset as a text file in a given directory in the local filesystem, HDFS, or any other Hadoop-supported file system.                                                                |
Since computation is lazy, the commands don't execute immediately. Instead sparks builds a DAG (Directed Acyclic Graph) of transformations. Hence, computation happens when an action is called. 
This enables us to do three things:
1. Optimize execution plan
2. Reduce unnecessary computation
3. Enables fault tolerance

> [!info] Before starting we need to establish a spark session

```
# Create a SparkSession configured for data preprocessing
spark = SparkSession.builder \
    .appName("SCC454-DataPreprocessing") \
    .config("spark.driver.memory", "4g") \
    .config("spark.sql.legacy.timeParserPolicy", "LEGACY") \
    .config("spark.ui.port", "4050") \
    .getOrCreate()

# Get the underlying SparkContext
sc = spark.sparkContext
```

## 1.3 Overview of Spark's Data Cleaning Capabilities

Spark provides several modules and functions for data preprocessing:

**Key Modules:**
- `pyspark.sql.functions`: Built-in functions for transformations
- `pyspark.sql.types`: Data type definitions
- `pyspark.ml.feature`: Feature engineering tools

**Important Function Categories:**

| Category         | Functions                                             |
| ---------------- | ----------------------------------------------------- |
| Null Handling    | `isNull()`, `isNotNull()`, `na.drop()`, `na.fill()`   |
| String Functions | `lower()`, `upper()`, `trim()`, `split()`, `concat()` |
| Regex Functions  | `regexp_extract()`, `regexp_replace()`, `rlike()`     |
| Type Conversion  | `cast()`, `to_date()`, `to_timestamp()`               |
| Aggregation      | `count()`, `avg()`, `sum()`, `mean()`                 |
| Conditional      | `when()`, `otherwise()`, `coalesce()`                 |
>[!important] Both Dataframes and RDDs in spark are immutable.

## (Un) Common Spark Functions 

| Function                        | What it does                                                                                                |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `concat_ws(separator,*columns)` | Concatenates multiple input string columns together into a single string column, using the given separator. |
| `explode(col,column)`           | takes an array column and turns each element into a row                                                     |
| `lit(value)`                    | literal value                                                                                               |
| `substring(value)`              | basically same as normal substring                                                                          |
| `array_distinct(array)`         | takes a single array and keeps distinct only                                                                |
| `array_union(arrays)`           | takes multiple arrays and keeps all the values                                                              |
| `broadcast(value)`              | sends a value to all clusters                                                                               |


## Regex
| Pattern | Meaning            |
| ------- | ------------------ |
| `\d`    | Any digit (0-9)    |
| `\w`    | Any word character |
| `\s`    | Any whitespace     |
| `.`     | Any character      |
| `*`     | Zero or more       |
| `+`     | One or more        |
| `[]`    | Character class    |
| `()`    | Capture group      |

