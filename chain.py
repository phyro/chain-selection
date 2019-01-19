
from collections import namedtuple
import random

class Pool(object):

    def __init__(self, address, hashrate):
        self.address = address
        self.hashrate = hashrate
    
    def __repr__(self):
        return "Pool: {}, hashrate: {}".format(self.address, self.hashrate)

class Block(object):

    def __init__(self, height, miner, pow, total_score):
        self.height = height
        self.miner = miner
        self.pow = pow
        self.total_score = total_score
    
    def __repr__(self):
        return "H: {}, total_score: {}, pow: {}".format(self.height, self.total_score, self.pow)

class Chain(object):

    def __init__(self, name, pools, parent_chain_blocks=None,
                 chain_score_fn=None, last_block_mined_at=0, difficulty=100):
        self.name = name
        # pools : [(miner, hashrate), ...]
        self.pools = pools
        if parent_chain_blocks is None:
            self.blocks = [self.genesis()]
        else:
            self.blocks = parent_chain_blocks
        self.chain_score_fn = chain_score_fn
        self.difficulty = difficulty
        self.last_block_mined_at = last_block_mined_at
        self.block_time_elapsed_data = []
        self.block_time = self.recalculate_block_time()

    @property
    def score(self):
        return self.chain_score_fn(self.blocks, self.name)

    def block_score(self, N):
        return self.blocks[N - 1].total_score - self.blocks[N - 2].total_score

    @property
    def height(self):
        return len(self.blocks)

    @property
    def avg_block_time(self):
        # this is only from the fork on
        return sum(x[0] for x in self.block_time_elapsed_data) / float(len(self.block_time_elapsed_data))

    def get_min_max_block_time(self):
        mini = min(self.block_time_elapsed_data, key=lambda x: x[0])
        maxi = max(self.block_time_elapsed_data, key=lambda x: x[0])
        return (mini, maxi)

    def generate_pow(self):
        _pow = 1000
        return int(_pow * random.uniform(0.95, 1.05))

    def genesis(self):
        return Block(1, 'satoshi', 100, 100)

    def add_pool(self, pool):
        self.pools.append(pool)
        self.block_time = self.recalculate_block_time()

    def recalculate_block_time(self):
        # 100 hashrate is 14 seconds
        sum_hashrate = sum(pool.hashrate for pool in self.pools)
        if sum_hashrate == self.difficulty:
            return 14
        rrr = 14.0 / float(self.difficulty)
        diff = abs(sum_hashrate * rrr - 14)
        if sum_hashrate > self.difficulty:
            return 14.0 - diff
        else:
            return 14.0 + diff

    def mines_a_block(self, seconds):
        elapsed = seconds - self.last_block_mined_at
        gauss_guess = random.gauss(elapsed, 1.5)
        will_mine = gauss_guess > self.block_time
        if will_mine:
            self.block_time_elapsed_data.append((elapsed, self.height + 1))
        return will_mine

    def create_block(self, seconds):
        # mine block based on pool_distribution
        miner = self.get_random_pool()
        prev_block = self.blocks[self.height - 1]
        new_block = Block(self.height + 1, miner, self.generate_pow(), None)
        self.blocks.append(new_block)
        # calculate the total score of the chain and write it to the mined block
        total_score = self.score
        assert new_block.total_score is None
        new_block.total_score = total_score
        assert self.blocks[-1].total_score == new_block.total_score  # sanity
        self.last_block_mined_at = seconds
        # Don't adjust the difficulty
        # if len(self.blocks) % 100 == 0:
        #     self.adjust_difficulty()

    def adjust_difficulty(self):
        # If we to generate a block on average every 14 seconds we have to
        # set the difficulty to the sum of the hashrates
        self.difficulty = sum(pool.hashrate for pool in self.pools)
        self.block_time = self.recalculate_block_time()

    
    def get_random_pool(self):
        cumulative_hashrate = 0.0
        sum_hashrate = sum(pool.hashrate for pool in self.pools)
        chosen = random.uniform(0, sum_hashrate)
        for pool in self.pools:
            cumulative_hashrate += pool.hashrate
            if cumulative_hashrate > chosen:
                return pool.address
        raise Exception("no pool chosen, problem with probabilities?")

    def fork(self, name, pools):
        # forks the chain at current state and continues with new pools and resets the block time data
        return Chain(name, [x for x in pools], parent_chain_blocks=[x for x in self.blocks],
            chain_score_fn=self.chain_score_fn, last_block_mined_at=self.last_block_mined_at,
            difficulty=self.difficulty)

    def remove_pools(self, pools):
        pools_addrs = [pool.address for pool in pools]
        # removes some pools from the chain
        self.pools = [pool for pool in self.pools if pool.address not in pools_addrs]
        # recalculate block time from hashrates
        self.block_time = self.recalculate_block_time()
        return self

    def score_over_time(self):
        # prints average block score over a few ranges of blocks
        block_ranges = [(1, 10), (10, 20), (20, 40), (40, 80), (80, 120), (120, 150),
                        (150, 200), (200, 250), (250, 300), (300, 350)]#, (350, 800), (800, 1200), (1200, 1600), (1600, 2000)]
        height_ = self.height
        for start, end in block_ranges:
            scores = []
            for block in self.blocks[-end:-start]:
                cur_score = self.block_score(block.height)
                scores.append(cur_score)
                # print "block: {}, block_score: {}".format(block.height, cur_score)
            print "[{} -> {}], AVG block score: {}".format(height_ - start + 1, height_ - end + 1, sum(scores) / len(scores))
    
    def __repr__(self):
        mini, maxi = self.get_min_max_block_time()
        return "{}: height:{}, score:{}, avg_block_time:{}, min_time:{}, max_time:{}".format(
            self.name, self.height, self.score, self.avg_block_time, mini[0], maxi[0]
        )
