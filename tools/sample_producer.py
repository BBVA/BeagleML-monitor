from confluent_kafka import Producer
import threading
import time



EXPERIMENTS_TOPIC="experiments"

class metricSimulator (threading.Thread):
    def __init__(self, threadID, expMetricName, pace, producer):
        threading.Thread.__init__(self)
        self.threadID=threadID
        self.expMetricName=expMetricName
        self.pace=pace
        self.producer=producer


    def run(self):
        print("Thread running")
        self.announce()
        self.produce()

    def announce(self):
        print("Thread: " + repr(self.threadID) + " Comunicating experiment ...")
        self.producer.produce(EXPERIMENTS_TOPIC, self.expMetricName)
        self.producer.flush()
        print("Thread: " + repr(self.threadID) + " done")

    def produce(self):
        print("Thread: " + repr(self.threadID) + " producing on metric: " + self.expMetricName)
        for i in range(10):
            msg= "Thread: " + repr(self.threadID) + " msg: " + repr(i)
            self.producer.produce(self.expMetricName, msg)
            print("sent: " + msg)
            self.producer.flush()
            time.sleep(self.pace)
        self.producer.produce(self.expMetricName, "<STOP>")
        self.producer.flush()
        

def main():
    p = Producer({'bootstrap.servers': '10.41.35.153'})
    threads=[]

    MAX_T=10
    for i in range(MAX_T):
        t=metricSimulator(i, "experiment_" + repr(i), 10, p)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    
    

if __name__ =="__main__":
    main()

