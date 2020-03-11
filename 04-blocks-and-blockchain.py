
# coding: utf-8

# # Putting it all together
# 
# Let's build a simple blockchain using all the tools we learnt about.

# In[15]:


import json
import hashlib
from time import time
from pprint import pprint


# To get started we define two transactions to get us rolling and see everything working.

# In[16]:


# Two transactions: we send 10 coins from A to B and then 3 from B to C.
transaction1 = {'from': "A's address",
                'to': "B's address",
                'amount': 10}
transaction2 = {'from': "B's address",
                'to': "C's address",
                'amount': 3}


# ## Grouping transactions into blocks
# 
# A new block has a timestamp and links to the previous one via its hash. 
# Otherwise the list of transactions, the hash and nonce are empty. We will set them when we mine the block.

# In[17]:


def new_block(previous_block):
    if not previous_block['hash']:
        raise RuntimeError("You need to close a block by mining it before it can be extended")

    block = {'timestamp': time(),
             'transactions': [],
             'nonce': 0,
             'hash': '',
             'previous_hash': previous_block['hash']
             }
    return block


# There is one special block: the genesis block. So far we avoided talking about how to get your  
# blockchain started, this is how. The genesis block is similar to the others except it does not 
# refer to a previous one, the `previous_hash` field is empty.
# In[18]:


def genesis_block():
    return {'timestamp': time(),
            'transactions': [],
            'nonce': 0,
            'hash': '',
            'previous_hash': ''
            }


# ## Mining a new block
# 
# Performing the proof-of-work and thereby "locking" the transactions in it in place is called mining. 
# Why? Because the node that performs the verification and proof-of-work is rewarded with a coin. 
# The transaction looks a little different from others because it originates from a special source: the network.
# 
# This is how coins come to exist in our blockchain.

# In[19]:


BLOCKCHAIN = []

def mine(block, miner):
    block['transactions'].append({'from': 'network', 'to': miner, 'amount': 1})
    h = ''
    while not h.startswith('0000'):
        block['nonce'] += 1
        block_string = json.dumps(block, sort_keys=True).encode()
        h = hashlib.sha256(block_string).hexdigest()

    block['hash'] = h
    BLOCKCHAIN.append(block)

    return block


# ## Building up our chain
# 
# Let's put these to work: generate the genesis block and then create one new block that contains our two transactions:

# In[20]:


first_block = genesis_block()
print('first block:')
pprint(first_block)


# In[21]:


print('mining the first block...')
mined_first_block = mine(first_block, miner='tim')
pprint(mined_first_block)


# Next, we create the second block and add our two transactions:

# In[22]:


second_block = new_block(mined_first_block)
second_block['transactions'] = [transaction1, transaction2]
print("second block:")
pprint(second_block)


# In[23]:


print('mining the second block...')
mined_second_block = mine(second_block, miner='kevin')
pprint(mined_second_block)


# ## The Blockchain
# 
# And we can inspect our whole blockchain:

# In[24]:


pprint(BLOCKCHAIN)

