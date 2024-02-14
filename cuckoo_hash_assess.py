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
		self.tables = [[None]*init_size for _ in range(2)]

	def get_rand_idx_from_bucket(self, bucket_idx: int, table_id: int) -> int:
		# you must use this function when you need to displace a random key from a bucket during insertion (see the description in requirements.py). 
		# this function randomly chooses an index from a given bucket for a given table. this ensures that the random 
		# index chosen by your code and our test script match.
		# 
		# for example, if you are inserting some key x into table 0, and hash_func(x, 0) returns 5, and the bucket in index 5 of table 0 already has 4 elements,
		# you will call get_rand_bucket_index(5, 0) to determine which key from that bucket to displace, i.e. if get_random_bucket_index(5, 0) returns 2, you
		# will displace the key at index 2 in that bucket.
		rand.seed(int(str(bucket_idx) + str(table_id)))
		return rand.randint(0, self.bucket_size-1)

	def hash_func(self, key: int, table_id: int) -> int:
		key = int(str(key) + str(self.__num_rehashes) + str(table_id))
		rand.seed(key)
		return rand.randint(0, self.table_size-1)

	def get_table_contents(self) -> List[List[Optional[List[int]]]]:
		# the buckets should be implemented as lists. Table cells with no elements should still have None entries.
		return self.tables

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.

	def insert(self, key: int) -> bool:
		# TODO
		table_id = 0
		for _ in range(self.CYCLE_THRESHOLD + 1):
			# Calculating the bucket index using hash_func  
			bucket_idx = self.hash_func(key, table_id)
			# Retrieving the bucket at the calculated index
			bucket = self.tables[table_id][bucket_idx]

			# If the bucket is None, creating a new bucket with the key
			if bucket is None:
				self.tables[table_id][bucket_idx] = [key]
				return True
			# If the bucket has space, appending the key to it
			elif len(bucket) < self.bucket_size:
				bucket.append(key)
				return True
			# The bucket is full, so displacing a key and continue the process
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
		# TODO
		hash_value1 = self.hash_func(key, 0)
		hash_value2 = self.hash_func(key, 1)
		if (self.tables[0][hash_value1] is not None and key in self.tables[0][hash_value1]) or (self.tables[1][hash_value2] is not None and key in self.tables[1][hash_value2]):
			return True
		return False


	def delete(self, key: int) -> None:
		# TODO
		for table_id in range(2):
			bucket_idx = self.hash_func(key, table_id)
			bucket = self.tables[table_id][bucket_idx]
			
			# Checking if the bucket exists and the key is in the bucket
			if bucket is not None and key in bucket:
				# Remove the key from the bucket
				bucket.remove(key)

				# Checking if the bucket is now empty, set to None if so
				if len(bucket) == 0:
					self.tables[table_id][bucket_idx] = None
				return
		return



	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
		# TODO
		if new_table_size <= 0:
			raise ValueError("New table size must be a positive integer.")

		# Updating the table size	
		old_tables = [self.tables[0].copy(), self.tables[1].copy()]
		self.tables = [[None] * new_table_size for _ in range(2)]
		
		# Copy keys from old tables to the new tables
		for old_table in old_tables:
			if old_table is not None:
				for bucket in old_table:
					if bucket is not None:
						for key in bucket:
							self.insert(key)

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define


