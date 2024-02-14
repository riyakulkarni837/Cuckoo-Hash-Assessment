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
		cycles = 0
		function_id = 0

		while True:
			if cycles > self.CYCLE_THRESHOLD:
				return False
			hash0 = self.hash_func(key, function_id)
			hash1 = self.hash_func(key, 1-function_id)
			if self.table[hash0] is None:
				self.table[hash0] = [key]
				return True
			elif len(self.table[hash0]) < self.bucket_size:
				self.table[hash0].append(key)
				return True
			elif self.table[hash1] is None:
				self.table[hash1] = [key]
				return True
			elif len(self.table[hash1]) < self.bucket_size:
				self.table[hash1].append(key)
				return True
			else:
				idx = self.get_rand_bucket_index(hash0)
				key, self.table[hash0][idx] = self.table[hash0][idx], key
				cycles += 1


	def lookup(self, key: int) -> bool:
		hash0 = self.hash_func(key, 0)
		hash1 = self.hash_func(key, 1)
		if self.table[hash0] is not None and key in self.table[hash0]:
			return True
		if self.table[hash1] is not None and key in self.table[hash1]:
			return True
		return False
		

	def delete(self, key: int) -> None:
		hash0 = self.hash_func(key, 0)
		hash1 = self.hash_func(key, 1)
		if self.table[hash0] is not None and key in self.table[hash0]:
			self.table[hash0].remove(key)
			if(len(self.table[hash0]) == 0):
				self.table[hash0] = None
		if self.table[hash1] is not None and key in self.table[hash1]:
			self.table[hash1].remove(key)
			if(len(self.table[hash1]) == 0):
				self.table[hash1] = None

	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1
		self.table_size = new_table_size # do not modify this line
		old_table = self.table
		self.table = [None]*self.table_size
		for key in old_table:
			if key is not None:
				for k in key:
					self.insert(k)

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define


