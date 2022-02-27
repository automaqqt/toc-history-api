import concurrent.futures, time, inspect
from utils.nodes import History
from config import wanted_actions
from disclog import postLog

class TrainManager:
    def __init__(
        self,
        worker = 1,
        posrr = 1896127,
        posm = 1896127
    ):
        self.worker = worker
        self.posrr = posrr
        self.posm = posm
        self.out = []
        self.sess = History(server="https://wax.greymass.com")   
    
    def thread(self, n):
        try:
            resp2 = self.sess.get_actions(account_name="m.century",pos=self.posm).json()["actions"]
            
            time.sleep(0.5)
            resp = self.sess.get_actions(account_name="rr.century",pos=self.posrr).json()["actions"]

            for res in resp:
                if res["action_trace"]["act"]["name"] in wanted_actions:
                    self.out.append(res)
            
            for res2 in resp2:
                if res2["action_trace"]["act"]["name"] in ["usefuel","buyfuel"]:
                    self.out.append(res2)

            self.posrr+=len(resp)
            self.posm+=len(resp2)

        except Exception as e:
            postLog(e,"warn",f"{inspect.stack()[0][3]}:{inspect.stack()[0][2]}")

        if len(resp) == 0:
            time.sleep(2)
        
        
    def fetch(self):
        start=time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.worker) as executor:
            for index in range(self.worker):
                executor.submit(self.thread, index)

        if time.time()-start < 0.5:
            time.sleep(0.6-(time.time()-start))
        
        
            

