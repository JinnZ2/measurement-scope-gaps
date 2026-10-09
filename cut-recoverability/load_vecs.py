import json, numpy as np, struct
D="/usr/local/lib/python3.13/dist-packages/en_core_web_md/en_core_web_md-3.8.0/vocab/"
M=0xc6a4a7935bd1e995; MASK=(1<<64)-1
def mm64a(data, seed=1):
    n=len(data); h=(seed ^ (n*M))&MASK
    nb=n//8
    for i in range(nb):
        k=struct.unpack_from("<Q",data,i*8)[0]
        k=(k*M)&MASK; k^=k>>47; k=(k*M)&MASK
        h^=k; h=(h*M)&MASK
    t=data[nb*8:]
    for i in range(len(t)-1,-1,-1): h^=t[i]<<(8*i)
    if t: h=(h*M)&MASK
    h^=h>>47; h=(h*M)&MASK; h^=h>>47
    return h
def _int(b,i):
    t=b[i]
    if t<0x80: return t,i+1
    f={0xcc:("<B",1),0xcd:(">H",2),0xce:(">I",4),0xcf:(">Q",8)}[t]
    return struct.unpack_from(f[0],b,i+1)[0],i+1+f[1]
def unpack_map(b):
    assert b[0]==0xdf; n=struct.unpack_from(">I",b,1)[0]; i=5; d={}
    for _ in range(n):
        k,i=_int(b,i); v,i=_int(b,i); d[k]=v
    return d
def load():
    V=np.load(D+"vectors",allow_pickle=False)
    k2r=unpack_map(open(D+"key2row","rb").read())
    return V,k2r
def vec(w,V,k2r):
    r=k2r.get(mm64a(w.encode()))
    return None if r is None else V[r]
if __name__=="__main__":
    V,k=load(); print(V.shape,len(k))
    for w in ["septic","turbine","head","the","drainfield"]: print(w, vec(w,V,k) is not None)
