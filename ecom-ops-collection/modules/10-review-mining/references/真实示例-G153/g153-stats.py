import json, sys, re, collections
sys.stdout.reconfigure(encoding='utf-8')
src, out = sys.argv[1], sys.argv[2]
d = json.load(open(src, encoding='utf-8'))
R = d['reviews']

NEG = {72,135,157,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,209,214,218,231,236,306,313,319,330,337,339,344,359,362,364,384,403,405,411,425,442}
MINOR = {18,92,103,117,148,166,182,259,284,288,328,331,393,413,419,434}
NEUTRAL = {83,129,137,142,165,174,208,237,271,275,289,303,333,340,341,346,355,388,418,452}
GENERIC = {36,42,50,61,75,90,104,112,120,126,140,145,151,154,156,160,163,164,170,178,211,215,216,221,223,225,243,254,258,265,268,270,281,294,298,299,307,312,318,321,329,349,358,376,381,387,394,397,398,401,406,414,423,424,426,427,428,429,430,431,433,435,436,437,439,440,443,444,446,450,451,66}
TOPICS = {
 '涂层粘锅、脱落、洗不净': [187,192,205,206,319,337,411],
 '做工、耐用': [191,195,197,306,362],
 '容量偏小或虚标': [72,135,199,209,231,425],
 '火力弱、慢': [157,189,202,313,330],
 '加热不均（半圈或C形）': [192,204,209,411],
 '蒸笼材质、不合': [193,384],
 '生锈': [201,344,359],
 '功能落差、不值': [190,196,198,200],
 '溢锅、跳闸、档位': [203,209,214,236,330],
 '物流、客服、售后': [194,197,339,344,403,405],
 '外观瑕疵': [188,218],
 '价保': [442],
 '无具体原因': [207,364],
}

allnums = {r['n'] for r in R}
sets = [NEG, MINOR, NEUTRAL, GENERIC]
for i in range(len(sets)):
    assert sets[i] <= allnums, 'bad number'
    for j in range(i + 1, len(sets)):
        assert not (sets[i] & sets[j]), ('overlap', sets[i] & sets[j])
cov = set()
for v in TOPICS.values():
    cov |= set(v)
assert NEG <= cov and cov <= NEG, ('topic cover', NEG - cov, cov - NEG)

def label(n):
    if n in NEG: return '差评'
    if n in MINOR: return '好评带小缺点'
    if n in NEUTRAL: return '中性或还没用'
    if n in GENERIC: return '好评无具体内容'
    return '好评有具体内容'

def sku_of(s):
    if '2.5L' in s: return '2.5L 大容量'
    if '升级钢胆' in s:
        return '钢胆+不锈钢蒸笼' if '不锈钢蒸笼' in s else '钢胆+蒸笼'
    if 'PP蒸笼' in s: return 'PP蒸笼款'
    if '不锈钢蒸笼款' in s: return '不锈钢蒸笼款'
    if '蒸笼款' in s: return '蒸笼款'
    if '基础款' in s: return '基础款'
    return '其他'

def media(r):
    if r['video']: return '有视频'
    if r['photos'] > 0: return '有图'
    return '无图'

for r in R:
    r['label'] = label(r['n'])
    r['sku2'] = sku_of(r['sku'])
    r['media'] = media(r)
    r['month'] = r['date'][:7]

def group(key):
    g = collections.OrderedDict()
    for r in R:
        k = r[key]
        x = g.setdefault(k, {'n': 0, 'neg': 0, 'minor': 0})
        x['n'] += 1
        if r['label'] == '差评': x['neg'] += 1
        if r['label'] == '好评带小缺点': x['minor'] += 1
    return g

stats = {}
stats['total'] = len(R)
stats['date_range'] = [min(r['date'] for r in R), max(r['date'] for r in R)]
stats['labels'] = dict(collections.Counter(r['label'] for r in R))
stats['neg_rate'] = round(len(NEG) / len(R) * 100, 1)
stats['media'] = group('media')
stats['sku'] = dict(sorted(group('sku2').items(), key=lambda kv: -kv[1]['n']))
stats['month'] = dict(sorted(group('month').items()))
stats['topics'] = {k: len(v) for k, v in TOPICS.items()}
app = [r for r in R if r['append']]
appneg = [r['n'] for r in app if r['label'] == '差评']
stats['append'] = {'total': len(app), 'neg': len(appneg), 'neg_numbers': appneg}
first = [r for r in R if not r['append']]
stats['no_append_neg_rate'] = [len(first), sum(1 for r in first if r['label'] == '差评')]
stats['photo_or_video'] = sum(1 for r in R if r['media'] != '无图')
stats['video'] = sum(1 for r in R if r['video'])

KW = [
 ('大小合适、1-2人', r'(大小|尺寸|容量|体积).{0,6}(合适|刚好|正好|够用|适合)|一个人|一人|1-2人|1至2人|1到2人|一两|两个人|单人|两人'),
 ('做工质量厚实', r'做工|厚实|扎实|质感|质量.{0,3}好|精致|精细|有份量'),
 ('颜值外观', r'颜值|好看|漂亮|外观|颜色|造型|款式|美观'),
 ('加热快', r'(加热|烧水|开锅|煮|烧开|水开).{0,6}快|速度快|很快|挺快'),
 ('蒸煮一锅多用', r'蒸|一锅多用|多功能|功能'),
 ('好清洗、不粘', r'清洗|好洗|洗刷|一冲|不粘|不黏|不沾|干净'),
 ('大品牌信任', r'大品牌|大牌|品牌|牌子'),
 ('没有异味', r'(没有|没什么|无).{0,3}(异味|味道|塑料味|刺鼻)|无异味|新机没有'),
 ('宿舍、办公室、租房', r'宿舍|办公室|单位|租房|上班'),
 ('物流、包装', r'物流|发货|快递|包装'),
 ('回购', r'回购|再买|第二次|第三次|买了两个|买了好几个|又买'),
 ('304、食品级不锈钢', r'304|不锈钢内胆|食品级|钢印'),
 ('安静', r'安静|不吵|噪音|声音不大|很静'),
 ('不跳闸', r'不会跳闸|不跳闸'),
]
nonneg = [r for r in R if r['label'] != '差评']
kw = {}
for name, pat in KW:
    kw[name] = sum(1 for r in nonneg if re.search(pat, (r['text'] or '') + ' ' + (r['append'] or '')))
stats['keywords_nonneg'] = kw
stats['keywords_base'] = len(nonneg)
stats['platform_tag_like'] = sum(1 for r in R if r['text'] and '。 ' in r['text'])
stats['placeholder_good'] = sum(1 for r in R if (r['text'] or '').startswith('该用户觉得商品非常好'))
stats['placeholder_empty'] = sum(1 for r in R if (r['text'] or '').startswith('该用户未填写评价内容'))

cnt = collections.defaultdict(list)
for r in R:
    t = (r['text'] or '').strip()
    if len(t) >= 8 and not t.startswith('该用户'):
        cnt[t].append(r['n'])
stats['exact_dup_groups'] = [{'text': t[:24], 'n': v} for t, v in cnt.items() if len(v) > 1]

lab = {'source': d['source'], 'fetched': d['fetched'], 'method': '逐条阅读正文（含追评）由 Agent 判断，不是平台星级；规则见 SKILL 的好评差评判断标准',
       'labels': {str(r['n']): r['label'] for r in R}, 'topics': TOPICS}
json.dump(lab, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(stats, ensure_ascii=False, indent=1))
