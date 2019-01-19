
from collections import namedtuple

from chain import Pool

AttackSetting = namedtuple('AttackSetting', ['name', 'pools'])

# Nice hash
nice_hash_12 = AttackSetting(
    'NiceHash 11 seconds block time',
    pools=[
        Pool('nh_pool1', 120)
    ],
)

nice_hash_10 = AttackSetting(
    'NiceHash 8.5 seconds block time',
    pools=[
        Pool('nh_pool1', 140)
    ],
)

# ETC pools
mining_pool_ethermine = AttackSetting(
    'Ethermine 40%',
    pools=[
        Pool('EtherMine', 40)
    ],
)

mining_pool_ethermine_and_nicehash = AttackSetting(
    'Mining pool EtherMine 40% + Nicehash 30%',
    pools=[
        Pool('EtherMine', 40),
        Pool('nh_pool4', 30),
    ],
)

mining_pool_ethermine_nanopool = AttackSetting(
    'Ethermine 40% and Nanopool 21%',
    pools=[
        Pool('EtherMine', 40),
        Pool('Nanopool', 21),
    ],
)

# Protocol level pools assumed
mining_pool_40_incentivized = AttackSetting(
    'Mining pool 40% - incentivized',
    pools=[Pool('pool{}'.format(i), 4) for i in range(1, 11)],
)
mining_pool_40_and_nicehash_incentivized = AttackSetting(
    'Mining pool 40% and nicehash - incentivized',
    pools=[
        Pool('pool{}'.format(i), 4) for i in range(1, 11),
        Pool('nh_pool11', 20)
    ],
)

# TODO: add a miner to the mining pool