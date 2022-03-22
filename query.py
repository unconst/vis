import bittensor
import torch
import argparse
import time
import json
from tqdm import tqdm

def config():
    parser = argparse.ArgumentParser()   
    parser.add_argument('--block_increment', type=int, help='Blocks per resync', default=100) 
    parser.add_argument('--queries_per_step', type=int, help='Number to query per request.', default=10) 
    bittensor.dendrite.add_args( parser )
    bittensor.logging.add_args( parser )
    bittensor.wallet.add_args( parser )
    bittensor.subtensor.add_args( parser )
    return bittensor.config( parser )

def run(config):
    last_block = -1
    while True:
        bittensor.logging( config )
        sub = bittensor.subtensor( config )
        wallet = bittensor.wallet( config )
        dend = bittensor.dendrite( config, wallet = wallet )
        block = sub.block
        if block - last_block < config.block_increment:
            time.sleep(5)
        else:
            meta = bittensor.metagraph().sync()
            try:
                last_block = block
                batch_size = sub.validator_batch_size
                sequence_length = sub.validator_sequence_length
                start = 0
                stop = 2000
                data = {}
                for uid in tqdm( range(start, stop, config.queries_per_step) ):
                    r, c, t = dend.forward_text(
                        endpoints = meta.endpoints[uid:uid+config.queries_per_step],
                        inputs = torch.ones([batch_size, sequence_length])
                    )
                    for i,(r,c,t) in enumerate(list( zip( r, c, t)) ):
                        data[int(uid + i)] = { "uid":int(uid + i), "code": c.item(), "time":t.item() }
                json.dump(data, open("data/queries/block{}_batch{}_seq{}.txt".format(block,batch_size,sequence_length),'w'))
                print ("+ data/queries/block{}_btc{}_seq{}.txt".format(block,batch_size,sequence_length))
            except Exception as e:
                print(block, e)

if __name__ == "__main__":
    run( config() )