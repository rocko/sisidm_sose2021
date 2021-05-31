# THIS NODE IS REQUESTING !!!!!!!!!!

import time
import logging
import grpc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from proto import service_pb2, service_pb2_grpc

# Address
#ADDRESS = "localhost:23333"
ADDRESS = "78.47.154.89:23333"

# Ping to address
ping = [20, 36, 20]  # min, max, avg

# Test time on server 
# date: Tue May 11 15:02:16 CEST 2021
# hwclock 2021-05-11 15:03:33.185262+0200
# date +%s 1620738268


# Name
NAME = "py node request"

# Duration in minutes
DURATION = 0.25

t_n = []  # diff between 
t_p = []
t_e = []
e_bmin = []
e_bmax = []
e_w = []
r_t = []
o_f = []

def t_network(t1, t2, t3, t4):
    return ((t2 - t1) + (t4 - t3)) / 2

def t_process(t2, t3):
    return t3 - t2

def t_estimate(t1, t2, t3, t4):
    return t3 + (t4 - t1 - t_process(t3, t2)) / 2

def error_band(t1, t2, t3, t4):
    tmin = t_network(t1, t2, t3, t4)
    error = (t3 + tmin, t3 + (t4 - t1) - tmin)
    return error

def error_width(t1, t2, t3, t4):
    tmin = t_network(t1, t2, t3, t4)
    return (t4 - t1) - (2 * tmin)

def rtt(t1, t2, t3, t4):
    return (t4 - t1) - (t2 - t3)

def t_offset(t1, t2, t3, t4):
    return ((t2 - t1) + (t3 - t4)) / 2

