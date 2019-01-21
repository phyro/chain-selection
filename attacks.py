
from collections import namedtuple

from chain import Pool

AttackSetting = namedtuple('AttackSetting', ['name', 'pools'])

# Hash renting
hash_rent_11 = AttackSetting(
    'HashRent 11 seconds block time',
    pools=[
        Pool('nh_pool1', 120)
    ],
)

hash_rent_8 = AttackSetting(
    'HashRent 8.5 seconds block time',
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

mining_pool_ethermine_and_hashrent = AttackSetting(
    'Mining pool EtherMine 40% + HashRent 30%',
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
mining_pool_40_and_hashrent_incentivized = AttackSetting(
    'Mining pool 40% and hashrent - incentivized',
    pools=[
        Pool('pool{}'.format(i), 4) for i in range(1, 11),
        Pool('nh_pool11', 20)
    ],
)

# TODO: add a miner to the mining pool