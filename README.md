# toughbt

toughbt 是一个基于Python/twisted开发的 radius 服务性能测试工具。

## 运行环境

    - Linux/Mac OSX/BSD
    - ZMQ
    - Python 2.7/PyPy
    - easy_install/pip


## 安装

    pip install toughbt

## 使用说明

    $ trbctl -h

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

    $ trbctl --auth -m -u trbtest -p 888888 -n 10000 -c 100 -f 2 -i 5 -r 500 -t 1000

    benckmark worker created! master pid - 78933, worker pid - 78937
    benckmark worker created! master pid - 78933, worker pid - 78938
    write worker 78938 log into /tmp/trbctl-worker-1.log
    write worker 78937 log into /tmp/trbctl-worker-0.log
    ...........
    ...........
    ...........
    ...........
    ...........
    ...........
    ------------------ radius auth benchmark statistics result ----------------------
    -
    - Benchmark params
    -
    - Client platform                   :  Darwin-15.3.0-x86_64-i386-64bit, x86_64
    - Python implement, version         :  PyPy, 2.7.9
    - Radius server  address            :  127.0.0.1
    - Radius Server auth port           :  1812
    - Raduius share secret              :  secret
    - Auth Request total                :  10000
    - Concurrency level                 :  100
    - Worker Process num                :  2
    - All Requests timeout              :  1000 sec
    - Stat data interval                :  5 sec
    - Send request rate                 :  500/sec
    -
    - Time data statistics
    -
    - Current stat datetime             :  Sat Mar 19 19:09:54 2016
    - Current sent request              :  10000
    - Current received response         :  10000
    - Current accepts response          :  9992
    - Current rejects response          :  8
    - Current error response            :  0
    - Current requests per second       :  373.312449622, cast 3.75824594498 sec
    - Current max requests per second   :  502.08186488, cast 5.01711010933 sec
    - Current time per request          :  2.67872127226 ms
    - Current min time per request      :  1.99170707 ms
    - Current max time per request      :  35.0688480669 ms
    - Current Cast total seconds        :  28.886922121 sec
    --------------------------------------------------------------------------------- 





