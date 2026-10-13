import json
import pytest
from oais_cad.demo_v02 import main
from oais_cad.v02 import IntentError

def test_demo_end_to_end(tmp_path,capsys):
    out=tmp_path/"demo"
    assert main(["--out",str(out)])==0
    message=json.loads(capsys.readouterr().out)
    assert message["verification"]["verified"] is True
    assert message["verification"]["strip_count"]==2
    assert message["verification"]["architectural_approval"] is False
    with pytest.raises(IntentError,match="exists"):
        main(["--out",str(out)])
