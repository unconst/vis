import bittensor
import torch
import argparse
import time
import json
from tqdm import tqdm

def config():
    parser = argparse.ArgumentParser()   
    bittensor.subtensor.add_args( parser )
    return bittensor.config( parser )

def run(config):
    last_block = -1
    while True:
        sub = bittensor.subtensor( config )
        block = sub.block
        print(block)
        if block == last_block:
            time.sleep(5)
        else:
            print('run')
            try:
                last_block = block
                sub = bittensor.subtensor( config )
                data = {}
                data['block'] = block
                params = ['N', 'TotalStake', 'TotalEmission', 'Rho', 'Kappa', 'IncentivePruningDenominator', 'StakePruningDenominator', 
                    'ValidatorEpochLen', 'ValidatorEpochsPerReset', 'ValidatorBatchSize', 'MaxAllowedUids', 'MinAllowedWeights', 'MaxAllowedMaxMinRatio', 
                    'ImmunityPeriod', 'TotalIssuance', 'BlocksSinceLastStep', 'BlocksPerStep', 'BondsMovingAverage', 'Difficulty','ActivityCutoff', 
                    'AdjustmentInterval', 'TargetRegistrationsPerInterval', 'MaxRegistrationsPerBlock', 'LastDifficultyAdjustmentBlock', 
                    'LastMechansimStepBlock', 'RegistrationsThisInterval', 'RegistrationsThisBlock'
                ]
                for param in tqdm(params):
                    value = int(sub.substrate.query(  module='SubtensorModule', storage_function = param ).value) 
                    data[param] = value
                    print (param, value)
                json.dump(data, open("data/params/block{}.txt".format(block),'w'))
                print ("+ data/params/block{}.txt".format(block))
            except Exception as e:
                print(block, e)

if __name__ == "__main__":
    run( config() )