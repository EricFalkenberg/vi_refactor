import javalang

TEST_SNIPPET = """
package com.falkenberg.eric;

class JustSayHello {

    public static void main(String[] args) {
        System.out.println("Hello World");
    }

}
"""

if __name__ == '__main__':
    tree = javalang.parse.parse(TEST_SNIPPET)
    print tree.package.name
    print tree.types[0].name
    for dec in tree.types[0].body:
        out_string = ""
        print dec.name, dec.throws
        for p in dec.parameters:
            print p.type.name, p.type.dimensions, p.name, p.varargs
        print dec.body[0].expression.arguments
        print dec.return_type
