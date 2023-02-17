from aiorosapi.protocol import RosApiProtocol, create_ros_connection
from metrics import metrics_cache, Metric


def get_prometheus_utc_ts():
    import datetime
    return int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp() * 1000)


class Profiler:
    METRIC_NAME = 'mikrotik_cpu_profiler'

    def __init__(self, host, username, password, profile_duration = 10, labels_const={}):
        self._host = host
        self._username = username
        self._password = password
        self._profile_duration = profile_duration
        self._labels_const = labels_const

    async def _con(self) -> RosApiProtocol:
        connection = await create_ros_connection(
            host=self._host,
            username=self._username,
            password=self._password,
            port=8728,
        )
        return connection

    async def start(self):
        while True:
            con = await self._con()
            profiler_task = con.talk_all('/tool/profile', attrs={'duration': str(self._profile_duration)})
            profile = await profiler_task
            profile_summery = self._parse_profiler_results_max(profile)
            now = get_prometheus_utc_ts()

            for service, usage in profile_summery.items():
                # see Metric.__eq__
                new_m = Metric(
                    name=self.METRIC_NAME,              # eq
                    labels_const=self._labels_const,    # eq
                    labels_dyn={'service': service},    # eq keys()
                    value=usage,                        # -
                    ts=now)                             # -
                if new_m in metrics_cache:
                    metrics_cache.remove(new_m)
                    metrics_cache.append(new_m)
                else:
                    metrics_cache.append(new_m)

    @staticmethod
    def _parse_profiler_results_max(profiler_results: dict) -> dict:
        '''parse distinct max service usage from profiler results'''
        profile_summery = {}
        for p in reversed(profiler_results):
            serv = p.get('name')
            usage = float(p.get('usage'))
            if serv == 'total':
                continue  # exclude total to aggregate by promql
            if serv not in profile_summery.keys() or usage > profile_summery[serv]:
                profile_summery[serv] = usage
        return profile_summery
