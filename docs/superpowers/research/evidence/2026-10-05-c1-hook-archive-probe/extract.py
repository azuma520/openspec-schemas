import json, sys
for line in open(sys.argv[1], encoding="utf-8"):
    try: e=json.loads(line)
    except: continue
    t=e.get("type")
    if t=="system":
        st=e.get("subtype")
        if st=="init":
            print("INIT permissionMode=",e.get("permissionMode"),"model=",e.get("model"),"cwd=",e.get("cwd"))
        else:
            print("SYSTEM",st, json.dumps(e, ensure_ascii=False)[:300])
    elif t in("assistant","user"):
        for c in (e.get("message") or {}).get("content") or []:
            if not isinstance(c,dict): continue
            if c.get("type")=="tool_use": print("TOOL_USE", c.get("name"), json.dumps(c.get("input"),ensure_ascii=False)[:400])
            elif c.get("type")=="tool_result":
                cc=c.get("content"); 
                if isinstance(cc,list): cc=" ".join(x.get("text","") for x in cc if isinstance(x,dict))
                print("TOOL_RESULT is_error=",c.get("is_error"), str(cc)[:400].replace("\n"," / "))
            elif c.get("type")=="text" and t=="assistant": print("TEXT", c.get("text","")[:300].replace("\n"," / "))
    elif t=="result":
        print("RESULT", e.get("subtype"), "turns=",e.get("num_turns"), "denials=", json.dumps(e.get("permission_denials"),ensure_ascii=False)[:400])
