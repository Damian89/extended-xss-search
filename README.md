# Extended XSS Searcher and Finder

This is the extended version based on the initial idea already published as "xssfinder". This private version allows an attacker
to perform not only GET but also POST requests. Additionally its possible to proxy every request through Burp or another tunnel.

## First steps

Rename the __example.app-settings.conf__ to __app-settings.conf__ and adjust the settings. It should work out of the box but
depending on the target I would recommend to resize the chunk sizes.

## Execution

This tool does not expect any arguments via CLI, so just type:

python3 extended-xss-search.py

## Configuration

Its possible to set a lot of options and settings, so here are some explanations.

### Files

The main config file is the "app-settings.conf", everything has to be done in that file! Besides that, there are some 
other files which allow to set more complex data like headers, urls and cookies.

__config/cookie-jar.txt__

Use this file to add a cookie string. I usually copy the one which you can see in every burp request. Please just 
copy the value of the "Cookie:"-header. A sample input is in the default file.

__config/http-headers.txt__

This file defines the http headers which are added to the request and manipulated (payload is added to each one). The 
most important ones are already in the file. But feel free to add more.

__config/parameters.txt__

The tool has the option to brute force get and post parameters. In that case those parameters (+ those in the query 
string) will be used. Each parameter gets the payload as value. Most important are already in that file.

__config/urls-to-test.txt__

Thats the file you need! Please add here your links to scan. The following formats are allowed:

- https://domain.com
- https://domain.com/path
- https://domain.com/path?param=value&param1=value1
- domain.com

When the last case is detected an "http://" is prepended. This tool is intended to work with a good list of urls. A 
good way to get one is to just export it using burp. Then you have a valid list of urls. All you need to do ist to 
just add your cookies.

__logs/__

This is the log folder where everything gets logged to!

### Settings

The app-settings.conf defined the program workflow. Its the most important file, you can activate/deactive different 
modules there.

__Basic settings__

_HTTPTimeout_

Some requests can take long. Here you can define the max. execution time of one request. I recommend values between 2 
and 6 seconds.

_MaxThreads_

The more threads, the faster the script is - but since we are dealing with a lot of connections I usually keep this 
below 10 on my personal computer and arround 30 on my VPS.

__Attack types__

_OnlyBaseRequest_

Setting this to true will result in only "base requests" - this means the url lists is just spidered and interesting
parameters extracted. You could use that to fill you burp sitemap quickly.

_UsePost_

Use can skip POST requests setting this to "false"

_UseGet_

This is similar - skip GET requests if set to "false"

__Attack type settings__

_GetChunkSize_

How many GET parameters to test with one request?

_PostChunkSize_

How many POST parameters to test with one request?

__Tunneling__

Its also possible to use a tunnel, e.g. "127.0.0.1:8080" (Burp Proxy), to monitor all traffic within Burp.

_Active_

Setting this to "true" will force the script to use a tunneled connection.

_Tunnel_

Set here your proxy server "ip:port".

The result is the following one, when you open Burp you can watch your http history:

![main](https://i.imgur.com/FKGOCHq.png)

## Screenshot

![main](https://i.imgur.com/DRGzb4m.png)

![asd](https://i.imgur.com/51sVjOt.png)

## Feature requests

Please just create an issue and tag it as a feature request.

## Support

Do you like that tool? Did it help you to get a bounty? Want to give something back/support me? Why not!<br />

#### Donate via PayPal: <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=PPHDNEJWY5UXJ&source=url">CLICK</a>

