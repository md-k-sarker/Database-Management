"""Count block accesses for three file organizations. A 'block access' is one block read or written."""
import math
import random

random.seed(42)
N = 10_000                       # records
BF = 20                          # blocking factor: records per block
keys = random.sample(range(1, 1_000_000), N)
B = math.ceil(N / BF)            # blocks in the file
print(f"{N:,} records, {BF} per block -> {B} blocks\n")


# ---------------- Heap file: records in arrival order ----------------
class Heap:
    def __init__(self, ks):
        self.blocks = [ks[i:i + BF] for i in range(0, len(ks), BF)]

    def search(self, k):                       # scan until found
        reads = 0
        for blk in self.blocks:
            reads += 1
            if k in blk:
                return reads
        return reads

    def range(self, lo, hi):                   # must read everything
        return len(self.blocks)

    def insert(self, k):                       # read the last block, write it back
        if len(self.blocks[-1]) < BF:
            self.blocks[-1].append(k)
            return 2
        self.blocks.append([k])
        return 1                               # a brand-new block is only written


# ---------------- Sorted (sequential) file ----------------
class Sorted:
    def __init__(self, ks):
        self.keys = sorted(ks)

    def _nblocks(self):
        return math.ceil(len(self.keys) / BF)

    def _block(self, i):
        return self.keys[i * BF:(i + 1) * BF]

    def _find_block(self, k):                  # binary search over blocks; returns (block index, reads)
        lo, hi, reads = 0, self._nblocks() - 1, 0
        while lo <= hi:
            mid = (lo + hi) // 2
            blk = self._block(mid)
            reads += 1
            if k < blk[0]:
                hi = mid - 1
            elif k > blk[-1]:
                lo = mid + 1
            else:
                return mid, reads
        return min(lo, self._nblocks() - 1), reads

    def search(self, k):
        return self._find_block(k)[1]

    def range(self, lo, hi):                   # binary search for the first block, then read forward
        i, reads = self._find_block(lo)
        while i < self._nblocks() - 1 and self._block(i)[-1] < hi:
            i += 1
            reads += 1
        return reads

    def insert(self, k):                       # shift later records: every later block is read and rewritten
        i, reads = self._find_block(k)
        after = self._nblocks() - i
        bisect_pos = sum(1 for x in self.keys if x < k)
        self.keys.insert(bisect_pos, k)
        return reads + 2 * after


# ---------------- Static hash file ----------------
class Hashed:
    def __init__(self, ks, buckets):
        self.m = buckets
        self.chains = [[[]] for _ in range(buckets)]    # each bucket: a chain of blocks
        for k in ks:
            self.insert(k)

    def search(self, k):
        reads = 0
        for blk in self.chains[k % self.m]:
            reads += 1
            if k in blk:
                return reads
        return reads

    def range(self, lo, hi):                   # the hash scatters neighbours: scan every block
        return sum(len(c) for c in self.chains)

    def insert(self, k):
        reads = 0
        chain = self.chains[k % self.m]
        for blk in chain:
            reads += 1
            if len(blk) < BF:
                blk.append(k)
                return reads + 1               # + one write
        chain.append([k])                      # overflow block
        return reads + 1


heap, srt = Heap(keys), Sorted(keys)
hsh = Hashed(keys, buckets=math.ceil(N / (BF * 0.8)))   # sized for 80% full buckets
overflow = sum(len(c) - 1 for c in hsh.chains)
print(f"hash file: {hsh.m} buckets, {overflow} overflow blocks\n")

probe = random.sample(keys, 1000)
sk = sorted(keys)
lo, hi = sk[4000], sk[4199]                    # a range holding exactly 200 records
taken = set(keys)
new_keys = []
while len(new_keys) < 500:
    x = random.randrange(1, 1_000_000)
    if x not in taken:
        taken.add(x)
        new_keys.append(x)

rows = []
for name, f in [("heap (unsorted)", heap), ("sorted", srt), ("hashed", hsh)]:
    eq = sum(f.search(k) for k in probe) / len(probe)
    rg = f.range(lo, hi)
    ins = sum(f.insert(k) for k in new_keys) / len(new_keys)
    rows.append((name, eq, rg, ins))

print(f"{'organization':<18}{'equality search':>17}{'range (200 rows)':>18}{'insert':>9}")
print(f"{'':<18}{'(avg blocks)':>17}{'(blocks)':>18}{'(avg)':>9}")
for name, eq, rg, ins in rows:
    print(f"{name:<18}{eq:>17.1f}{rg:>18}{ins:>9.1f}")
print(f"\nlog2({B}) = {math.log2(B):.1f}   (the sorted file's binary search should land near this)")
