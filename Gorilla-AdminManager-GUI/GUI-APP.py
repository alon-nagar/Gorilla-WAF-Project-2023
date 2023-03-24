import os, signal
import webbrowser
import subprocess

print("""
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@(.          ,%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@          @%         /@          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#******/**@@@@@@@@@@@@@@@@@@@@@#                      #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@          (@          @,         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&(*/**/**/*****/**/@@@@@@@@@@@@@@@@@#                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@(          @,         %&          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@@@@@@@@@@@&/**//////////////////***(@@@@@@@@@@@@@@@/            ,&@@@@@/      &@@@@@@@(         /@@@@@&*********#@%/,,*#@@@@@@@@@@         .@          @@@%*            #@@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@@@@%/*****/*/*/*/***************/***#@@@@@@@@@@@@@          ,@@@@@@@@@@@@@   ,@@@&                  @@                         /@.         @#         /@                   *@@@@@@@@@@@@
    @@@@@@@@@@@@@@@(//*/****//*/*/**/*******/*****/***(&@@@@@@@@@@@@(         /@@@@@@@@@@@@@@@@@@@@,                     (                         @%         .@          @(      ...           %@@@@@@@@@@@
    @@@@@@@@@@@@@@@@////************/**************/@@@@@@@@@@@@@@@(         &@@@               ,&          @@@*                   .&@%           %@          @*         %@.*@@@@@&#*.          @@@@@@@@@@@@
    @@@@@@@@@@@@@@@(@***/***/**////*/////***/*/*/**/@@@@@@@@@@@@@@@//       ,%%@&//             %%@        *,@@@@&       .          @@@@//        %//*       /% /        %%@@&                  . @@@@@@@@@@
    @@@@@@@@@@@@@@@(*@*/******&&&&&&&&&&&&&&&&**/**/@@@@@@@@@@@@@@@@@         .@@@               ..         &@@@@                  /@@@@@/         /@.         @(         (                      %@@@@@@@@@@
    @@@@@@@@@@@@@@@(**@*/*****@@@@@@@@@@@@@@@@***/*/@@@@@@@@@@@@@@@@@          *@@@@@@@          @          @@@@                   @@@@@@          @#         .@                   @@@@         .@@@@@@@@@@@
    @@@@@@@@@@@@@@**/**@******@@@@@@@@@@@@@@@@*****/@@@@@@@@@@@@@@@@@&                          ,@                                %@@@@@,         %@          @,                   .@#          @@@@@@@@@@@@
    @@@@@@@@@@@&**/**&@*/*/**@@@@@@@@@@@@@@@@#*//**/@@@@@@@@@@@@@@@@@@@                         @@@                    @          @@@@@@          @*         %@          &                     ,@@@@@@@@@@@@
    @@@@@@@@@(*/***@@@/*****@@@@@@@@@@@@@@@@@*/****/@@@@@@@@@@@@@@@@@@@@@@                   &@@@@@@@/             %@@@,         &@@@@@          @@          @          @@@@.                  @@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@""")

print("""
      This script is trying to do the best to open the GUI app.
      There may be errors due to the system you are using.
      
      If you are using WSL, please enter the distro name correctly.
      If you are using Linux, please make sure that you have installed Google Chrome.
      
      The browser default location is "C:\Program Files\Google\Chrome\Application\chrome.exe".
      If you are using a different browser/location, please change the path in the script (line 40).
      
      Please note that you can hit Ctrl+C to stop the script at any time.
""")

html_file_path = os.path.abspath("Frontend/index.html")

# Generate different paths for different systems:
system_preference = input("Are you using WSL? (y for yes): ")
if system_preference == "y":
    os.environ['BROWSER'] = "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
    distro_name = input("Enter your distro name: ")
    gui_app_path = f"file://wsl.localhost/{distro_name}/{html_file_path}"

else:
    gui_app_path = f"file://{html_file_path}"


# Open the GUI app in the browser:
print(f"Opening {gui_app_path}...")
try:
    webbrowser.open(gui_app_path)
except Exception as e:
    print("Error: ", e)
    

# Run the backend server:
command = "nohup python3 Backend/db_flask_server.py &"
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

# Register the signal handler function to stop the process on Ctrl+C
def signal_handler(sig, frame):
    print("Stopping the backend server...")
    process.kill()
    print("Backend server stopped.")
    print("Bye!")

signal.signal(signal.SIGINT, signal_handler)

# Capture the output and error of the process
output, error = process.communicate()

if error:
    print(f"Error: {error.decode()}")
else:
    print(output.decode())
    