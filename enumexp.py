
## generate all experimental designs of interest
n = 0
stimuli = ['A', 'AB']
for P1 in subsets(stimuli):
    if len(P1) == 0: # skip the empty phase
        continue
    for R1 in variations( ['0', '+'], len(P1), repetition=True ):
        for i in range( 0, len(P1) ):
            phase1 = str(P1[i]) + str(R1[i])
            print '* phase 1: ' + phase1
            for P2 in subsets(stimuli):
                for R2 in variations( ['0', '+'], len(P2), repetition=True ):
                    for j in range( 0, len(P2) ):
                        phase2 = str(P2[j]) + str(R2[j])
#                        print '* phase2: ' + phase2
                        if phase2 == phase1:
                            print 'skipped repeated phase: ' + phase1
                        else:
                            print str(n) + ': ' + phase1 + ' | ' + phase2
                            n += 1
