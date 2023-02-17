import asyncio
from metrics import render_metrics
from profiler import Profiler
from aiohttp import web
import json5


async def start_metrics_endpoint(port: int):
    app = web.Application()
    app.router.add_get('/metrics', render_metrics)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host='0.0.0.0', port=port)
    await site.start()


async def main():
    conf = json5.load(open('mikrotik_profiler_exporter.json5', 'r'))

    profile_duration = int(conf.get('settings').get('profile_duration'))

    for mt in conf.get('mikrotiks'):
        p = Profiler(host=mt.get('host'), username=mt.get('username'), password=mt.get('password'),
                     profile_duration=profile_duration,
                     labels_const={
                         'routerboard_address': mt.get('host'),
                         'routerboard_name': mt.get('name')
                     })
        asyncio.create_task(p.start())
        print(f"started profiling task for {mt.get('name')} - {mt.get('host')} with dur {profile_duration}")

    port = int(conf.get('settings').get('port'))
    await start_metrics_endpoint(port)
    print(f'/metrics endpoint started on port {port}')

    print('wait forever')
    while True:
        await asyncio.sleep(10)


if __name__ == '__main__':
    asyncio.run(main())
