
>[!info] this drops ROWS based on the how we want to drop them

```
(df).na.drop(how=["any","all"])
```

>[!info] show shows the column and its values

```
df.select(col(c)).show()
```

In Apache Spark, especially when using **PySpark**, functions like `count()`, `when()`, `isnan()`, and others are part of the **`pyspark.sql.functions`** module, which provides a collection of functions that can be used to perform a variety of operations on DataFrame columns. These functions follow a **functional programming** style, where operations are expressed in terms of applying functions to DataFrame columns or expressions.

Here’s a breakdown of the syntax and usage for the specific functions in your example:

### 1. **`count()`**:

* **Purpose**: This is an aggregate function that counts the number of non-null values in a column or expression.
* **Syntax**:

  ```python
  from pyspark.sql import functions as F

  F.count(col)
  ```
* **Example**:

  ```python
  df_customers.select(F.count("age")).show()
  ```

### 2. **`when()`**:

* **Purpose**: This is a conditional function that returns a value if a condition is met, otherwise, it returns `null`.
* **Syntax**:

  ```python
  from pyspark.sql import functions as F

  F.when(condition, value)
  ```
* **Example**:

  ```python
  df_customers.select(F.when(df_customers.age > 18, "Adult").otherwise("Minor")).show()
  ```

### 3. **`isnan()`**:

* **Purpose**: This function checks whether the values in a column are `NaN` (Not a Number). It returns `True` for `NaN` values and `False` for other values.
* **Syntax**:

  ```python
  from pyspark.sql import functions as F

  F.isnan(col)
  ```
* **Example**:

  ```python
  df_customers.select(F.isnan(df_customers.age)).show()
  ```

### 4. **`alias()`**:

* **Purpose**: This function is used to rename a column or expression in a query, making the result more readable.
* **Syntax**:

  ```python
  col.alias("new_name")
  ```
* **Example**:

  ```python
  df_customers.select(F.count("age").alias("age_count")).show()
  ```

### 5. **`select()`**:

* **Purpose**: This is used to project (select) specific columns or expressions in a DataFrame.
* **Syntax**:

  ```python
  DataFrame.select(*cols)
  ```
* The `*cols` unpacks a list or multiple arguments, so you can pass expressions like functions applied to columns.
* **Example**:

  ```python
  df_customers.select("name", "age").show()
  ```

### 6. **`show()`**:

* **Purpose**: This function is used to display the first `n` rows of the DataFrame in a tabular format.
* **Syntax**:

  ```python
  DataFrame.show(n=20, truncate=True)
  ```
* `n`: The number of rows to display (default is 20).
* `truncate`: If `True`, truncates the column values to 20 characters for display. Set to `False` to show full content.
* **Example**:

  ```python
  df_customers.show(10)
  ```

### Syntax Flow in Your Case:

Here’s the **syntax flow** for your example:

```python
df_customers.select(
    *[F.count(F.when(F.isnan(c), c)).alias(c + '_nan_count') for c in df_customers.columns]
).show()
```

* **`df_customers.select()`**: Selects one or more columns/expressions for the DataFrame.
* **`[F.count(F.when(F.isnan(c), c)).alias(c + '_nan_count') for c in df_customers.columns]`**:

  * For each column `c` in `df_customers.columns`, apply the following operations:

    * **`F.isnan(c)`**: Checks if the value in column `c` is NaN.
    * **`F.when(F.isnan(c), c)`**: If the value is NaN, return `c`, otherwise `null`.
    * **`F.count()`**: Count the number of non-null (i.e., NaN) values.
    * **`.alias(c + '_nan_count')`**: Rename the resulting column to indicate that it represents the count of NaN values for that column.
* **`.show()`**: Displays the results.

### Function Categories in Spark:

1. **Aggregation Functions**: These operate on one or more columns to summarize data (e.g., `count()`, `sum()`, `avg()`, `min()`, `max()`, etc.).

   * **Examples**:

     ```python
     F.avg("column_name")
     F.min("column_name")
     F.max("column_name")
     ```

2. **Conditional Functions**: These apply conditions to columns (e.g., `when()`, `otherwise()`, `coalesce()`, `ifnull()`).

   * **Examples**:

     ```python
     F.when(df.age > 18, "Adult").otherwise("Minor")
     ```

3. **String Functions**: These are used for manipulating string data (e.g., `concat()`, `length()`, `substring()`, `lower()`, `upper()`).

   * **Examples**:

     ```python
     F.concat("first_name", "last_name")
     F.length("name")
     ```

4. **Math Functions**: These are used for mathematical operations (e.g., `abs()`, `round()`, `sqrt()`, `log()`, `pow()`).

   * **Examples**:

     ```python
     F.abs("column_name")
     F.round("column_name", 2)
     ```

5. **Date/Time Functions**: These allow for operations on date and time columns (e.g., `current_date()`, `year()`, `month()`, `datediff()`).

   * **Examples**:

     ```python
     F.current_date()
     F.year("date_column")
     ```

6. **Window Functions**: These perform operations over a "window" of rows, often used with `groupBy()` (e.g., `row_number()`, `rank()`, `lead()`, `lag()`).

   * **Example**:

     ```python
     from pyspark.sql.window import Window
     windowSpec = Window.partitionBy("column_name").orderBy("date_column")
     df_customers.withColumn("row_number", F.row_number().over(windowSpec))
     ```



### Conclusion:

Spark's function syntax is designed to be expressive, with most functions taking column expressions (or combinations of them) as arguments. By chaining these functions together, you can perform complex operations on your data in a very readable and efficient manner. Let me know if you'd like to explore any of these functions further!
