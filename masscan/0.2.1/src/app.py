import subprocess
import json

from walkoff_app_sdk.app_base import AppBase

class MASSCAN(AppBase):
    __version__ = "0.2.1"
    app_name = "masscan"  # this needs to match "name" in api.yaml

    def __init__(self, redis, logger, console_logger=None):
        print("INIT")
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)
    
    def read_masscan_result_file(self, file_path:str):
        text = open(file_path, 'r').read()
        result = {}
        if len(text) == 0:
            return result
        json_data = json.loads(text)
        for data in json_data:
            if data['ip'] not in result:
                result[data['ip']] = data['ports']
            else:
                result[data['ip']].append(data['ports'])
        return result

    def scan(self, ip:str, port:str, rate:int):
        tmp_file = '/tmp/masscan.json'
        cmd_list = [
            'masscan',
            ip,
            '-p', str(port),
            '--rate', str(rate),
            '--output-format', 'json',
            '--output-file', tmp_file,
        ]
        process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=False)
        stdout = process.communicate()
        if len(stdout[0]) > 0:
            return {
                "success": False,
                "message": stdout[0],
            }
        else:
            return {
                "success": True,
                "message": self.read_masscan_result_file(tmp_file),
            }   

if __name__ == "__main__":
    MASSCAN.run()
