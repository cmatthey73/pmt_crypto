
# coding: utf-8

# # A signed list of transactions
# 
# Following the slides we can do the same task with a list of transactions
# 
# ```
# Tim pays Joel $3
# Joel pays Kevin $1.5
# Tim pays Joel $3
# ```
# 

# In[19]:


from hashlib import sha256
import json

def simple_hash_func(value):
    return sha256('{}'.format(value).encode()).hexdigest()[-8:]


# In[26]:


transactions = [
    {'date': '2017-12-12', 'content': 'Tim pays Joel $3', 'nonce': 0},
    {'date': '2017-12-13', 'content': 'Joel pays Kevin $1.5', 'nonce': 0},
    {'date': '2017-12-13', 'content': 'Tim pays Joel $3', 'nonce': 0},
]


# We will link this set of transaction to each other by computing a hash for each one that includes the has 
# of the previous transaction. This way the third transaction is linked to the second, which is linked to the first.
# In[27]:


def sign_transactions(transactions):
    signed = []

    for transaction in transactions:
        new_transaction = transaction.copy()
        if signed:
            new_transaction['previous_signature'] = signed[-1]['signature']
        else:
            new_transaction['previous_signature'] = ''

        signature = simple_hash_func(
            json.dumps(new_transaction, sort_keys=True).encode()
        )
        new_transaction['signature'] = signature
        signed.append(new_transaction)
        
    return signed

signed_transactions = sign_transactions(transactions)

for c_transaction in signed_transactions:
    print('{date}\t{content}\t{nonce}\t{signature}'
          '\t{previous_signature}'.format(**c_transaction))


# We can now try and manipulate an earlier transaction in our chain and see what happens.
# 
# We make a fairly simple modification, swapping a `5` and a `.` in the second transaction. As a result Kevin wil lreceive \$15 instead of $1.5. A third party will be able to tell that this modification has happened because the signature for the last transaction differs from what they have.

# In[28]:


transactions[1]['content'] = 'Joel pays Kevin $15.'

new_signed_transactions = sign_transactions(transactions)

for new_transaction, old_transaction in zip(new_signed_transactions, signed_transactions):
    print('\t{date}\t{content}'.format(**new_transaction))
    print('\t\t\t\tnew: ', new_transaction['signature'])
    print('\t\t\t\told: ', old_transaction['signature'])


# Note how the value of the hash function for the second transation is completely different from its old value 
# even though we just swapped a `5` and `.`. Because the hash value of the previous transaction feeds into the 
# current transaction's hash value we can tell by looking just at the last transaction that something has gone 
# wrong or was manipulated along the way. We do not have to go through every single transaction to be able to 
# tell.
# 
# The problem with using a simple hash function like this is that it is not very expensive to  create a fake 
# blockchain where you recompute all the hashes yourself.
