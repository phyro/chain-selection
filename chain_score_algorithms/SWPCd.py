
from collections import defaultdict

# Sliding-window-pools-consistency delta

def chain_score(blocks):
  new_block = blocks[-1]  # This is the mined block
  prev_blocks = blocks[:-1]
  # Calculate the pool consistency of the network
  adjusted_pow_score = PCI(blocks) * new_block.pow
  previous_block = prev_blocks[-1]
  # The value of the block is a combination of work and pool consistency
  return previous_block.total_score + adjusted_pow_score

def PCI(blocks):
  # Checks if the miners from the past are still present
  miners_3000 = get_miners(blocks[-3000:])
  last_30_blocks = blocks[-30:]
  miners_last_30 = {block.miner for block in last_30_blocks}
  penalty_ratio = 1.0
  for miner, miner_ratio in miners_3000.items():
    if miner in miners_last_30:
      # If the miner is in the last 30 blocks, don't penalize his contribution ratio
      penalty_ratio -= miner_ratio
  return 1.0 - penalty_ratio

def get_miners(blocks):
  miners = defaultdict(int)
  for block in blocks:
    miners[block.miner] += 1
  return {
    miner: blocks_mined / float(len(blocks))
    for miner, blocks_mined in miners.items()
  }
