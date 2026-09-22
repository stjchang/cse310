# 1. True or false? Explain your answer with reasoning (14 points) 

##### a. A user requests a Web page that consists of an html file which contains the URLs to three images. Assume that HTTP/1.1 protocol is being used with persistent connection but no parallelization or pipelining. To render this page, the client will send one HTTP request and receive four HTTP responses.

**False**, because the client needs 4 HTTP requests and subsequently 4 HTTP responses (due to no parallelization/pipelining)

##### b. Two distinct Web objects on the same server (for example, https://www.cs.stonybrook.edu/about-us.html and https://www.cs.stonybrook.edu/admissions.html) can be requested and received over the same persistent HTTP connection.

**True**, persistent HTTP connection remains open after the first response, allowing multiple objects from the same server to be requested.
 

##### c. Before you start sending application-layer request and response, you need to set up a connection. This connection set up is primarily to ensure that the connection is secure.

**False**, while you do need a connection before application-layer request and response, the connection (such as TCP) is for reliable communication, not for security (which is handled by TLS/HTTPS)


##### d. If I want to transfer a file from my friend’s computer, I have to use a standard application layer protocol such as HTTP and cannot write my own protocol.

**False**, You can create your own application layer protocol, as long as both the sender and receiver are using the same protocol it will work (however HTTP is standardized).
 

##### e. If the Cache-Control field in the HTTP header message were removed, the HTTP protocol can no longer be used by Web applications.

 **False**, Cache control is used for caching behavior, but removing this field would not degrade the entire protocol, rather degrade caching behaviors.


##### f. You can connect to a server without using DNS first. 

**True**, You could connect directly to the IP address. DNS is used to translate domain names into IP addresses. 

##### g. The advantage of non-persistent HTTP versus persistent HTTP is that it is simple(r) to implement.

**True**, Non-persistent HTTP is stateless since it uses seperate TCP connections for each seperate TCP connection.