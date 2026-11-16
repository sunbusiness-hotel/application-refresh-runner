import io,json,unittest,urllib.error
from unittest.mock import Mock
import importlib.util
spec=importlib.util.spec_from_file_location('sync_sheet','sync-sheet.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class SyncTests(unittest.TestCase):
 def test_success_is_confirmed_and_request_contains_no_business_values(self):
  opener=Mock(return_value=io.BytesIO(b'{"ok":true,"result":{"updated":46}}'))
  module.sync('https://script.google.com/macros/s/example/exec','x'*64,'stock',opener)
  request=opener.call_args.args[0];self.assertEqual(set(json.loads(request.data)),{'action','source','token'})
 def test_unknown_completion_is_retried_once_but_never_claimed_success(self):
  for response in [b'{"ok":false}',b'{"ok":true,"result":{"updated":0}}',b'not json']:
   opener=Mock(side_effect=lambda *a,**kw:io.BytesIO(response));pause=Mock()
   with self.assertRaisesRegex(RuntimeError,'SYNC_FAILED'):module.sync('https://script.google.com/macros/s/example/exec','x'*64,'availability',opener,pause)
   self.assertEqual(opener.call_count,2);pause.assert_called_once_with(5)
 def test_invalid_source_or_endpoint_never_sends_a_secret(self):
  opener=Mock()
  for url,source in [('https://other.invalid/exec','stock'),('https://script.google.com/macros/s/example/exec','prices')]:
   with self.assertRaises(ValueError):module.sync(url,'x'*64,source,opener)
  opener.assert_not_called()
if __name__=='__main__':unittest.main()
