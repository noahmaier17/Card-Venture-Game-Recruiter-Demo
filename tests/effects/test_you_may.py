import copy

import pytest
import pytest_timeout

from Dinosaur_Venture import gameplay_scripted_input as scriptInput
from Dinosaur_Venture import helper as h


@pytest.mark.parametrize(
    "expected_value, input_array",
    [
        (True, ["y"]),
        (True, ["yes"]),
        (True, ["gibberish input", "y"]),
        (True, ["more gibberish input", "yes"]),   
        (False, ["n"]),
        (False, ["no"]),
        (False, ["sadkfjskadfjasdkfjalwesjfkasfj", "n"]),
        (False, ["wieurwjfdskansdfalk", "no"]),   
    ]
)
@pytest.mark.parametrize(
    "input_string",
    [
        ("Discard your Hand?"),
        ("Do this thing?")
    ]
)
@pytest.mark.timeout(5)
def test_yesOrNo(expected_value, input_array, input_string):
    """
        Tests:
        1. Does helper.yesOrNo work correctly?
    """
    
    gameplayScriptInput = scriptInput.gameplayScriptInput(copy.copy(input_array))
    assert expected_value == h.yesOrNo(input_string, scriptedInput=gameplayScriptInput)