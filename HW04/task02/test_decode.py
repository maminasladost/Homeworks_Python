from morse import decode
import pytest


@pytest.mark.parametrize(
    'morse_code, text',
    [
        ('.... .. -- -.-- -. .- -- . .. ... -. .. -.- .. - --- ... .. -.-',
         'HIMYNAMEISNIKITOSIK'),
        ('---.. -....- ---.. ----- ----- -....- ..... ..... ..... -....- \
            ...-- ..... -....- ...-- .....', '8-800-555-35-35'),
        ('-.. --- -. --- - -.-. .- .-.. .-.. -- . .--- ..- ... - - \
            . -..- - -- .',
         'DONOTCALLMEJUSTTEXTME')
    ]
)
def test_decode(morse_code, text):
    assert decode(morse_code) == text
