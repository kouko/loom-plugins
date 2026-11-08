"""Local Obsidian render check; no vault files or network operations."""
from pathlib import Path
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent


def main():
    note = next((ROOT / "execution/B01/artifacts/docs").rglob("*.md"))
    fence = chr(96) * 3
    blocks = re.findall(fence + r"mermaid\s*\n(.*?)\n" + fence, note.read_text(), re.S)
    assert len(blocks) == 1
    samples = [
        {"id": "valid-control", "body": 'flowchart TD\nA["Start"] --> B["End"]'},
        {"id": "invalid-control", "body": "flowchart TD\nA -> B"},
        {"id": "B01-saved-block", "body": blocks[0]},
    ]
    code = """(async()=>{
      const {MarkdownRenderer,Component,apiVersion}=require('obsidian');
      const samples=PAYLOAD; const result=[]; const fence=String.fromCharCode(96).repeat(3);
      for(const sample of samples){
        const el=document.createElement('div');
        el.style.cssText='position:fixed;left:-10000px;top:0;width:1400px;';
        document.body.appendChild(el); const c=new Component();c.load();
        let thrown=null;
        try {
          await MarkdownRenderer.render(app,fence+'mermaid\\n'+sample.body+'\\n'+fence,el,'',c);
          await new Promise(r=>setTimeout(r,1600));
        } catch(e){thrown=String(e);}
        const txt=el.textContent||''; const svgCount=el.querySelectorAll('svg').length;
        const error=thrown||(/(?:syntax|parse|lexical) error|error parsing mermaid|unsupported markdown/i.test(txt)?txt.slice(0,500):null);
        result.push({id:sample.id,svgCount,error,rendered:svgCount>0&&!error});
        c.unload();el.remove();
      }
      return JSON.stringify({obsidianApiVersion:apiVersion,mermaidVersion:'not introspected',
        checks:result,vaultFilesWritten:false,visualLayoutInspected:false});
    })()""".replace("PAYLOAD", json.dumps(samples))
    out = ROOT / "render-check"
    out.mkdir(exist_ok=True)
    (out / "payload.js").write_text(code + "\n")
    run = subprocess.run(["obsidian", "eval", "code=" + code], text=True,
                         capture_output=True, timeout=40)
    (out / "result.txt").write_text(run.stdout)
    (out / "stderr.txt").write_text(run.stderr)
    assert run.returncode == 0, (run.returncode, run.stderr)
    # The deliberately invalid control emits diagnostics before the eval result.
    result_line = next(line for line in reversed(run.stdout.splitlines())
                       if line.startswith("=> "))
    result = json.loads(result_line.removeprefix("=> "))
    (out / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    assert result["checks"][0]["rendered"]
    assert result["checks"][1]["error"]
    assert result["checks"][2]["rendered"]
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
