import asyncio
import time

from aiorosapi.protocol import RosApiProtocol, create_ros_connection
from aiorosapi.exceptions import RosApiException
from metrics import metrics_cache, Metric


def get_prometheus_utc_ts():
    import datetime
    return int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp() * 1000)


class Profiler:
    METRIC_NAME = 'mikrotik_cpu_profiler'

    def __init__(self, host, username, password, profile_duration=5, labels_const={}):
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
            print('profile stasrt')
            t0 = time.time()
            try:
                await self._profile()
            except RosApiException as rae:
                print(f'{rae}')
            except Exception as e:
                print(f'{e}')
            finally:
                dur = time.time() - t0
                sleep = self._profile_duration - dur
                if sleep > 0:
                    print(f'wait {sleep}')
                    await asyncio.sleep(sleep)
            print('profile done')

    async def _profile(self):
        con = await self._con()
        profiler_task = con.talk_all('/tool/profile', attrs={'duration': str(self._profile_duration)})
        profile = await profiler_task
        profile_summery = self._parse_profiler_results_max(profile)
        now = get_prometheus_utc_ts()

        for service, usage in profile_summery.items():
            # see Metric.__eq__
            new_m = Metric(
                name=self.METRIC_NAME,  # eq
                labels={**self._labels_const, 'service': service},  # eq
                value=usage,  # -
                ts=now)  # -
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
