# Locality Sensitive Hashing
>[!question] What is LSH and why do we need it?
> >[!answer] Comparing every document to another one to find similarity is a difficult task and may require $O(N^2)$ computation. As documents grow large, this gets extremely difficult

Hence, we use LSH. 
The ***LSH*** framework ->
```
Documents → Shingling → MinHash Signatures → LSH Buckets → Candidate Pairs
```
***Core Intuition:***
LSH is a technique that hashes similar items into the same "buckets" with high probability. Unlike traditional hash functions (designed to minimize collisions), LSH *maximizes* collisions for similar items.
***Key Properties of LSH:***
1. Similar items have high probability of same hash
2. Dissimilar items have low probability of same hash
3. Hashing is much faster than pairwise comparison
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

### Code 
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

### Jaccard Similarity
-> The Jaccard similarity between two sets corresponds to the probability of a randomly selected element from the union of the sets also being in the intersection.
$set_1$ and $set_2$ 
$$Similarity = \frac{|set_1 \cup set_2|}{|set_1 \cap set_2 |}$$

>[!info] In our code in ***lab4*** we combine all shingles into an array and then calculate jaccard similarity. This is not necessarily needed but it is used to capture different levels of textual granularity.
## MinHash
>[!important] MinHash basically allows us to represent each ***set of shingles*** as a signature. A set of shingles is the array we get when we do character or token-shingling.
>

-> This idea is based on probability and the idea of ***Jaccard Similarity***.
$$ P[min(π(A)) = min(π(B))] = Jaccard(A, B) $$
where $\pi$ is any random permutation of the universal set.

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

### The Error
$SE ≈ √(J(1-J)/k)$ - J is jaccard and K is number of Hashes
#### Solved Example
Suppose our global list of shingles is: `{a, b, c, d}`.
- **Doc 1** has shingles: `{a, c}`
- **Doc 2** has shingles: `{b, c}`
Now, let's say we "shuffle" the list and the new random order is: `(b, a, d, c)`.
1. We look at **Doc 1** (`a, c`). In our shuffled list `(b, a, d, c)`, which of Doc 1's shingles appears **first**?
2. We look at **Doc 2** (`b, c`). In our shuffled list `(b, a, d, c)`, which of Doc 2's shingles appears **first**?
>[!answer] a for doc 1 and b for doc 2

-> This doesn't result in a match. However, if we perform **many** different random shuffles, the probability that the MinHash values for two documents are the same is **exactly equal** to their Jaccard Similarity.
-> now performing many different random shuffles is difficult, hence, we use ***hash functions***

---
Suppose we have two hash functions:
1. $h_1(x) = (x + 1) \mod 4$
2. $h_2(x) = (3x + 1) \mod 4$
we map the shingles to numbers so `{a,b,c,d}` = `{0,1,2,3}`
-> ***Hashing For Document 1***:
	`{a,c}` =`{0,2}` -> hashed -> `{(0+1) mod 4, (2+1) mod 4}` = `{1,3}`
	`{a,c}` =`{0,2}` -> hashed -> `{(3(0)+1) mod 4, (3(2)+1) mod 4}` = `{1,3}`
	-> we will take the minimum for each hash, hence it'll be `{1,1}`
-> ***Hashing For Document 1***:
	`{b,c}` =`{1,2}` -> hashed -> `{(1+1) mod 4, (2+1) mod 4}` = `{2,3}`
	`{b,c}` =`{1,2}` -> hashed -> `{(3(1)+1) mod 4, (3(2)+1) mod 4}` = `{0,3}`
	-> we will take the minimum for each hash, hence it'll be `{2,0}`
-> ***Final Similarity Score for Doc 1 and Doc 2***
	$Doc1_{Hash}$ = `{1,1}`
	$Doc2_{Hash}$ = `{2,0}`

---
***Final Similarity check***
-> We compare the value of signature at doc1[x] = value of signature at doc2[x] where `X is in range(len(doc))`
$Doc1_{Hash}$  does not match $Doc2_{Hash}$ at any position, hence the similarity is 0, but this only a lucky miss, that is why we use a 100 different hash functions.
#### Final Algorithm Steps
##### Step 1: Shingling (The Set Creation) 🧱
Convert your raw text into a set of unique items.
- **Action**: Break the document into "shingles" (k-length sequences of characters or words).
- **Result**: Each document is represented as a **set** of strings.
    > _Example_: For $k=3$, "fly free" becomes `{"fly", "ly ", "y f", " fr", "fre", "ree"}`.
##### Step 2: Mapping to Integers 🔢
Since computers process numbers faster than strings, we map our shingles to a numerical space.
- **Action**: Use a hash function (like **MD5**) to turn each string shingle into a unique integer ID.
- **Code logic**: `int(hashlib.md5(element.encode()).hexdigest(), 16) % max_hash`
##### Step 3: Generating Hash Functions (The Shuffling) 🔄
Instead of literally shuffling all possible shingles (which could be millions), we simulate shuffles using **$n$ different hash functions**.
- **Action**: Create a series of functions $h_1(x), h_2(x), \dots, h_n(x)$.
- **Purpose**: Each function provides a different "randomized order" of your shingle IDs.
##### Step 4: MinHashing (The Signature Creation) ✍️
This is where we compress the large sets into small signatures.
- **Action**: For **each** hash function, apply it to **every** shingle in the document and keep only the **minimum** result.
- **Result**: A **Signature** (an array/vector of numbers). 
    > _Example_: If you use 100 hash functions, your document is now represented by only 100 numbers, regardless of how long the original document was.
##### Step 5: Similarity Estimation 🏁
Calculate how similar the documents are by comparing their condensed signatures.
- **Action**: Compare the signatures index-by-index.
- **Logic**: Count how many slots are identical and divide by the total number of slots.
- **Formula**:$$J(A, B) \approx \frac{\text{Matches}}{\text{Total Hash Functions}}$$

- **Code logic**: `np.mean(sig1 == sig2)`
##### 💡 Why does it work?
The **MinHash Property** states that:
> The probability that the minimum hash value for two sets is identical is exactly equal to their **Jaccard Similarity**:
> 
> $$P[\min(\pi(A)) = \min(\pi(B))] = J(A, B)$$