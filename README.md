# Xedis
Redis-like in-memory datastructure store
* Supports lists, sets and hashmaps/dicts
* Has a client-server architecture and a repl
* Persists data in a background thread every few seconds (30 by default). Option to recover persisted data in case of errors


## Instructions
1) Start the server
```python
>>> from xedis.server import start_serving
>>> start_serving()
>>> # or start_serving(True) if an error occurred and you want to recover persisted data
INFO:xedis.server:listening on:('localhost', 6379)
```
2) Start the client
```python
>>> from xedis.client import XedisClient
>>> z=XedisClient()
>>> z.repl()
xedis> 
```
3) Run some commands on the repl. Try `help`. l - list, s - set, h - hashmap
```
xedis> help
<OK> flush
hcount name
hcreate name
help cmd
hget name *items
hkeys name
hpop name *items
hset name *items
hvalues name
info
keys
lappend name *items
lcount name
lcreate name
lget name
lrem name *items
rem name
sadd name *items
scount name
screate name
sget name
sinter *names
srem name *items
sunion *names
xedis> 
xedis> help sadd
<OK> sadd name *items
```
4) Let's load some data now
```
xedis> screate s1
<OK>
xedis> sadd s1 1 2 3
<OK>
xedis> sget s1
[1, 2, 3]
xedis> 
xedis> scount s1
3
xedis> hcreate h1
<OK>
xedis> hset h1 k1:v1 k2:v2
<OK>
xedis> hget h1 k1
[u'v1']
xedis> hkeys h1
[u'k2', u'k1']
xedis> hvalues h1
[u'v2', u'v1']
```
5) Instrospect the data
```
xedis> keys
[u's1', u'h1']
xedis> info
{u'mem_usage': 1098, u'num_items': 2}
```
5) Commands may even be chained together with a `|`
```
xedis> screate s2
<OK>
xedis> hkeys h1|hget h1|sadd s2
<OK>
xedis> sget s2
[u'v1', u'v2']
xedis> scount s2
2
xedis> screate s3
<OK>
xedis> sadd s3 1 2 3
<OK>
xedis> screate s4
<OK>
xedis> sunion s2 s3 | sadd s4
<OK>
xedis> sget s4
[u'v1', u'v2', 3, 2, 1]
```
