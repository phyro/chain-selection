
def chain_score(blocks, name):
    return sum(block.pow for block in blocks)
