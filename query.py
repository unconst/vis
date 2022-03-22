import bittensor
import torch
import random
import time
import json
from tqdm import tqdm

last_block = -1
block_increment = 100
while True:
    sub = bittensor.subtensor()
    wallet = bittensor.wallet()
    dend = bittensor.dendrite( wallet = wallet )
    block = sub.block
    if block - last_block < block_increment:
        time.sleep(5)
    else:
        meta = bittensor.metagraph().sync()
        try:
            last_block = block
            batch_size = sub.validator_batch_size
            sequence_length = sub.validator_sequence_length
            start = 0
            stop = 2000
            incr = 10
            data = {}
            for uid in tqdm( range(start, stop, incr) ):
                r, c, t = dend.forward_text(
                    endpoints = meta.endpoints[uid:uid+incr],
                    inputs = torch.ones([batch_size, sequence_length])
                )
                for i,(r,c,t) in enumerate(list( zip( r, c, t)) ):
                    data[int(uid + i)] = { "uid":int(uid + i), "code": c.item(), "time":t.item() }
            json.dump(data, open("data/queries/block-{}_batch-{}_seq-{}.txt".format(block,batch_size,sequence_length),'w'))
            print ("+ data/queries/block{}-btc{}_seq{}.txt".format(block,batch_size,sequence_length))
        except Exception as e:
            print(block, e)