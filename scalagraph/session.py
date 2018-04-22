from typing import List
from scalagraph.op import Op
import json
import requests


class Session:
    def __init__(self, url='http://localhost:8080/query'):
        self.url = url

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def compile_to_json(self, outs: List[Op]):
        def collect_op(op: Op, ops: List[Op]) -> List[Op]:
            if op in ops:
                return ops
            elif op.inp is not None:
                return collect_op(op.inp, ops + [op])
            else:
                return ops + [op]

        def collect(outs: List[Op], ops: List[Op]) -> List[Op]:
            if len(outs) == 0:
                return ops
            else:
                return collect(outs[1:], collect_op(outs[0], ops))

        def compile_to_dict(graph: str, target: List[Op], ops: List[Op]):
            res = {
                "graph": graph,
                "target": [t.id for t in target],
                "ops": [{"id": o.id, "op": o.op, "args": o.args, "inp": o.inp.id if o.inp is not None else None}
                        for o in ops]
            }
            [o.pop("inp", None) for o in res["ops"] if o["inp"] is None]
            return res

        return json.dumps(compile_to_dict("abcd", outs, collect(outs, list())))

    def run(self, outs: List[Op]):
        data = self.compile_to_json(outs)
        resp = requests.post(
            self.url,
            headers={'Content-Type': 'application/json'},
            data=data
        )
        return resp.json()['data']
