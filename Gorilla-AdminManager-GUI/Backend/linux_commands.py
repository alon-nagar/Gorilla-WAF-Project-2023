import subprocess


class LinuxCMD:
    """Class that handles linux commands and their outputs."""
    
    def __init__(self):
        self.__process = None
        
    
    def __del__(self):
        self.stop_waf()
     
        
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
        try:
            self.__process.kill()
        except OSError as e:
            return f"Failed to stop WAF: {e}"
        else:
            if self.__process.returncode is None:
                return "WAF stopped"
            else:
                return f"WAF had already terminated with return code {self.__process.returncode}"
    