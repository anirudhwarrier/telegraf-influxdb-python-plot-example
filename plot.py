import datetime as datetime

from influxdb_client import InfluxDBClient, Point, Dialect
from influxdb_client.client.write_api import SYNCHRONOUS
import seaborn
import matplotlib.pyplot as plt


with InfluxDBClient(
    url="http://localhost:8086", 
    token="mytoken", 
    org="myorg",
    debug=True) as client:

    write_api = client.write_api(write_options=SYNCHRONOUS)
    query_api = client.query_api()
    data_frame = query_api.query_data_frame('''
    from(bucket: "telegraf-metrics")
        |> range(start: -10m)
        |> filter(fn: (r) => r["_measurement"] == "docker_container_mem")
        |> filter(fn: (r) => r["_field"] == "usage_percent")
        |> filter(fn: (r) => r["container_name"] == "nginx")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value") 
    ''')
    
    print(data_frame)
    # seaborn.displot(data_frame)
    # plt.show()

    seaborn.lineplot(x='_time', y='usage_percent', data=data_frame)
    plt.xticks(rotation=30)
    plt.savefig('docker_container_mem.png')