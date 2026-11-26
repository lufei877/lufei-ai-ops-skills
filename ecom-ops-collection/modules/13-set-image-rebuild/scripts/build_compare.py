#!/usr/bin/env python3
"""套图对照页生成器：读 套图清单.json，输出离线单文件 HTML；可选把详情图合成长图。
只拼页面和长图，不判断图好不好。用法见 references/对照页脚本.md。
"""
import argparse, base64, html, io, json, os, sys
from PIL import Image

STATUS = ["通过", "带偏差接受", "未通过", "未检查"]
CLS = {"通过": "ok", "带偏差接受": "warn", "未通过": "bad", "未检查": "na"}
MARK = {"ok": "符合", "warn": "有偏差", "bad": "不符"}
PREVIEW_W = 1100  # 页面内嵌的是压缩预览，原图在 图/ 目录


def preview(path):
    im = Image.open(path)
    w, h = im.size
    rgb = im.convert("RGB")
    if w > PREVIEW_W:
        rgb = rgb.resize((PREVIEW_W, round(h * PREVIEW_W / w)))
    buf = io.BytesIO()
    rgb.save(buf, "JPEG", quality=82)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), (w, h)


def img_tag(base, rel, label):
    if not rel:
        return ""
    p = os.path.join(base, rel)
    if not os.path.isfile(p):
        return f'<figure><div class="miss">缺图：{html.escape(rel)}</div><figcaption>{label}</figcaption></figure>'
    uri, (w, h) = preview(p)
    return (f'<figure><img src="{uri}" alt="{html.escape(label)}" data-full="1">'
            f'<figcaption>{label}　{w}×{h}</figcaption></figure>')


def build(manifest_path, out):
    base = os.path.dirname(os.path.abspath(manifest_path))
    m = json.load(open(manifest_path, encoding="utf-8"))
    items = m.get("items", [])
    count = {s: 0 for s in STATUS}
    cards = []
    for it in items:
        st = it.get("status", "未检查")
        if st not in count:
            sys.exit(f"状态只能是 {STATUS}，收到：{st}（{it.get('id')}）")
        count[st] += 1
        rows = "".join(
            f'<tr><td>{html.escape(n)}</td><td class="{c}">{MARK.get(c, "")} </td></tr>' for n, c in it.get("checks", []))
        issues = "".join(f"<li>{html.escape(i)}</li>" for i in it.get("issues", []))
        prompt = it.get("prompt", "")
        cards.append(f'''<section class="card"><h2>{html.escape(it.get("id", ""))}<span class="st {CLS[st]}">{st}</span>
<small>{html.escape(it.get("category", ""))}</small></h2>
<div class="imgs">{img_tag(base, it.get("reference"), "参考图")}{img_tag(base, it.get("final"), "新图")}</div>
{f'<table>{rows}</table>' if rows else ''}{f'<ul class="iss">{issues}</ul>' if issues else ''}
{f'<details><summary>实际提示词</summary><pre>{html.escape(prompt)}</pre></details>' if prompt else ''}</section>''')
    sample = '<span class="tag">示例数据</span>' if m.get("sample") else ""
    doc = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(m.get("title", "套图对照"))}</title>
