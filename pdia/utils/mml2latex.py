import os
from lxml import etree

def mml2latex(equation, xslPath="mml-to-latex/lib/mmltex", xslFilename="mmltex.xsl"):
    """MathML to LaTeX conversion with XSLT from Vasil Yaroshevich (http://xsltml.sourceforge.net/)

    We use an implementation at https://github.com/ets-interactive/mml-to-latex.
    The XSLT directory is assumed to be under the xslPath. It returns None if anything fails
    in the conversion. Also note that it retains the $ signs around the latex text.

    :param equation: a valid mathML string
    :param xslPath: the path to the XSLT files
    :param xslFilename: the name of the primary XSLT file
    :return: a string of latex, or None if anything fails
    """

    assert(isinstance(equation, str))

    try:
        xslt_file = os.path.join(xslPath, xslFilename)
        dom = etree.fromstring(equation)
        xslt = etree.parse(xslt_file)
        transform = etree.XSLT(xslt)
        newdom = transform(dom)
        res = str(newdom)
    except:
        res = None
    return res

# for unit testing

def test_mml2latex():
    mathml = """
    <math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>sin</mi><mrow><mo>-</mo><mn>1</mn></mrow></msup><mi>x</mi><mo>=</mo><msup><mi>cos</mi><mrow><mo>-</mo><mn>1</mn></mrow></msup><mi>x</mi><mo>=</mo><msup><mi>tan</mi><mrow><mo>-</mo><mn>1</mn></mrow></msup><mi>x</mi></math>
    """
    tex = mml2latex(mathml)
    assert(tex=="${\sin }^{-1}x={\cos }^{-1}x={\tan }^{-1}x$")