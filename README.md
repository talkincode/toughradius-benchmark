# toughbt

toughbt 是一个基于Python/twisted开发的 radius 服务性能测试工具。

## 运行环境

    - Linux/Mac OSX/BSD
    - ZMQ
    - Python 2.7/PyPy
    - easy_install/pip


## 安装

    pip install toughbt -r requirements.txt

## 使用说明

    $ pypy trbctl -h

    usage: trbctl [-h] [-auth] [-acct] [-m] [-w] [-s SERVER] [-P PORT] [-e SECRET]
              [-u USERNAME] [-p PASSWORD] [-n REQUESTS] [-c CONCURRENCY] [-v]
              [-t TIMEOUT] [-f FORK] [-i INTERVAL] [-r RATE] [-conf CONF]

    optional arguments:
    -h, --help            show this help message and exit
    -auth, --auth         Run radius auth test
    -acct, --acct         Run radius acct test
    -m, --master          Run benchmark master
    -w, --worker          Run benchmark worker
    -s SERVER, --server SERVER
                        Radius server address
    -P PORT, --port PORT  Radius server auth port or acct port
    -e SECRET, --secret SECRET
                        Radius testing share secret
    -u USERNAME, --username USERNAME
                        Radius testing username
    -p PASSWORD, --password PASSWORD
                        Radius testing password
    -n REQUESTS, --requests REQUESTS
                        Number of requests to perform
    -c CONCURRENCY, --concurrency CONCURRENCY
                        Number of multiple requests to make at a time
    -v, --verbosity       How much troubleshooting info to print
    -t TIMEOUT, --timeout TIMEOUT
                        Seconds to max. wait for all response
    -f FORK, --fork FORK  Fork worker process nums, default 1
    -i INTERVAL, --interval INTERVAL
                        Stat data interval, default 2 sec
    -r RATE, --rate RATE  Max send message rate , default 5000 per process
    -conf CONF, --conf CONF
                        Radius testing config file


## 示例

    $ pypy trbctl --auth -m -u trbtest -p 888888 -n 10000 -c 100 -f 4 -i 5 -r 200 -t 1000
    2016-03-19 18:55:51+0800 [-] Log opened.
    2016-03-19 18:55:51+0800 [-] benckmark worker created! master pid - 78655, worker pid - 78659
    2016-03-19 18:55:51+0800 [-] benckmark worker created! master pid - 78655, worker pid - 78660
    2016-03-19 18:55:51+0800 [-] benckmark worker created! master pid - 78655, worker pid - 78661
    2016-03-19 18:55:51+0800 [-] benckmark worker created! master pid - 78655, worker pid - 78662
    2016-03-19 18:55:53+0800 [-] write worker 78660 log into /tmp/trbctl-worker-1.log
    2016-03-19 18:55:53+0800 [-] write worker 78659 log into /tmp/trbctl-worker-0.log
    2016-03-19 18:55:53+0800 [-] write worker 78661 log into /tmp/trbctl-worker-2.log
    2016-03-19 18:55:53+0800 [-] write worker 78662 log into /tmp/trbctl-worker-3.log
    ...........
    ...........
    ...........
    ...........
    ...........
    ...........
    2016-03-19 18:56:26+0800 [-]  ------------------ radius auth benchmark statistics result ----------------------
    2016-03-19 18:56:26+0800 [-]  -
    2016-03-19 18:56:26+0800 [-]  - Benchmark params
    2016-03-19 18:56:26+0800 [-]  -
    2016-03-19 18:56:26+0800 [-]  - Client platform                   :  Darwin-15.3.0-x86_64-i386-64bit, x86_64
    2016-03-19 18:56:26+0800 [-]  - Python implement, version         :  PyPy, 2.7.9
    2016-03-19 18:56:26+0800 [-]  - Radius server  address            :  127.0.0.1
    2016-03-19 18:56:26+0800 [-]  - Radius Server auth port           :  1812
    2016-03-19 18:56:26+0800 [-]  - Raduius share secret              :  secret
    2016-03-19 18:56:26+0800 [-]  - Auth Request total                :  10000
    2016-03-19 18:56:26+0800 [-]  - Concurrency level                 :  100
    2016-03-19 18:56:26+0800 [-]  - Worker Process num                :  4
    2016-03-19 18:56:26+0800 [-]  - All Requests timeout              :  1000 sec
    2016-03-19 18:56:26+0800 [-]  - Stat data interval                :  5 sec
    2016-03-19 18:56:26+0800 [-]  - Send request rate                 :  200/sec
    2016-03-19 18:56:26+0800 [-]  -
    2016-03-19 18:56:26+0800 [-]  - Time data statistics
    2016-03-19 18:56:26+0800 [-]  -
    2016-03-19 18:56:26+0800 [-]  - Current stat datetime             :  Sat Mar 19 18:56:26 2016
    2016-03-19 18:56:26+0800 [-]  - Current sent request              :  10000
    2016-03-19 18:56:26+0800 [-]  - Current received response         :  10000
    2016-03-19 18:56:26+0800 [-]  - Current accepts response          :  9981
    2016-03-19 18:56:26+0800 [-]  - Current rejects response          :  19
    2016-03-19 18:56:26+0800 [-]  - Current error response            :  0
    2016-03-19 18:56:26+0800 [-]  - Current requests per second       :  236.072818989, cast 1.12677097321 sec
    2016-03-19 18:56:26+0800 [-]  - Current max requests per second   :  439.310067127, cast 5.01923394203 sec
    2016-03-19 18:56:26+0800 [-]  - Current time per request          :  4.23598110228 ms
    2016-03-19 18:56:26+0800 [-]  - Current min time per request      :  2.27629657235 ms
    2016-03-19 18:56:26+0800 [-]  - Current max time per request      :  38.7394464933 ms
    2016-03-19 18:56:26+0800 [-]  - Current Cast total seconds        :  31.2822549343 sec
    2016-03-19 18:56:26+0800 [-]  ---------------------------------------------------------------------------------    