def cycle() -> None:
    # Service name = GetTime
    # Service rpc name = GimmeTime
    # Request name = TimeRequest
    # Response name = TimeResponse

    

    with grpc.insecure_channel(ADDRESS) as channel:
        idx = 0

        # Current time on the requester
        current_time = time.time()
        # Calculated time when the processing should end
        end_time = time.time() + (DURATION * 60)

        # Get Service
        stub = service_pb2_grpc.GetTimeStub(channel)
        # Get Response from service's RPC

        # Difference in timestamps
        offset = 0
        while (time.time() < end_time):
            # Time when request was sent
            # Set unreferenced monotonic timestamp
            t1 = time.time() #+ offset
            monotonic_1 = time.monotonic()
            print("request_sent", t1)
            # Syncronous call
            response = stub.GimmeTime(service_pb2.TimeRequest(req="gimme"))
            
            # Time when request was received on server          
            t2 = response.time_received
            # Time when request was processed and sent back on server
            t3 = response.time_sent
            #print("request_received", t2, "response_sent", t3)
            # Time when reply was received
            # Set unreferenced monotonic timestamp
            t4 = t1  + (time.monotonic() - monotonic_1) #+ offset
            print("response_received", t4)

            #print("lol", t4 - t1)

            # Calculations
            net = t_network(t1, t2, t3, t4)
            t_n.append(net)
            #print("t network", net)
            pro = t_process(t2, t3)
            t_p.append(pro)
            #print("t processing", pro)
            est = t_estimate(t1, t2, t3, t4)
            #print("t estimate", est)
            eb = error_band(t1, t2, t3, t4)
            e_bmin.append(eb[0])
            e_bmax.append(eb[1])
            #print("error band", eb)
            ew = error_width(t1, t2, t3, t4)
            e_w.append(ew)
            #print("width", ew)
            r = rtt(t1, t2, t3, t4)
            r_t.append(r)
            #print("rtt", r)
            offset = t_offset(t1, t2, t3, t4)
            o_f.append(offset)
            #print("offset", offset)
            #processing_time = response_sent - request_received
            #new_time = response_sent + (response_received - request_sent - processing_time) / 2
            #print("new time", new_time)


            # Difference between timestamps
            #diff = current_time - new_time
            #print("diff", diff)

            # Update current time on requester
            #print("old current_time", current_time)
            #current_time = new_time #response.time_received + rtt
            #print("current_time", current_time)
            #if idx > 1:
            #drift.append(diff)

            time.sleep(1)
            #idx += 1
            #print("time left", end_time - time.time())

    # Plotting

    x = list(range(0, len(t_n)))

    nrow = 2
    ncol = 2
 
    df_networking = pd.DataFrame({
        'data': t_n,
        'median': [np.median(t_n)] * len(t_n),
        'std': [np.std(t_n)] * len(t_n)
    })

    df_offset = pd.DataFrame({
        'data': o_f
    })

    df_rtt = pd.DataFrame({
        'data': r_t,
        'median': [np.median(r_t)] * len(r_t),
    })

    df_processing = pd.DataFrame({
        'data': t_p
    })

    df_list = [df_networking, df_offset, df_rtt, df_processing]
    df_titles = ["networking", "offset", "rtt", "processing"]
    _, axes = plt.subplots(nrow, ncol)

    count = 0
    for r in range(nrow):
        for c in range(ncol):
            df_list[count].plot(ax=axes[r, c], title=df_titles[count])
            count += 1

    #plt.plot(t_n)
    #t_n_med = [np.median(t_n)] * len(t_n)
    #t_n_std = [np.std(t_n)] * len(t_n)
    #plt.plot(t_n_med, linestyle='--', label='Median')
    #plt.plot(t_n_std, linestyle='--', label='Std')
    #plt.errorbar(x, t_n, yerr=t_n_std, fmt='-o')
    #plt.title("networking time")
    #plt.legend(loc='upper right')

    #plt.subplot(222)
    #plt.plot(o_f)
    #plt.title("offset")
    #plt.legend(loc='upper right')

    #plt.subplot(223)
    #plt.plot(r_t)
    #plt.title("rtt")
    #plt.legend(loc='upper right')

    #plt.subplot(224)
    #plt.plot(t_p)
    #plt.title("processing time")
    #plt.legend(loc='upper right')

    #plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25, wspace=0.35)
    
    #plt.plot(t_n)
    #plt.plot(t_p)
    #plt.plot(o_f)
    #plt.plot(r_t)

    # Plot stuff
    #y = drift
    #x = list(range(0, len(y)))
    #print("len x", len(x))
    #bins = len(x)

    # mean
    #mu = np.mean(y)*len(x)
    # std
    #std = np.std(y)*len(x)


    #print("x", x)
    #y_mean = [np.mean(y)]*len(x)
    #print("mean", y_mean[0])
    #y_median = [np.median(y)]*len(x)
    #print("median", y_median[0])
    #y_std = [np.std(y, axis=0)]*len(x)
    #print("std", y_std[0])

    #fig, ax = plt.subplots(1, 2, tight_layout=True)
    #ax[0].hist(y)
    #ax[0].set_xlabel("Wert")
    #ax[0].set_ylabel("Häufigkeit")
    #ax[1].hist(y, stacked=True, cumulative=True)
    #y_best = ((1 / (np.sqrt(2 * np.pi) * std)) * np.exp(-0.5 * (1 / std * (bins - mu))**2))
    #ax.plot(bins, y_best, '--')
    #ax.set_xlabel('Smarts')

    #data_line = ax.plot(x,y, label='Data')
    #mean_line = ax.plot(x,y_mean, label='Mean', linestyle='-')  # label=str(y_mean[0])
    #median_line = ax.plot(x,y_median, label='Median', linestyle='--')  # label=str(y_mean[0])
    #std_line = ax.plot(x,y_std, label='Deviation', linestyle=':')  # label=str(y_mean[0])
    #mean = np.mean(DIFFS)
    #median = np.median(DIFFS)
    #print("Mean", mean)
    #print("Median", median)
    #plt.plot(DIFFS)
    #plt.axvline(mean, color='r')
    #plt.ylabel('some numbers')

    #legend = ax.legend(loc='upper right')
    plt.show()

if __name__ == '__main__':
    # Time monotonic on windows differs from linux
    # Windows: namespace(implementation='GetTickCount64()', monotonic=True, adjustable=False, resolution=0.015625)
    # hence monotonic returns i.e 175151.89
    # Linux: namespace(adjustable=False, implementation='clock_gettime(CLOCK_MONOTONIC)', monotonic=True, resolution=1e-09)
    # hence monotonic return
    # and clock_gettime(clock.MONOTONIC) gives 0.15521452100000002

    logging.basicConfig()
    cycle()