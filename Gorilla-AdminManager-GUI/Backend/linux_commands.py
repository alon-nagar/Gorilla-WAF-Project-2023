import subprocess
import requests

WAF_PORT = 3333

class LinuxCMD:
    """Class that handles linux commands and their outputs."""
    
    def __init__(self):
        self.__process = None
        
    
    def start_waf(self):
        """Function to start the WAF Python script in the background.

        Returns:
            str: "WAF started" if the WAF was started successfully, otherwise an error message.
        """
        command = "nohup python3 ../Gorilla-ScanSoftware/main.py &"
        self.__process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        return "WAF started"
    
    
    def stop_waf(self):
        """Function to stop the WAF Python script.
        
        Returns:
            str: "WAF stopped" if the WAF was stopped successfully, otherwise an error message.
        """
        if self.__process is not None:
            try:
                self.__process.kill()
            except OSError as e:
                return f"Failed to stop WAF: {e}"
            else:
                if self.__process.returncode is None:
                    return "WAF stopped"
                else:
                    return f"WAF had already terminated with return code {self.__process.returncode}"
        else:
            return "WAF is not running"
    
    
    def get_waf_status(self):
        """Function to check if the WAF is on or off.

        Returns:
            str: "WAF is on" if the WAF is on, otherwise "WAF is off".
        """
        waf_url = f"http://localhost:{WAF_PORT}"

        # Send an HTTP GET request to the server and check the response status code
        try:
            response = requests.get(waf_url)
            return "WAF is on"
        except requests.exceptions.ConnectionError:
            return "WAF is off"
        