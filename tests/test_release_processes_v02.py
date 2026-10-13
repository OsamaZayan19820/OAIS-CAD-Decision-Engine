"""Cross-process publication competition on a local filesystem."""
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from oais_cad.verify_release_v02 import verify_release

def _worker(target, ready, start):
    from oais_cad.publish_solids_v02 import publish_solid_plan
    from oais_cad.v02 import IntentError
    spec={"units":"mm","walls":[{"id":"A","start":[0,0],"end":[1000,0],"thickness":200}],"openings":[]}
    ready.put(1)
    if not start.wait(20):
        return "TIMEOUT"
    try:
        publish_solid_plan(spec,target)
        return "PUBLISHED"
    except IntentError:
        return "REJECTED"

def test_independent_processes_compete_for_one_release(tmp_path):
    ctx=mp.get_context("spawn")
    target=str(tmp_path/"release")
    with ctx.Manager() as manager:
        ready=manager.Queue()
        start=manager.Event()
        with ProcessPoolExecutor(max_workers=2,mp_context=ctx) as pool:
            jobs=[pool.submit(_worker,target,ready,start) for _ in range(2)]
            ready.get(timeout=20)
            ready.get(timeout=20)
            start.set()
            outcomes=[job.result(timeout=30) for job in jobs]
    assert sorted(outcomes)==["PUBLISHED","REJECTED"]
    assert verify_release(Path(target))["verified"] is True
