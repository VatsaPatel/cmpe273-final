import hashlib
from dataclasses import dataclass


class Node(object):
    def __init__(self, val=None, left=None, right=None):
        # Hash value of the node via hashlib.sha256(xxxxxx.encode()).hexdigest()
        self.val = val
        # Left node
        self.left = left
        # Right node
        self.right = right

    def __str__(self):
        return f':val={self.val},left={self.left},right={self.right}:'


class MerkleTrees(object):
    def __init__(self):
        self.root = None
        # txns dict: { hash_val -> 'file_path' } 
        self.txns = None


    def get_root_hash(self):
        return self.root.val if self.root else None

    def build(self, txns):
        """
        Construct a Merkle tree using the ordered txns from a given txns dictionary.
        """
        # save the original txns(files) dict while building a Merkle tree.
        self.txns = txns
        txns_list = list(txns.keys())
        if len(txns_list) % 2 != 0:
            txns_list.append(txns_list[-1])
        temp = []
        for index in range(0, len(txns_list) - 1, 2):
            left = txns_list[index]
            right = txns_list[index + 1]
            combine = left + right
            root = hashlib.sha256(combine.encode()).hexdigest()
            current_node = Node(root, Node(left), Node(right))
            # print(current_node)
            temp.append(current_node)

        self.recur(temp)

    def recur(self, list):
        temp = []
        if len(list) == 1:
            self.root = list[0]
        elif len(list) > 1:
            for index in range(0, len(list) - 1, 2):
                current_node = None
                left = list[index]
                right = list[index + 1]
                combine = left.val + right.val
                root = hashlib.sha256(combine.encode()).hexdigest()
                current_node = Node(root, left, right)
                temp.append(current_node)
            self.recur(temp)


    def print_level_order(self):
        """
          1             1
         / \     -> --------------------
        2   3       2 3
        """

        # print(self.root.val)
        # print("--------------------")

        self.print_child(self.root)

    def print_child(self, root):
        current_level = [root]
        while current_level:
            print(' '.join(str(node.val) for node in current_level))
            print("--------------------")
            next_level = list()
            for n in current_level:
                if n.left:
                    next_level.append(n.left)
                if n.right:
                    next_level.append(n.right)
            current_level = next_level


    @staticmethod
    def compare(x, y):
        """
        Compare a given two merkle trees x and y.
        x: A Merkle Tree
        y: A Merkle Tree
        Pre-conditions: You can assume that number of nodes and heights of the given trees are equal.

        Return: A list of pairs as Python tuple type(xxxxx, yyyy) that hashes are not match.
        https://realpython.com/python-lists-tuples/#python-tuples
        """
        diff = []
        trip = 1
        if x.get_root_hash() == y.get_root_hash():
            return diff
        elif x.get_root_hash() != y.get_root_hash():
            diff.append((x.root.val,y.root.val))

        # x_left = x.root.left.val
        # x_right = x.root.right.val
        #
        # y_left = y.root.left.val
        # y_right = y.root.right.val
        #
        # if x_left != y_left:
        #     diff.append((x_left, y_left))
        #
        # if x_right != y_right:
        #     diff.append((x_right, y_right))

        diff = diff + (MerkleTrees.compareN(x.root, y.root))

        return diff

    @staticmethod
    def compareN(x, y):
        temp = []
        if x.val != y.val and x.left:
            # First recur on left child
            if(x.left.val != y.left.val):
                temp.append((x.left.val,y.left.val))
                temp = temp + MerkleTrees.compareN(x.left,y.left)
            # then print the data of node
            # print(root.val),

            # now recur on right child
            if (x.right.val != y.right.val):
                temp.append((x.right.val, y.right.val))
                temp = temp + MerkleTrees.compareN(x.right,y.right)

        return temp
