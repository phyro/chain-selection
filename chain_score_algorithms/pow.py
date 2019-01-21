
def chain_score(blocks):
    return sum(block.pow for block in blocks)
