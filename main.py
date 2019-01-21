
from attacks import hash_rent_8
from attacks import hash_rent_11

from attacks import mining_pool_ethermine
from attacks import mining_pool_ethermine_and_hashrent
from attacks import mining_pool_ethermine_nanopool

from attacks import mining_pool_40_incentivized
from attacks import mining_pool_40_and_hashrent_incentivized

from chain import Pool
from chain import Chain
from chain_score_algorithms import standard_pow
from chain_score_algorithms import SWMCd
from utils import has_attacker_won
from utils import print_winner


def run_attacks(chain_rule, algo_name, pools, expected_blocks, fork_block):
    attack_settings = [
        hash_rent_11,
        hash_rent_8,
        mining_pool_ethermine,
        mining_pool_ethermine_and_hashrent,
        mining_pool_ethermine_nanopool
        # protocol incentivized
        # mining_pool_40_incentivized,
        # mining_pool_40_and_hashrent_incentivized

    ]
    total_seconds = expected_blocks * 14

    for attack in attack_settings:
        mainnet = Chain('mainnet', pools, parent_chain_blocks=None, chain_score_fn=chain_rule)
        attacker_chain = None
        active_chains = [mainnet]
        lost_at_block = None
        forked = False

        for seconds in range(total_seconds):
            for _chain in active_chains:

                if _chain.mines_a_block(seconds):
                    _chain.create_block(seconds)
                if _chain.name == 'mainnet' and _chain.height == fork_block and not forked:
                    print "Chain block time and pools before fork:"
                    print "  - mainnet: block_time:{}, pools:{}".format(
                        mainnet.block_time, mainnet.pools)
                    attacker_chain = mainnet.fork(attack.name, attack.pools)
                    mainnet = mainnet.remove_pools(attack.pools)
                    active_chains = []
                    active_chains.append(mainnet)
                    active_chains.append(attacker_chain)
                    forked = True
                    print "Chain block time and pools after fork:"
                    print "  - {}: block_time:{}, pools:{}".format(
                        attacker_chain.name, attacker_chain.block_time, attacker_chain.pools)
                    print "  - mainnet: block_time:{}, pools:{}".format(
                        mainnet.block_time, mainnet.pools)
                # Check if the mainnet lost. We lost when the attacker is more than
                # 30 blocks ahead and has a higher score
                if lost_at_block is None and has_attacker_won(active_chains):
                    lost_at_block = active_chains[0].height
                    print "Lost to attacker at block: {}".format(lost_at_block)

        print_winner(algo_name, active_chains, expected_blocks, fork_block)

etc_pools = [
    Pool('EtherMine', 40),
    Pool('Nanopool', 21),
    Pool('MiningPoolhub', 7),
    Pool('2miners', 3),
    Pool('privatePool', 7),
    Pool('Clona', 2),
    Pool('ETC altpool', 3),
    Pool('privatePool2', 10),
    Pool('f2pool', 2),
    Pool('HiveonPool', 2),
    Pool('privatePool3', 1),
    Pool('privatePool4', 1),
    Pool('privatePool5', 1),
]
# Incentivized pools
incentivized_pools = [Pool('pool{}'.format(i), 4) for i in range(1, 26)]

# Simulate PoW 51%
run_attacks(standard_pow, 'PoW', etc_pools, 5500, 4850)
# Simulate SWHVd 51%
run_attacks(SWMCd, 'SWMCd', etc_pools, 5500, 4850)
