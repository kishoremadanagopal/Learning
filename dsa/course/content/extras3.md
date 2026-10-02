@@ hash-tables
topics: hash functions, buckets, collisions, separate chaining vs open addressing, load factor and resizing, average O(1) vs worst O(n), hash randomisation, hashable keys, building a hash map
terms:
- **Hash function:** turns a key into a number (its hash); the same key always gives the same hash.
- **Bucket:** a slot in a hash table's internal array where entries are stored.
- **Collision:** two different keys landing in the same bucket.
- **Separate chaining:** handling collisions by keeping a small list of entries in each bucket.
- **Open addressing:** handling collisions by probing other buckets until a free one is found; Python's dict does this.
- **Load factor:** number of entries ÷ number of buckets; higher means more collisions.
- **Resize (rehash):** moving every entry into a bigger table when the load factor gets too high.
- **Hash randomisation:** Python changes string hashes each run, so attackers can't force collisions.
- **frozenset:** an immutable set, usable as a dict key.
mistakes:
- Assuming hash tables are always O(1). It's the average; the worst case is O(n).
- Using a list or dict as a key; convert to a tuple or frozenset.
- In your own hash map, appending a new pair without first checking whether the key exists.
- Relying on set order; only dicts keep insertion order.

@@ hashing-patterns
topics: counting with Counter and dict.get, first unique character, Two Sum with complements, grouping with defaultdict, choosing a key, prefix sums with a hash map, longest consecutive sequence, pattern summary
terms:
- **Frequency count:** how many times each item appears, usually in a dict or Counter.
- **Counter:** a dict subclass from collections that counts items; missing keys count as 0.
- **defaultdict:** a dict that creates a default value (like an empty list) for missing keys.
- **Complement:** the value needed to complete a pair, such as target − x.
- **Grouping key:** a normalised form shared by everything that belongs together, like sorted letters for anagrams.
- **Prefix-sum count:** a dict from each prefix sum to how often it has appeared, used to count subarrays with a given sum.
- **Consecutive sequence:** integers that follow each other without gaps, like 3, 4, 5.
mistakes:
- Storing a number before checking its complement, so it pairs with itself.
- Forgetting `counts = {0: 1}` when counting subarray sums.
- Starting a run count from every number in "longest consecutive", which makes it O(n²).
- Using a sliding window for subarray sums when numbers can be negative.
