# Program that defines the Hybrid data structure that combines hash table with BSTs.
class BST_Node:
    """Class to represent a single node in a BST"""
    def __init__(self, key, value):
        self.key = key      # uniquely identifies the node.
        self.value = value  # data associated with the key
        self.left = None    # Node initiated with no left child (no left subtree)
        self.right = None   # Node initiated with no right child (no right subtree)

class Binary_Search_Tree:
    """BST Class to represent each bucket in the hash table"""
    def __init__(self):
        """initialises the tree with empty node"""
        self.root = None

    def insert(self, key, value):
        """Inserts a new key-value pair into the BST"""
        def _insert(node, key, value):
            """helper function to recursively find the correct position for the key"""
            if not node:  # Empty tree(or subtree)
                return BST_Node(key, value)
            if key < node.key:
                node.left = _insert(node.left, key, value)
            elif key > node.key:
                node.right = _insert(node.right, key, value)
            else:
                node.value = value  # Update value if key already exists
            return node

        self.root = _insert(self.root, key, value)  # Updates the root after the insertion

    def search(self, key):
        """Searches for a key in the BST and returns its value if found; else returns None"""
        def _search(node, key):
            """helper function to recursively traverse the BST"""
            if not node: # empty tree (or subtree)
                return None
            if key == node.key:
                return node.value
            elif key < node.key:
                return _search(node.left, key)
            else:
                return _search(node.right, key)

        return _search(self.root, key)  # returns search results

    def delete(self, key):
        """Deletes the key-value pair from the BST and maintains the BST structure"""
        def _delete(node, key):
            """helper function to recursively locate and delete the node"""
            if not node:  # empty tree (or subtree)
                return None
            if key < node.key:
                node.left = _delete(node.left, key)
            elif key > node.key:
                node.right = _delete(node.right, key)
            else:
                # Node to delete is found: key matches the current node's key
                if not node.left:  # Node found with no left child
                    return node.right  # returns right child (or None if it has no right child)
                elif not node.right:  # Node found with no right child
                    return node.left  # returns left child (or None if it has no left child)

                # Node with two children:
                successor = self._find_min(node.right)  # gets the inorder successor
                node.key, node.value = successor.key, successor.value
                node.right = _delete(node.right, successor.key)
            return node  # return the updated node to rebuild the tree structure

        self.root = _delete(self.root, key) #updates the root after deletion

    def _find_min(self, node):
        """Finds the smallest key in a given subtree"""
        while node.left:
            node = node.left
        return node

    def is_empty(self):
        """Checks if the tree is empty"""
        return self.root is None

    def print_bst(self):
        """Print all the key-value pairs in the BST in sorted order."""
        def inorder_traversal(node):
            if node is not None:
                inorder_traversal(node.left)
                print(f"  ({node.key}: {node.value})", end=" ")
                inorder_traversal(node.right)

        if self.root is None:
            print("  Empty")
        else:
            inorder_traversal(self.root)
            print()

class Hybrid_DS:
    """Class for the hybrid data structure"""
    def __init__(self, table_size):
        """class Hybrid_DS initialised with hash table of fixed size and empty buckets (arrays)"""
        self.table_size = table_size
        self.table = [None] * table_size  # Each bucket will hold a BST

    def _hash_function(self, key):
        """Computes the bucket index for a given key using hash() and hash table's size"""
        return hash(key) % self.table_size

    def insert(self, key, value):
        """inserts a key-value pair into the hybrid structure"""
        index = self._hash_function(key)
        if not self.table[index]:  # if no data exists at index
            self.table[index] = Binary_Search_Tree()
        self.table[index].insert(key, value)  # store data in bst found at compute index

    def search(self, key):
        """searches for a key in the hybrid structure and retrieves its associated value"""
        index = self._hash_function(key)
        if not self.table[index]:  # if no data exists at index
            return None
        return self.table[index].search(key)  # search data in bst found at computed index

    def delete(self, key):
        """deletes a key-value pair from the hybrid structure"""
        index = self._hash_function(key)
        if not self.table[index]:  # if no data exists at index
            return False
        self.table[index].delete(key)  # delete data in bst found at computed index
        if self.table[index].is_empty():
            self.table[index] = None  # Free the bucket if BST becomes empty
        return True

    def display_items(self):
        """Display items in each bucket (BST) of the hash table."""
        for index, bucket in enumerate(self.table):
            print(f"Bucket {index}:", end=" ")
            if bucket is None:
                print("None")
            else:
                bucket.print_bst()

def main():
    # Initialize the Hybrid_DS with a table size of 6
    hybrid = Hybrid_DS(7)

    dataset= [(10, "bae"), (5, "tim"), (15, "len"),
              (20, "moe"), (18, "mia"), (25, "zoe"),
              (15, "sue"), (12, "lou"), (18, "rae")]

    print("Inserting data from dataset:")
    for key, value in dataset:
        hybrid.insert(key, value)
        print(f"Inserted ({key}, {value})")

    print("\nPrinting items in hybrid after insertion:")
    hybrid.display_items()

    print("\nSearching for keys in dataset:")
    search_keys = [15, 20, 50]  # keys may exist or not

    for key in search_keys:
        result = hybrid.search(key)
        if result:
            print(f"Key {key} found with value: {result}")
        else:
            print(f"Key {key} not found.")

    print("\nDeleting keys from dataset:")
    delete_keys = [20, 35, 50]  # keys may exist or not

    for key in delete_keys:
        success = hybrid.delete(key)
        if success:
            print(f"Key {key} deleted successfully.")
        else:
            print(f"Key {key} not found for deletion.")

    print("\nSearching again after deletions:")
    for key in search_keys:
        result = hybrid.search(key)
        if result:
            print(f"Key {key} found with value: {result}")
        else:
            print(f"Key {key} not found.")

    print("\nPrinting items in hybrid after deletion:")
    hybrid.display_items()

if __name__ =="__main__":
    main()

