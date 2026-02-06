```
# Method 1: Using Spark's NGram transformer

def create_shingle_pipeline(n_values=[2, 3, 4]):

    """Create a pipeline for generating word n-grams of multiple sizes."""

    from pyspark.sql.functions import concat_ws, flatten

  

    # Tokenizer

    tokenizer = Tokenizer(inputCol="text_clean", outputCol="words")

  

    # Create NGram transformers for each n

    ngram_transformers = []

    for n in n_values:

        ngram = NGram(n=n, inputCol="words", outputCol=f"ngrams_{n}")

        ngram_transformers.append(ngram)

  

    return tokenizer, ngram_transformers
```

In PySpark, different transformers expect different "Data Types":
- **`Tokenizer`** expects a **String**.
- **`NGram`** expects an **Array of Strings** (a list of words).
If you pass a raw string directly into an `NGram`, the code will throw an error because it doesn't see a list of individual elements to "slide" its window across.

## Shingling 
-> Shingling essentially uses a sliding window logic. In this, we can define the window and it converts word into shingles or **`Grams`** of text  
***What is Shingling?***
Shingling converts documents into sets of contiguous subsequences (shingles). This allows us to measure document similarity by comparing these sets.
**Types of Shingles:**

| Type                       | Description                            | Example (Input: "hello world")                    |
| :------------------------- | :------------------------------------- | :------------------------------------------------ |
| **Character $k$-shingles** | Contiguous sequences of $k$ characters | $k=3$: `{"hel", "ell", "llo", "lo ", "o w", ...}` |
| **Word $n$-grams**         | Contiguous sequences of $n$ words      | $n=2$: `{"hello world"}`                          |

**Choosing Shingle Size:**
- Too small: High overlap even for dissimilar documents
- Too large: Low overlap even for similar documents
- ***Rule of thumb: k=5-9 for characters, n=2-4 for words***

### Jaccard Similarity
-> The Jaccard similarity between two sets corresponds to the probability of a randomly selected element from the union of the sets also being in the intersection.
$set_1$ and $set_2$
$$Similarity = \frac{|set_1 \cup set_2|}{|set_1 \cap set_2 |}$$
## MinHash
-> This idea is based on probability and the idea of ***Jaccard Similarity***.

Suppose you have a huge corpus of text and a lot of shingles. Comparing each of them to each other would take a loooooong time. 

So we basically first, shuffle the dataset.
### The Shuffle 🔀
The `MinHasher` doesn't just hash once. It uses 200 different "recipes" (coefficients $a$ and $b$) to create 200 different ways of numbering the shingles.
Imagine each hash function creates a different **random permutation** (order) of all possible shingles.
- **Hash 1** might decide "apple" is #1 and "zebra" is #500.
- **Hash 2** might decide "zebra" is #2 and "apple" is #900.
By using 200 different hash functions, we are essentially running 200 independent experiments
### The "Min" 📉
For a single document, we take all its shingles and run them through **Hash 1**. We look at all the resulting numbers and pick the **smallest one**. Then we do the same for **Hash 2**, and so on, until we have 200 "winners." 🏆

|**Shingle**|**Hash 1 Value**|**Hash 2 Value**|
|---|---|---|
|"the cat"|452|**12**|
|"cat sat"|**105**|889|
|"sat on"|600|234|
|**Winner (Min)**|**105**|**12**|
So the minimum or the ***smallest*** list is the signature.
