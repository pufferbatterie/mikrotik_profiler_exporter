mikrotik_profiler_exporter
==========================

perodically starts /tool/profile for [profile_duration](mikrotik_profiler_exporter.json5) seconds and publishes the result in prometheus text format with timestamp. 


```
MacBook-Pro-von-Markus % docker run --rm -it -p49091:49091 mikrotik_profiler_exporter
started profiling task for mymictrod - 172.30.10.1 with dur 20
/metrics endpoint started on port 49091
wait forever
```

Output:
```
mikrotik_cpu_profiler{routerboard_address="172.30.10.1",routerboard_name="mymictrod",radv="0.5"} 0.5 1676674951530
mikrotik_cpu_profiler{routerboard_address="172.30.10.1",routerboard_name="mymictrod",bridging="0.5"} 0.5 1676674951530
mikrotik_cpu_profiler{routerboard_address="172.30.10.1",routerboard_name="mymictrod",queuing="0.0"} 0.0 1676674971762
mikrotik_cpu_profiler{routerboard_address="172.30.10.1",routerboard_name="mymictrod",certificate="0.0"} 0.0 1676674992082
mikrotik_cpu_profiler{routerboard_address="172.30.10.1",routerboard_name="mymictrod",unclassified="1.0"} 1.0 1676675012306
mikrotik_cpu_profiler{routerboard_address="172.30.10.1",routerboard_name="mymictrod",profiling="0.5"} 0.5 1676675012306
mikrotik_cpu_profiler{routerboard_address="172.30.10.1",routerboard_name="mymictrod",routing="0.5"} 0.5 1676675012306
mikrotik_cpu_profiler{routerboard_address="172.30.10.1",routerboard_name="mymictrod",wireless="1.0"} 1.0 1676675012306
mikrotik_cpu_profiler{routerboard_address="172.30.10.1",routerboard_name="mymictrod",management="1.5"} 1.5 1676675012306
mikrotik_cpu_profiler{routerboard_address="172.30.10.1",routerboard_name="mymictrod",firewall="0.5"} 0.5 1676675012306
mikrotik_cpu_profiler{routerboard_address="172.30.10.1",routerboard_name="mymictrod",console="1.0"} 1.0 1676675012306
mikrotik_cpu_profiler{routerboard_address="172.30.10.1",routerboard_name="mymictrod",wireguard="0.5"} 0.5 1676675012306
mikrotik_cpu_profiler{routerboard_address="172.30.10.1",routerboard_name="mymictrod",ppp="0.5"} 0.5 1676675012306
mikrotik_cpu_profiler{routerboard_address="172.30.10.1",routerboard_name="mymictrod",internet-detect="0.5"} 0.5 1676675012306
mikrotik_cpu_profiler{routerboard_address="172.30.10.1",routerboard_name="mymictrod",networking="0.5"} 0.5 1676675012306
mikrotik_cpu_profiler{routerboard_address="172.30.10.1",routerboard_name="mymictrod",ssl="0.0"} 0.0 1676675012306
mikrotik_cpu_profiler{routerboard_address="172.30.10.1",routerboard_name="mymictrod",dns="0.0"} 0.0 1676675012306
mikrotik_cpu_profiler{routerboard_address="172.30.10.1",routerboard_name="mymictrod",ethernet="0.0"} 0.0 1676675012306
```