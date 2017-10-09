import javalang
import hashlib
import pickle

TEST_SNIPPET = """
package com.falkenberg.eric;

class JustSayHello {

    public static void main(String[] args) {
        System.out.println("Hello World");
    }

}
"""

TEST_SNIPPET_2 = """
package com.falkenberg.eric;

class JustSayHello {

    public static void main(String[] args) {
        System.out.println("Hello World");
    }

}
"""

def compare_code_blocks(block1, block2):
    return obj_to_hash_val(block1) == obj_to_hash_val(block2)

def obj_to_hash_val(obj):
    raw = pickle.dumps(obj)
    return hashlib.sha256(raw).hexdigest()

if __name__ == '__main__':
    tree1 = javalang.parse.parse(TEST_SNIPPET)
    tree2 = javalang.parse.parse(TEST_SNIPPET_2)

    print compare_code_blocks(tree1, tree2)
