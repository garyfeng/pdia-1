def MathMLExtraction(s):
    """
    Takes a MathML expression as string, returns the last mn or mo value.

    To-do: @@ this is a very rough implementation based on string operations. Should have parsed the mathML

    :param s: mathML string with mo or mn components
    :return: the value of the last mn or mo element
    """
    if(s.find('</mn></math>') != -1):
        length = len(s.split('</mn></math>')[0].rsplit('<mn>',1))
        return s.split('</mn></math>')[0].rsplit('<mn>', 1)[length - 1]
    elif(s.find('</mo></math>') != -1):
        length = len(s.split('</mo></math>')[0].rsplit('<mo>',1))
        return s.split('</mo></math>')[0].rsplit('<mo>', 1)[length - 1]