<style>
:root{{--bg:#faf8f5;--card:#fff;--ink:#222;--sub:#6b6b6b;--line:#e8e2da;--ok:#1a7f4b;--warn:#b26a00;--bad:#c0392b;--ac:#e8590c}}
@media (prefers-color-scheme:dark){{:root{{--bg:#161616;--card:#1f1f1f;--ink:#eee;--sub:#a0a0a0;--line:#333;--ok:#4cc38a;--warn:#f0a840;--bad:#ef6b5e;--ac:#ff8a4c}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 -apple-system,"PingFang SC","Microsoft YaHei",sans-serif}}
main{{max-width:1100px;margin:0 auto;padding:16px}}h1{{font-size:20px;margin:8px 0}}
.tag{{display:inline-block;padding:1px 8px;border:1px solid var(--ac);color:var(--ac);border-radius:10px;font-size:12px;margin-left:6px}}
.sum{{display:flex;gap:10px;flex-wrap:wrap;margin:12px 0 20px}}.sum div{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 14px;min-width:96px}}.sum b{{display:block;font-size:22px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin-bottom:16px}}
h2{{font-size:16px;margin:0 0 10px}}h2 small{{color:var(--sub);font-weight:400;margin-left:8px}}
.st{{margin-left:10px;font-size:13px;padding:1px 8px;border-radius:10px;border:1px solid currentColor}}
.ok{{color:var(--ok)}}.warn{{color:var(--warn)}}.bad{{color:var(--bad)}}.na{{color:var(--sub)}}
.imgs{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;align-items:start}}
figure{{margin:0}}figure img{{width:100%;height:auto;border-radius:8px;display:block;cursor:zoom-in}}figcaption{{font-size:13px;color:var(--sub);margin-top:4px}}
.miss{{border:1px dashed var(--bad);color:var(--bad);padding:20px;border-radius:8px;font-size:13px;word-break:break-all}}
table{{width:100%;border-collapse:collapse;margin-top:10px;font-size:14px}}td{{border-top:1px solid var(--line);padding:5px 4px}}td:last-child{{text-align:right;width:5em;white-space:nowrap}}
.iss{{margin:8px 0 0;padding-left:20px;color:var(--warn);font-size:14px}}
details{{margin-top:10px;color:var(--sub);font-size:13px}}pre{{white-space:pre-wrap;word-break:break-all}}
#lb{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.85);overflow:auto;z-index:9;padding:16px}}#lb img{{display:block;margin:0 auto;max-width:none}}
#lb button{{position:fixed;top:10px;right:14px;font-size:18px;padding:4px 12px}}
footer{{text-align:center;color:var(--sub);font-size:12px;padding:20px 0}}
</style></head><body><main>
<h1>{html.escape(m.get("title", "套图对照"))}{sample}</h1>
<div class="sum"><div><b class="ok">{count["通过"]}</b>通过</div><div><b class="warn">{count["带偏差接受"]}</b>带偏差接受</div>
<div><b class="bad">{count["未通过"]}</b>未通过</div><div><b>{count["未检查"]}</b>未检查</div><div><b>{len(items)}</b>共几张</div></div>
{"".join(cards)}
<footer>页面内是压缩预览，原图见「图/」目录　·　路飞的AI运营笔记</footer></main>
<div id="lb"><button>关闭</button><img alt=""></div>
<script>
const lb=document.getElementById('lb'),li=lb.querySelector('img');
document.querySelectorAll('img[data-full]').forEach(i=>i.onclick=()=>{{li.src=i.src;lb.style.display='block'}});
lb.querySelector('button').onclick=()=>lb.style.display='none';
document.addEventListener('keydown',e=>{{if(e.key==='Escape')lb.style.display='none'}});
</script></body></html>'''
    os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
    open(out, "w", encoding="utf-8").write(doc)
    print(f"已生成 {out}：{len(items)} 张；" + "，".join(f"{k}{v}" for k, v in count.items()))
    return base, items


def stitch(base, items, out):
    """把类别为“详情”的新图按清单顺序竖向合成一张长图；宽度取最宽的，其余按比例缩放，不裁切。"""
    paths = [os.path.join(base, i["final"]) for i in items
             if i.get("category") == "详情" and i.get("final") and os.path.isfile(os.path.join(base, i["final"]))]
    if not paths:
        sys.exit("没有找到类别为“详情”且文件存在的新图，不合成")
    ims = [Image.open(p).convert("RGB") for p in paths]
    W = max(i.width for i in ims)
    ims = [i if i.width == W else i.resize((W, round(i.height * W / i.width))) for i in ims]
    canvas = Image.new("RGB", (W, sum(i.height for i in ims)), "white")
    y = 0
    for i in ims:
        canvas.paste(i, (0, y)); y += i.height
    os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
    canvas.save(out)
    print(f"已合成长图 {out}：{len(ims)} 屏，{canvas.width}×{canvas.height}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("--out", default="套图对照.html")
    ap.add_argument("--stitch", help="把类别为“详情”的新图合成长图，写到这个路径")
    a = ap.parse_args()
    b, its = build(a.manifest, a.out)
    if a.stitch:
        stitch(b, its, a.stitch)
