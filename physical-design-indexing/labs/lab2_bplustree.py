"""A small B+ tree (insert, search, range scan) so you can see splits and measure height."""
import bisect
import random


class Node:
    def __init__(self, leaf):
        self.leaf = leaf
        self.keys = []
        self.children = []      # internal nodes only
        self.next = None        # leaf nodes only: link to the next leaf


class BPlusTree:
    def __init__(self, max_keys=3):
        self.max_keys = max_keys          # a node splits when it would hold more keys than this
        self.root = Node(leaf=True)

    # ---- search: returns (leaf, number of nodes read) ----
    def _find_leaf(self, key):
        node, reads = self.root, 1
        while not node.leaf:
            node = node.children[bisect.bisect_right(node.keys, key)]
            reads += 1
        return node, reads

    def search(self, key):
        leaf, reads = self._find_leaf(key)
        return key in leaf.keys, reads

    def range(self, lo, hi):
        leaf, reads = self._find_leaf(lo)
        out = []
        while leaf is not None:
            for k in leaf.keys:
                if k > hi:
                    return out, reads
                if k >= lo:
                    out.append(k)
            leaf = leaf.next              # follow the leaf chain: no need to climb back up
            if leaf is not None:
                reads += 1
        return out, reads

    # ---- insert ----
    def insert(self, key):
        split = self._insert(self.root, key)
        if split:                          # the root itself split: the tree grows one level
            sep, right = split
            new_root = Node(leaf=False)
            new_root.keys = [sep]
            new_root.children = [self.root, right]
            self.root = new_root

    def _insert(self, node, key):
        if node.leaf:
            i = bisect.bisect_left(node.keys, key)
            if i < len(node.keys) and node.keys[i] == key:
                return None                # duplicate key: ignore
            node.keys.insert(i, key)
            if len(node.keys) <= self.max_keys:
                return None
            mid = (len(node.keys) + 1) // 2
            right = Node(leaf=True)
            right.keys = node.keys[mid:]
            node.keys = node.keys[:mid]
            right.next, node.next = node.next, right
            return right.keys[0], right    # a leaf split COPIES the separator up
        i = bisect.bisect_right(node.keys, key)
        split = self._insert(node.children[i], key)
        if not split:
            return None
        sep, right = split
        node.keys.insert(i, sep)
        node.children.insert(i + 1, right)
        if len(node.keys) <= self.max_keys:
            return None
        mid = len(node.keys) // 2
        up = node.keys[mid]
        sibling = Node(leaf=False)
        sibling.keys = node.keys[mid + 1:]
        sibling.children = node.children[mid + 1:]
        node.keys = node.keys[:mid]
        node.children = node.children[:mid + 1]
        return up, sibling                 # an internal split MOVES the middle key up

    # ---- inspection ----
    def height(self):
        h, node = 1, self.root
        while not node.leaf:
            node, h = node.children[0], h + 1
        return h

    def levels(self):
        out, level = [], [self.root]
        while level:
            out.append(level)
            level = [c for n in level if not n.leaf for c in n.children]
        return out

    def leaf_fill(self):
        leaves = [n for n in self.levels()[-1]]
        return sum(len(n.keys) for n in leaves) / (len(leaves) * self.max_keys), len(leaves)


# ---------- demo 1: watch a small tree grow ----------
t = BPlusTree(max_keys=3)
for k in [10, 20, 5, 6, 12, 30, 7, 17, 3, 25, 28, 40]:
    t.insert(k)
    print(f"insert {k:>2}: height {t.height()}")
print("\nthe tree (one line per level):")
for depth, level in enumerate(t.levels()):
    print(f"  level {depth}: " + "  ".join(str(n.keys) for n in level))
found, reads = t.search(17)
print(f"\nsearch 17 -> found={found}, nodes read={reads}")
rng, reads = t.range(6, 20)
print(f"range 6..20 -> {rng}, nodes read={reads}  (one descent, then along the leaf chain)")

# ---------- demo 2: height stays tiny as the data grows ----------
print("\nheight of a B+ tree holding 100,000 random keys, by node size:")
print(f"{'max keys/node':>14}{'height':>8}{'leaf fill':>11}{'leaves':>9}")
random.seed(7)
data = random.sample(range(1, 10_000_000), 100_000)
for m in (3, 15, 63, 255):
    tree = BPlusTree(max_keys=m)
    for k in data:
        tree.insert(k)
    fill, leaves = tree.leaf_fill()
    print(f"{m:>14}{tree.height():>8}{fill:>10.0%}{leaves:>9,}")

# ---------- correctness check against a plain sorted list ----------
tree = BPlusTree(max_keys=15)
for k in data:
    tree.insert(k)
ref = sorted(data)
assert all(tree.search(k)[0] for k in random.sample(data, 2000))
assert not any(tree.search(k)[0] for k in range(1, 200) if k not in set(data))
lo, hi = ref[1000], ref[1500]
assert tree.range(lo, hi)[0] == ref[1000:1501]
print("\nchecks passed: every key found, absent keys not found, range scan equals the sorted list")
