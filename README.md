# Gorilla-WAF-Project-2023
## Installation Guide (Ubuntu)
### Requirements:
- A server on a specific port, that server your vulnerable Web App.
### Step 1 - Download Nginx and NJS:
- Write the following commands, to configure the Nginx JavaScript Modules (NJS) on your machine:
```bash
>>> sudo apt install curl gnupg2 ca-certificates lsb-release ubuntu-keyring
>>> curl https://nginx.org/keys/nginx_signing.key | gpg --dearmor \
    | sudo tee /usr/share/keyrings/nginx-archive-keyring.gpg >/dev/null
>>> gpg --dry-run --quiet --no-keyring --import --import-options import-show /usr/share/keyrings/nginx-archive-keyring.gpg
>>> echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
http://nginx.org/packages/ubuntu `lsb_release -cs` nginx" \
    | sudo tee /etc/apt/sources.list.d/nginx.list
>>> echo -e "Package: *\nPin: origin nginx.org\nPin: release o=nginx\nPin-Priority: 900\n" \
    | sudo tee /etc/apt/preferences.d/99nginx
```
Source: https://nginx.org/en/linux_packages.html#Ubuntu
- Update your APT and install Nginx with NJS:
```bash
>>> sudo apt update
>>> sudo apt install nginx
>>> sudo apt install nginx-module-njs
```
The output should be something like this:
```
----------------------------------------------------------------------
The njs dynamic modules for nginx have been installed.
To enable these modules, add the following to /etc/nginx/nginx.conf
and reload nginx:

    load_module modules/ngx_http_js_module.so;
    load_module modules/ngx_stream_js_module.so;

Please refer to the modules documentation for further details:
https://nginx.org/en/docs/njs/
https://nginx.org/en/docs/http/ngx_http_js_module.html
https://nginx.org/en/docs/stream/ngx_stream_js_module.html
----------------------------------------------------------------------
```
### Step 2 - Configure the configuration files:
- Go to `/etc/nginx/nginx.conf` and add this line at the beginning:
```
load_module /usr/lib/nginx/modules/ngx_http_js_module.so;
```
- Restart Nginx (`sudo service nginx restart`) [Verify the Nginx default page].
- Go to `/etc/nginx/conf.d/default.conf` and replace it with this content:
```nginx
# Import the folder that contains the JS module' files:
js_path "/home/alon-nagar/Gorilla-WAF-Project-2023";

# Import the specific module file, that contains the function we want to run each request:
js_import waf.js;

# Set as a variable the return value of main() function in waf.js file:
js_set $return_value_of_main_func_in_waf waf.main;

# Convert it to a log_format:
log_format ret_val $return_value_of_main_func_in_waf;

resolver 127.0.0.1:3333;

server
{

    # Define the port and server_name that the NGINX is listening on:
    listen        80;
    server_name   localhost;

    # Write the main() return value to a new log file, named "njs_output.log":
    access_log  /var/log/nginx/njs_output.log ret_val;

    # Each request come to this location directive, and the main() function in waf.js is performed on it:
    location / {
        js_content waf.main;
    }

    # If the waf.js decided that the request is blocked, it'll send it to this location directive, that contains the "block.html" file:
    location /block.html {
        root  /home/alon-nagar/Gorilla-WAF-Project-2023/block-pages;
    }

    location /block_blacklisted.html {
        root  /home/alon-nagar/Gorilla-WAF-Project-2023/block-pages;
    }

    # If the waf.js decided that the request is valid to pass to the actual server, it'll send it to this location directive, that contains the actual backend and serve the clients:
    location @app-backend {
        proxy_pass http://127.0.0.1:7777;
    }

    # Redirect server error pages to the static page /50x.html:
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

}
```
