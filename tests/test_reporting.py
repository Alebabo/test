import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import monitor as m
import reporting as r


def item(title='C24 Support Antwort fehlt',source='a',category='community'):
    return {'id':source,'title':title,'text':'','url':'https://example.org/'+source,'sourceId':source,'category':category,'brandMatches':['C24'],'observedAt':m.now().isoformat(),'baseline':False,'promptInjectionSuspected':False}


class ReportingTests(unittest.TestCase):
    def test_no_call_for_ordinary_support(self):
        with patch.object(r,'model_select') as api:
            self.assertEqual(r.assess_critical([item()],{} )[0],[])
            api.assert_not_called()

    def test_fallback_requires_corroboration(self):
        with patch.dict(os.environ,{},clear=True):
            self.assertEqual(r.assess_critical([item('C24 Betrug')],{})[0],[])
            alerts,_=r.assess_critical([item('C24 Betrug','a'),item('C24 Betrug','b')],{})
            self.assertEqual(len(alerts),2)
            self.assertEqual(r.assess_critical([item('C24 major outage resolved','s','status')],{})[0],[])

    def test_ai_index_validation_and_link_preservation(self):
        response={'content':[{'type':'text','text':json.dumps({'items':[{'index':99,'summary':'Fake','critical':True},{'index':0,'summary':'Nutzerbericht über Ausfall','critical':True}]})}]}
        stream=io.BytesIO(json.dumps(response).encode())
        with patch.dict(os.environ,{'ANTHROPIC_API_KEY':'test-only'}),patch.object(r.urllib.request,'urlopen',return_value=stream) as request:
            result,status=r.model_select([item()],{},'daily')
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['item']['url'],'https://example.org/a')
        payload=json.loads(request.call_args.args[0].data)
        self.assertEqual(payload['model'],'claude-sonnet-4-6')
        self.assertEqual(payload['max_tokens'],700)

    def test_short_report_limit_and_gap(self):
        with patch.dict(os.environ,{},clear=True):
            text,_=r.daily_short([item(source=str(n)) for n in range(10)],[{'status':'error'}],{'dailyBulletLimit':3})
        self.assertEqual(text.count('\n- '),3)
        self.assertIn('https://example.org/',text)
        self.assertIn('1 Quellen',text)

    def test_hourly_silence_and_once_daily(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'monitor-config.json').write_text(json.dumps({'brandKeywords':['C24'],'customerServiceKeywords':['Support'],'dailyReportAfterHour':0}))
            (root/'sources-config.json').write_text(json.dumps({'additionalServiceKeywords':[],'topics':{},'sources':[{'id':'a','name':'A','type':'rss','enabled':True}],'ai':{'enabled':False}}))
            rows=[{'id':'one','title':'C24 Support','text':'Antwort fehlt','url':'https://example.org/a','publishedAt':m.now().isoformat()}]
            with patch.object(m,'fetch',return_value=(rows,None)),patch.object(m,'daily_short',wraps=r.daily_short) as summarize:
                first=io.StringIO()
                with contextlib.redirect_stdout(first):m.run(SimpleNamespace(root=directory,mode='Automation',quiet=True))
                self.assertIn('Tagesbericht',first.getvalue())
                handoff=json.loads((root/'output/claude-handoff-latest.json').read_text())
                self.assertTrue(handoff['dailyReportCreated'])
                self.assertEqual(handoff['criticalCandidates'],[])
                self.assertEqual(len(handoff['dailyCandidates']),1)
                second=io.StringIO()
                with contextlib.redirect_stdout(second):m.run(SimpleNamespace(root=directory,mode='Automation',quiet=True))
                self.assertEqual(second.getvalue(),'')
                handoff=json.loads((root/'output/claude-handoff-latest.json').read_text())
                self.assertFalse(handoff['dailyReportCreated'])
                self.assertEqual(handoff['dailyCandidates'],[])
                self.assertEqual(summarize.call_count,1)
                with contextlib.redirect_stdout(io.StringIO()):m.run(SimpleNamespace(root=directory,mode='Daily',quiet=True))
                self.assertEqual(summarize.call_count,1)

if __name__=='__main__':unittest.main()
