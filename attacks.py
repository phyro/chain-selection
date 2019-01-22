
from collections import namedtuple

from chain import Pool

AttackSetting = namedtuple('AttackSetting', ['name', 'pools', 'abbreviation'])


# Hash renting
hash_rent_11 = AttackSetting(
    'HashRent 11 seconds block time',
    pools=[
        Pool('nh_pool1', 120)
    ],
    abbreviation='HashRent11'
)

hash_rent_8 = AttackSetting(
    'HashRent 8.5 seconds block time',
    pools=[
        Pool('nh_pool1', 140)
    ],
    abbreviation='HashRent8.5'
)

# ETC pools
mining_pool_ethermine = AttackSetting(
    'Ethermine 40%',
    pools=[
        Pool('EtherMine', 40)
    ],
    abbreviation='EM40%'
)

mining_pool_ethermine70 = AttackSetting(
    'Ethermine 70%',
    pools=[
        Pool('EtherMine', 70)
    ],
    abbreviation='EM70%'
)

mining_pool_ethermine_and_hashrent = AttackSetting(
    'Mining pool EtherMine 40% + HashRent 30%',
    pools=[
        Pool('EtherMine', 40),
        Pool('nh_pool4', 30),
    ],
    abbreviation='EM40% HashRent30'
)

mining_pool_ethermine_nanopool = AttackSetting(
    'Ethermine 40% and Nanopool 21%',
    pools=[
        Pool('EtherMine', 40),
        Pool('Nanopool', 21),
    ],
    abbreviation='EM40 NP21'
)

# Protocol level pools assumed
mining_pool_40_incentivized = AttackSetting(
    'Mining pool 40% - incentivized',
    pools=[Pool('pool{}'.format(i), 4) for i in range(1, 11)],
    abbreviation='Pool40-inc'
)
mining_pool_40_and_hashrent_incentivized = AttackSetting(
    'Mining pool 40% and hashrent - incentivized',
    pools=[
        Pool('pool{}'.format(i), 4) for i in range(1, 11),
        Pool('nh_pool11', 20)
    ],
    abbreviation='Pool40 Hashrent11 - inc'
)
