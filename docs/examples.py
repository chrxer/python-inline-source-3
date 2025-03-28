import sourcetypes
from sourcetypes import html, sql, cpp, hpp, golang, rust

test_html: html = """
  <html>
    <body>
      <h1>Inline syntax highlighting!</h1>
    </body>
  </html>
"""

test_sql: sql = """
    SELECT test
    FROM a_table
"""

test_css: sourcetypes.css = """
  body {
    font-weight: bold;
    color: #f00;
  }
"""

test_javascript: sourcetypes.javascript = """
  function() {
    var text = "Some Text";
    alert(text)
  }
"""

test_typescript: sourcetypes.ts = """
  function() {
    var text = "Some Text";
    alert(text)
  }
"""

class x:
  test_jsx: sourcetypes.jsx = \
"""
function() {
  const element = <h1>Hello, world!</h1>;
  return element
}
"""

test_tsx: sourcetypes.tsx = """
  function() {
    const element = <h1>Hello, world!</h1>;
    return element
  }
"""

test_python: sourcetypes.python = """
  test = "123"
  def my_function():
      return f"My string: {test}"
"""

test_sql2: sourcetypes.sql = """
    SELECT test
    FROM a_table
"""

test_html2: "html" = """
  <html>
    <body>
      <h1>Inline syntax highlighting</h1>
    </body>
  </html>
"""

test_cpp: "cpp" = """
int main() {
  cout << "Hello World!";
  return 0;
}
"""

test_hpp: "hpp" = """
#ifndef MY_HEADER_H
#define MY_HEADER_H

void myCFunction() ;

#endif // MY_HEADER_H
"""

test_rust: "rust" = """
fn main() {
    println!("Hello, world!");
}
"""

test_golang: "golang" = \
"""
package main
import "fmt"
func main() {
    fmt.Println("hello world")
}
"""

test_py2: sourcetypes.py = "print(x)"
test_py3: sourcetypes.py = """print(x)"""

test_lsp2: sourcetypes.trs = \
"""
(function_definition
  name: (identifier) @function.name
  parameters: (parameters
    (typed_parameter
      (asterisk)  # Match the variadic argument (*nums)
      (identifier) @param.name  # Capture the name of the variadic parameter
      type: (type (identifier) 
        (#eq? "int")  # The type is int
      )
    )
  )
  return_type: (type (identifier) 
    (#eq? "int")  # The return type is int
  )
  body: (block) @function.body  # Match the body of the function (a block of statements)
)
"""