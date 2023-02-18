import dataclasses
from typing import List, Dict


@dataclasses.dataclass
class Metric:
    name: str
    labels: Dict[str, str] = dataclasses.field(default_factory=dict)
    value: float = None
    ts: int = None

    def __eq__(self, other):
        if type(other) != Metric:
            return False

        if self.name == other.name:
            if self.labels == other.labels:
                return True

        return False


metrics_cache: List[Metric] = []

from aiohttp import web


def format_line(m: Metric) -> str:
    labels_str = ','.join([f'{k}="{v}"' for k, v in m.labels.items()])
    labels_str = f"{{{labels_str}}}"
    return f"{m.name}{labels_str} {m.value} {m.ts}"


async def render_metrics(request):
    lines = ["# HELP mikrotik_cpu_profiler Profiler CPU", "# TYPE mikrotik_cpu_profiler gauge"]
    lines.extend([format_line(m) for m in metrics_cache])
    resp = web.Response(body='\n'.join(lines))
    resp.content_type = 'text/plain; version=0.0.4; charset=utf-8'
    return resp
