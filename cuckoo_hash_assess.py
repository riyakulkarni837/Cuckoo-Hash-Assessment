# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List, Optional

class CuckooHash24:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.bucket_size = 4
		self.CYCLE_THRESHOLD = 10

		self.table_size = init_size
		self.table = [None]*self.table_size

	def get_rand_bucket_index(self, bucket_idx: int) -> int:
		# you must use this function when you need to evict a random key from a bucket. this function
		# randomly chooses an index from a given cell index. this ensures that the random
		# index chosen by your code and our test script match.
		#
		# for example, if you need to remove a random element from the bucket at table index 5,
		# you will call get_rand_bucket_index(5) to determine which key from that bucket to evict, i.e. if get_random_bucket_index(5) returns 2, you
		# will evict the key at index 2 in that bucket.
		rand.seed(int(str(bucket_idx)))
		return rand.randint(0, self.bucket_size-1)

	def hash_func(self, key: int, func_id: int) -> int:
		# access h0 via func_id=0, access h1 via func_id=1
		key = int(str(key) + str(self.__num_rehashes) + str(func_id))
		rand.seed(key)
		result = rand.randint(0, self.table_size-1)
		return result

	def get_table_contents(self) -> List[Optional[List[int]]]:
		# the buckets should be implemented as lists. Table cells with no elements should still have None entries.
		return self.table

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.

    def insert(self, key: int) -> bool:
        table_id = 0
        for _ in range(self.CYCLE_THRESHOLD + 1):
        
        bucket_idx = self.hash_func(key, table_id)
        
        bucket = self.tables[table_id][bucket_idx]

    
        if bucket is None:
            self.tables[table_id][bucket_idx] = [key]
            return True
        
        elif len(bucket) < self.bucket_size:
            bucket.append(key)
            return True
    
        else:
            
            if (self.tables[table_id][self.hash_func(key, 0)] is None or len(self.tables[table_id][self.hash_func(key, 0)]) < self.bucket_size) \
                    or (self.tables[table_id][self.hash_func(key, 1)] is None or len(self.tables[table_id][self.hash_func(key, 1)]) < self.bucket_size):
                bucket_idx = self.hash_func(key, 0)
            else:
                bucket_idx = self.hash_func(key, 0)
                displaced_idx = self.get_rand_idx_from_bucket(bucket_idx, table_id)
                key_to_displace = self.tables[table_id][bucket_idx][displaced_idx]
                self.tables[table_id][bucket_idx][displaced_idx] = key
                key = key_to_displace

            table_id = 1 - table_id
    return False


	def lookup(self, key: int) -> bool:
		# Check if the key is present in either of the hash buckets
		hash0, hash1 = self.hash_func(key, 0), self.hash_func(key, 1)
		return any(key in (self.table[h] if self.table[h] else []) for h in [hash0, hash1])

	def delete(self, key: int) -> None:
		# Delete the key from the hash table if it exists
		for h in [self.hash_func(key, 0), self.hash_func(key, 1)]:
			if self.table[h] and key in self.table[h]:
				self.table[h].remove(key)
				if not self.table[h]:
					self.table[h] = None

	def rehash(self, new_table_size: int) -> None:
		# Rehash the existing keys into a new table with the specified size
		self.__num_rehashes += 1
		self.table_size = new_table_size
		old_table, self.table = self.table, [None] * self.table_size

		for key_bucket in old_table:
			if key_bucket:
				for k in key_bucket:
					self.insert(k)

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define


