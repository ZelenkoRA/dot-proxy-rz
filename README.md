# DoT-proxy-rz

## Implementation

Handling a single TCP DNS query over `53` port and proxing it through `CloudFlare DNS over TLS server` 
over an encrypted connection. 

A proxy is started on port 53 that listens to DNS queries over `TCP`. 

Step by step flow:
1) Socket receives a DNS query
2) Wrapping a socket into an SSL context thats created with the `cert.pem` from the OS cert store
3) Wrapped socket is sent to Cloudflare `DNS over TLS`server on port  `853` 
4) Response from DoT server is relayed to the client via `socket.sendall`

## Usage

### Building Image

```
$ docker build -t {$image_tag} .
```
### Starting container
```
$ docker run -d --name {$container_name} -p 53:53 {$image_tag}
```

### Running Dig query
```
$ dig @127.0.0.1 google.com -t A +tcp

; <<>> DiG 9.10.6 <<>> @127.0.0.1 google.com -t A +tcp
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 58280
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; PAD: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 (".........................................................................................................................................................................................................................................................................................................................................................................................................................")
;; QUESTION SECTION:
;google.com.			IN	A

;; ANSWER SECTION:
google.com.		260	IN	A	216.58.215.110

;; Query time: 204 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
;; WHEN: Mon May 23 13:01:14 CEST 2022
;; MSG SIZE  rcvd: 468

```


## Security Concerns
- Client-Proxy connection is not encrypted. This expose the service to a person in the middle attack

## Improvements
- Multithreading
- HA config for DoT servers (Prepare the list of the servers that can handle requests from the proxy)
- Handling UDP requests
- Caching
- Detailed logging for SOC purposes
- Rate-limiting as a protection for DOS attacks

