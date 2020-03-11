
# coding: utf-8

# # Hash Functions
# 
# Hash functions compute a fingerprint for the data you feed into them. 
# This fingerprint uniquely identifies the data you fed into the hash function.
 <img src="hashfunction.png" style="max-width: 60%" />
# 
# Here we start out with hash functions where we use the [SHA256](https://en.wikipedia.org/wiki/SHA-2) 
# algorithm built into python. We wrap the function up a bit so we can use it with both strings and numbers.
 
# In[3]:


from hashlib import sha256

def simple_hash_func(value):
    return sha256('{}'.format(value).encode()).hexdigest()[-8:]


# Using the hash function, here we can use the hash function to encode a _signature_ or fingerprint of the value. 
# The primary purpose of this _signature_ is that it encapsulates the value without actually containing it. 
# Individual hashes are very quick to compute which is important for making a blockchain easy to verify.

# In[4]:


my_favorite_number = 12345

print(my_favorite_number, '\t', simple_hash_func(my_favorite_number))

# we can now try adding one to this number and we see that the hash changes
print(my_favorite_number + 1, '\t', simple_hash_func(my_favorite_number + 1))

if simple_hash_func(my_favorite_number) != simple_hash_func(my_favorite_number + 1):
    print('Hashes do not match!')

