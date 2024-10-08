
## this is a copy-and-pase from https://github.com/lh3/readfq/blob/master/readfq.py
def readseq(fp): # this is a generator function
#	print(fp)
	last = None # this is a buffer keeping the last unprocessed line
	while True: # mimic closure; is it a bad idea?
		if not last: # the first record or a record following a fastq
			for l in fp: # search for the start of the next record
				#print('1', l)
				if l[0] in '>@': # fasta/q header line
					last = l[:-1] # save this line
					break
		if not last: break
		name, seqs, last = last[1:].partition(" ")[0], [], None
		for l in fp: # read the sequence
			#print('2', l)
			if l[0] in '@+>':
				#print('judge last.')
				last = l[:-1]
				break
			seqs.append(l[:-1])
			#print('idlast?', last)
		if not last or last[0] != '+': # this is a fasta record
			yield name, ''.join(seqs), None  # yield a fasta record
			if not last: break
		else: # this is a fastq record
			seq, leng, seqs = ''.join(seqs), 0, []
			for l in fp: # read the quality
				#print('3', l)
				seqs.append(l[:-1])
				leng += len(l) - 1
				if leng >= len(seq): # have read enough quality
					last = None
					yield name, seq, ''.join(seqs) # yield a fastq record
					break
			if last: # reach EOF before reading enough quality
				yield name, seq, None # yield a fasta record instead
				break
