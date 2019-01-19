
from collections import defaultdict

# Sliding-window-miners-consistency delta

def chain_score(blocks, name):
  new_block = blocks[-1]  # This is the mined block
  prev_blocks = blocks[:-1]
  # Calculate the pool consistency of the network
  PCI = calc_PCI(blocks, name)
  # PCI regulates the amount of work done
  adjusted_pow_score = PCI * new_block.pow
  # CMS is Consistent Miner Bonus ratio - new miners don't get it. Value between 0 and 1
  CMB_ratio = calc_CMB_ratio(new_block.miner, prev_blocks)
  # Miner consistency can be awarded at best as the work done
  CMB_score = CMB_ratio * adjusted_pow_score
  # NOTE: lowering adjusted_PoW_score also lowers the PCI_score which depends on it
  # The value of the block is a combination of work, pool consistency and miner consistency
  block_score = adjusted_pow_score + CMB_score
  previous_block = prev_blocks[-1]
  return previous_block.total_score + block_score

def calc_CMB_ratio(miner, prev_blocks):
  # calculate the % of blocks the miner mined in the last 3000 blocks
  miner_mined_3000 = get_blocks_mined(3000, miner, prev_blocks)
  # check how much blocks he mined relative to last 3000 blocks
  relative_mined = miner_mined_3000 / float(min(3000, len(prev_blocks)))
  # miner can get a 'speeding ticket' if they are speeding up on last 30 blocks
  speed_penalty = speeding_ticket(miner, prev_blocks)
  return max(0.0, relative_mined - speed_penalty)

def calc_PCI(blocks, name):
  # Checks if the miners from the past are still present
  # TODO: The measure should scale well with minority leaving (perhaps even account for the number of pools)
  miners_3000 = get_miners(blocks[-3000:])
  last_50_blocks = blocks[-50:]
  miners_last_50 = {block.miner for block in last_50_blocks}
  penalty_ratio = 1.0
  for miner, miner_ratio in miners_3000.items():
    if miner in miners_last_50:
      # If the miner is in the last 50 blocks, don't penalize his contribution ratio
      penalty_ratio -= miner_ratio
  return 1.0 - penalty_ratio
  
def get_miners(blocks):
  miners = defaultdict(int)
  for block in blocks:
    miners[block.miner] += 1
  total = sum(miners.values())
  assert total == len(blocks)
  return {
    miner: blocks_mined / float(total)
    for miner, blocks_mined in miners.items()
  }

def get_blocks_mined(N, miner, prev_blocks):
  return len([1 for block in prev_blocks[-N:] if block.miner == miner])

def speeding_ticket(miner, prev_blocks):
  # Speeding ticket penalizes miners that are speeding up including the new ones
  # NOTE: 30 and 3000 are hardcoded because average block time is constant - 14 sec
  # get the miner avg blocks mined from the last 3000 blocks
  avg_blocks_3000 = get_blocks_mined(3000, miner, prev_blocks) / min(3000, len(prev_blocks))
  # get the miner avg blocks mined from the last 30 blocks
  avg_blocks_30 = get_blocks_mined(30, miner, prev_blocks) / min(30.0, len(prev_blocks))
  if avg_blocks_3000 == 0.0:  # new miner
    return 1.0
  ratio = avg_blocks_30 / float(avg_blocks_3000)
  if ratio < 1.0:
    # if the miner is less active we don't care
    return ratio  # we could perhaps return average from 3000
  # speed penalty - the penalty grows exponentially with speed increase
  if ratio < 2.0:
    # NOTE: we subtract 1.0 because 1.0 is the optimal ratio
    return min(1.0, (ratio - 1.0) ** 1.5)
  return 1.0
