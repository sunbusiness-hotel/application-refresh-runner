"""Notify a private endpoint after collection; never print secrets or response data."""
import json,os,time,urllib.request,urllib.error

def sync(endpoint,token,source,opener=urllib.request.urlopen,pause=time.sleep):
    if not endpoint.startswith('https://script.google.com/macros/s/') or not endpoint.endswith('/exec'):
        raise ValueError('INVALID_ENDPOINT')
    if source not in ('stock','availability') or len(token)<43:
        raise ValueError('INVALID_CONFIGURATION')
    body=json.dumps({'action':'refresh_inventory_feed','source':source,'token':token}).encode()
    for attempt in range(2):
        try:
            request=urllib.request.Request(endpoint,data=body,headers={'Content-Type':'application/json','User-Agent':'application-refresh/1.0'})
            with opener(request,timeout=45) as response:
                result=json.load(response)
            if not result.get('ok') or not isinstance(result.get('result',{}).get('updated'),int) or result['result']['updated']<=0:
                raise RuntimeError('SYNC_NOT_VERIFIED')
            return
        except Exception:
            # Safe to retry: endpoint pulls current source and reads saved cells
            # before writing; it never accepts caller-supplied prices or counts.
            if attempt:raise RuntimeError('SYNC_FAILED') from None
            pause(5)

if __name__=='__main__':
    try:
        sync(os.environ['SHEET_SYNC_URL'],os.environ['SHEET_SYNC_TOKEN'],os.environ['SHEET_SYNC_SOURCE'])
        print('Verified sheet synchronization completed')
    except Exception:
        print('Sheet synchronization failed; inspect the private service status')
        raise SystemExit(1)
