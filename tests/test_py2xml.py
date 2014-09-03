
import xml.etree.ElementTree as ET

import pytest

from pyreg.py2xml import py2xml, xml2py


@pytest.fixture
def s2xml(tmpdir):
    """return fixture function to easy convertion of python code to XML"""
    def py_str2xml(string, strip_body=True):
        p = tmpdir.join("x.py")
        p.write(string)
        result = py2xml(p.strpath)
        if strip_body:
            # the slice 14:-16 is to remove the string of
            # the module and body tags: <Module><body> ... </body></Module>
            return result[14:-16]
        return result
    return py_str2xml


class TestSimpleExpressions:
    def test_num(self, s2xml):
        assert s2xml('6') == '<Expr><Num>6</Num></Expr>'

    def test_str(self, s2xml):
        assert s2xml('"my string"') == '<Expr><Str><s>"my string"</s></Str></Expr>'
        assert s2xml("'''my 2'''") == "<Expr><Str><s>'''my 2'''</s></Str></Expr>"

    def test_str_multiline(self, s2xml):
        string = '''"""line 1
line 2""" '''
        assert s2xml(string) == '<Expr><Str><s>"""line 1\nline 2"""</s></Str></Expr>'

    def test_str_implicit_concat(self, s2xml):
        string = "'part 1' ' /part 2'"
        assert s2xml(string) == "<Expr><Str><s>'part 1'</s><space> </space><s>' /part 2'</s></Str></Expr>"

    def test_str_implicit_concat_line_continuation(self, s2xml):
        string = r"""'part 1'  \
 ' /part 2'"""
        assert s2xml(string) == "<Expr><Str><s>'part 1'</s><space>  \\\n</space><s>' /part 2'</s></Str></Expr>"

    def test_tuple(self, s2xml):
        assert s2xml('(1,2,3)') == '<Expr><Tuple ctx="Load"><delimiter>(</delimiter><Num>1</Num><delimiter>,</delimiter><Num>2</Num><delimiter>,</delimiter><Num>3</Num><delimiter>)</delimiter></Tuple></Expr>'

    def test_tuple_space(self, s2xml):
        assert s2xml('(  1, 2,3 )') == '<Expr><Tuple ctx="Load"><delimiter>(  </delimiter><Num>1</Num><delimiter>, </delimiter><Num>2</Num><delimiter>,</delimiter><Num>3</Num><delimiter> )</delimiter></Tuple></Expr>'



class TestExpressions:
    def test_binop_add(self, s2xml):
        assert s2xml('1 + 2') == \
            '<Expr><BinOp><Num>1</Num><Add> + </Add><Num>2</Num></BinOp></Expr>'

    def test_binop_add_space(self, s2xml):
        assert s2xml('3+  4') == \
            '<Expr><BinOp><Num>3</Num><Add>+  </Add><Num>4</Num></BinOp></Expr>'

class TestStatements:
    def test_assign(self, s2xml):
        assert s2xml('d = 5') == \
            '<Assign><targets><Name ctx="Store" name="d">d</Name></targets><delimiter> = </delimiter><Num>5</Num></Assign>'

    def test_assign_space(self, s2xml):
        assert s2xml('f  =   7') == \
            '<Assign><targets><Name ctx="Store" name="f">f</Name></targets><delimiter>  =   </delimiter><Num>7</Num></Assign>'





def test_xml2py():
    assert xml2py('<a>x<b>y</b>z</a>') == 'xyz'