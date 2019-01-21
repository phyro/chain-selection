
def print_winner(algo_name, chains, expected_blocks, fork_block):
    def get_work_from_block(chain, N):
        length = len(chain.blocks) - N
        # Returns the sum of total work for the blocks since block N
        return sum(chain.block_score(len(chain.blocks) - cur_n) for cur_n in range(length, 0, -1))

    # chains[0] = mainnet, chains[1] = attacker
    print "-----------------------------------------------------"
    print " Testing {} against {}".format(algo_name, chains[1].name)
    print "   - Expecting around {} blocks ({} * 14)".format(expected_blocks, expected_blocks)
    print "   - Fork of attacker chain happens at {} block".format(fork_block)
    print "-----------------------------------------------------"
    sorted_chains = sorted(chains, key=lambda ch: ch.score, reverse=True)
    for chain_ in sorted_chains:
        print chain_
        chain_.score_over_time()
    fork_work_mainnet = get_work_from_block(chains[0], fork_block)
    fork_work_attacker = get_work_from_block(chains[1], fork_block)
    print "\n Work done since fork block:"
    print " Mainnet score: {}, height: {}".format(fork_work_mainnet, chains[0].height)
    print " {} score: {}, height: {}".format(chains[1].name, fork_work_attacker, chains[1].height)
    print " Ratio: {}".format(fork_work_mainnet / float(fork_work_attacker))
    print "-----------------------------------------------------"
    print "\nWinner: {}\n".format(sorted_chains[0])

def has_attacker_won(active_chains):
    # If attacker is not yet in the game, he can't win
    if len(active_chains) < 2:
        return False
    mainnet = active_chains[0]
    attacker = active_chains[1]
    if mainnet.height < attacker.height and attacker.height - mainnet.height > 30 and\
        attacker.score > mainnet.score:
        return True
    return False
