// Only accept exact, dose-specific labels. Do not infer a dose from age or map
// vaccines with ambiguous formulations (for example, IPV to fractional IPV).
const doseLabels = {
  bcg: /\bbcg\b/g,
  hepb0: /\b(?:hep(?:atitis)?\s*b(?:\s*[-:]?\s*(?:0|1))?\s*\(?\s*birth dose|hep(?:atitis)?\s*b\s*[-:]?\s*0)\b/g,
  opv0: /\bopv\s*[-:]?\s*(?:0|zero dose)\b/g,
  opvb: /\bopv\s*[-:]?\s*booster\b/g,
  pcvb: /\bpcv\s*[-:]?\s*booster\b/g,
  dptb1: /\bdpt\s*(?:booster|b)\s*[-:]?\s*1\b/g,
  dptb2: /\bdpt\s*(?:booster|b)\s*[-:]?\s*2\b/g,
  td10: /\btd\s*[-:(]?\s*(?:at\s+)?10\s*(?:years?|yrs?)\b/g,
  td16: /\btd\s*[-:(]?\s*(?:at\s+)?16\s*(?:years?|yrs?)\b/g,
};
for (const [id, label, count] of [
  ['opv', 'opv', 3], ['penta', 'penta(?:valent)?', 3],
  ['rvv', 'rvv|rota(?:virus)?', 3], ['fipv', 'f\\s*ipv', 3],
  ['pcv', 'pcv', 2], ['mr', 'mr', 2], ['je', 'je', 2],
  ['vita', 'vit(?:amin)?\\s*[-.]?\\s*a', 9],
]) {
  for (let n = 1; n <= count; n++) {
    doseLabels[id+n] = new RegExp(`\\b(?:${label})\\s*[-:]?\\s*(?:dose\\s*[-:]?\\s*)?${n}\\b`, 'g');
  }
}

const givenLabel = /\b(?:(?<!due )(?<!next )(?<!scheduled )(?<!planned )date\s+(?:of\s+(?:vaccination|administration)|(?:actually\s+)?given|administered)|actual\s+(?:vaccination\s+)?date|given\s+on|administered\s+on)\b/g;
const otherDateLabel = /\b(?:next\s+(?:(?:vaccination|session|visit|dose)\s+)?date|(?:due|scheduled|planned|birth|expiry)\s+date|date\s+(?:due|scheduled|to\s+be\s+given|of\s+(?:next|birth|expiry|delivery))|missed\s+dose)\b/g;
const notGiven = /\b(?:not\s+(?:given|administered)|missed|declined|refused|cancelled|canceled)\b/;
const columnLabel = /\b(?:vaccine(?:\s+name)?|age|due|brand(?:\s+name)?|batch(?:\s+no)?|signature)\b/g;
const numericDate = /(?<![0-9a-z/.-])(?:\d{4}\s*-\s*\d{1,2}\s*-\s*\d{1,2}|\d{1,2}\s*[/.-]\s*\d{1,2}\s*[/.-]\s*\d{4})(?![0-9a-z/.-])/g;

export function parseCardDate(text, order, min, max) {
  const normalized = text.replace(/\s/g,'');
  if (!/^(?:\d{4}-\d{1,2}-\d{1,2}|\d{1,2}([./-])\d{1,2}\1\d{4})$/.test(normalized)) return null;
  const parts = normalized.split(/[./-]/);
  const [a,b,c] = parts.map(Number);
  const iso = parts[0].length === 4;
  const safeOrder = order === 'dmy' || order === 'mdy' ? order : a > 12 ? 'dmy' : b > 12 ? 'mdy' : a === b ? 'dmy' : null;
  if (!iso && !safeOrder) return null;
  const [year,month,day] = iso ? [a,b,c] : safeOrder === 'dmy' ? [c,b,a] : [c,a,b];
  if (year < 1000 || month < 1 || month > 12 || day < 1 || day > 31) return null;
  const date = new Date(Date.UTC(year,month-1,day));
  const value = date.toISOString().slice(0,10);
  return date.getUTCMonth() === month-1 && date.getUTCDate() === day && value >= min && value <= max ? value : null;
}

// Rebuild visual rows from word positions: OCR often returns different table
// columns as different text blocks. Keep word positions and confidence attached.
function visualRows(tsv) {
  const words = (tsv || '').split(/\r?\n/).map(line => {
    const [level,,,,,,x,y,w,h,score,text] = line.split('\t');
    if (level !== '5' || !text?.trim() || ![x,y,w,h,score].every(n => Number.isFinite(Number(n))) || +h <= 0 || +w <= 0) return null;
    return {x:+x,y:+y+h/2,right:+x + +w,h:+h,score:+score,text:text.trim().toLowerCase().replace(/[–—−]/g,'-')};
  }).filter(Boolean);
  if (!words.length) return [];
  const heights = words.map(w => w.h).sort((a,b)=>a-b);
  const height = heights[Math.floor(heights.length/2)];
  const rows = [];
  for (const word of words.sort((a,b)=>a.y-b.y)) {
    let row = rows[rows.length-1];
    if (!row || word.y-row.y > height*0.55) {
      row = {y:word.y,height,words:[],text:''}; rows.push(row);
    }
    row.words.push(word);
  }
  for (const row of rows) {
    row.words.sort((a,b)=>a.x-b.x);
    let previous;
    for (const word of row.words) {
      if (previous && word.x-previous.right > height*1.6) row.text += '| ';
      previous = word;
      word.start = row.text.length;
      row.text += word.text+' ';
      word.end = row.text.length-1;
    }
  }
  return rows;
}

function matches(row, pattern) {
  return [...row.text.matchAll(pattern)].map(match => {
    const start = match.index, end = start+match[0].length;
    const words = row.words.filter(w=>w.start<end && w.end>start);
    const left = words[0].x, right = words[words.length-1].right;
    return {start,end,left,right,x:(left+right)/2,score:Math.min(...words.map(w=>w.score)),text:match[0]};
  });
}

// Return draft suggestions only. A shared visit date is never evidence that
// every printed vaccine was administered; the UI requires a per-dose choice.
export function readCardDates(tsv, {min,max,order='auto'}) {
  const rows = visualRows(tsv).map(row => ({...row,
    given:matches(row,givenLabel), other:matches(row,otherDateLabel), dates:matches(row,numericDate),
    doses:Object.entries(doseLabels).flatMap(([id,pattern])=>matches(row,pattern).map(hit=>({...hit,id}))),
  }));
  const found = new Map();
  const dateFormats = new Set(rows.flatMap(r => [...r.text.matchAll(/\b(dd\s*[/.-]\s*mm|mm\s*[/.-]\s*dd)\s*[/.-]\s*yyyy\b/g)].map(m=>m[1].startsWith('dd')?'dmy':'mdy')));
  if (order === 'auto' && dateFormats.size === 1) order = [...dateFormats][0];
  const resolveDate = dates => dates.length === 1 && dates[0].score >= 75 ? parseCardDate(dates[0].text,order,min,max) : null;
  const add = (id,date,shared=false) => {
    const result = found.get(id) || {id,date:null,shared:false};
    if (date && result.date && result.date !== date) result.conflict = true;
    if (date && !result.conflict) { result.shared = result.date ? result.shared && shared : shared; result.date = date; }
    if (result.conflict) result.date = null;
    found.set(id,result);
  };
  const confidentDoses = row => row.doses.filter(d=>d.score>=75);
  const inlineDates = (row,label) => {
    const next = [...row.other,...row.given].filter(x=>x.start>=label.end).reduce((end,x)=>Math.min(end,x.start),Infinity);
    return row.dates.filter(d=>d.start>=label.end && d.end<=next);
  };
  let table = null;
  for (const row of rows) {
    const doses = confidentDoses(row);
    doses.forEach(d=>add(d.id,null));
    if (notGiven.test(row.text)) { table=null; continue; }
    if (row.given.length) {
      table = null;
      const label = row.given[0];
      if (row.given.length!==1 || label.score<75 || row.other.some(o=>o.end>label.start && o.start<label.end)) continue;
      if (row.doses.length===1 && doses.length===1 && doses[0].end<=label.start) {
        add(doses[0].id,resolveDate(inlineDates(row,label)));
      } else if (!row.doses.length && /\b(?:vaccine|dose)\b/.test(row.text.slice(0,label.start))) {
        const neighbors = [...row.other, ...matches(row,columnLabel)].filter(m=>m.end<=label.start || m.start>=label.end);
        const left = Math.max(label.left-row.height*1.6,...neighbors.filter(m=>m.right<=label.left).map(m=>(m.right+label.left)/2));
        const right = Math.min(label.right+row.height*1.6,...neighbors.filter(m=>m.left>=label.right).map(m=>(m.left+label.right)/2));
        table = {left,right,y:row.y};
      }
    } else if (table) {
      if (row.y-table.y>row.height*6 || row.other.length || row.doses.length!==1 || doses.length!==1 || doses[0].right>=table.left) { table=null; continue; }
      table.y=row.y;
      add(doses[0].id,resolveDate(row.dates.filter(d=>d.x>=table.left && d.x<=table.right)));
    }
  }
  // For a photo cropped to a single visit box, offer a date the parent can
  // choose for individual doses. Stop at any next/due date line or other box.
  const headers = rows.filter(row=>row.given.length);
  if (headers.length===1 && headers[0].given.length===1 && !rows.some(row=>row.dates.length>1)) {
    const row = headers[0], label = row.given[0];
    if (label.score>=75 && !notGiven.test(row.text) && !row.other.some(o=>o.end>label.start && o.start<label.end) && !/\b(?:vaccine|dose)\b/.test(row.text.slice(0,label.start))) {
      let hits = inlineDates(row,label);
      const next = rows[rows.indexOf(row)+1];
      if (!hits.length && !row.other.some(m=>m.start>label.start) && next && next.y-row.y<row.height*4 && !next.other.length && !next.doses.length) {
        hits = next.dates.filter(d=>d.x>=label.left-row.height && d.x<=label.right+row.height*4);
      }
      const date = resolveDate(hits);
      if (date && rows.every(r=>r===row || r===next || !r.dates.length || r.other.length)) {
        for (const r of rows.filter(r=>!notGiven.test(r.text))) for (const d of confidentDoses(r)) {
          if (!found.get(d.id)?.date) add(d.id,date,true);
        }
      }
    }
  }
  return [...found.values()].map(({id,date,shared})=>({id,date,shared}));
}

export async function scanCardImage(file, signal) {
  if (signal.aborted) throw signal.reason;
  const {default: Tesseract} = await import('./vendor/tesseract.esm.min.js');
  if (signal.aborted) throw signal.reason;
  const asset = name => new URL('./vendor/'+name,import.meta.url).href;
  let worker;
  let fail;
  const failed = new Promise((_,reject)=>{fail=reject;});
  const abort = () => fail(signal.reason);
  signal.addEventListener('abort',abort,{once:true});
  try {
    const create = Tesseract.createWorker('eng', Tesseract.OEM.LSTM_ONLY, {
      workerPath:asset('worker.min.js'),corePath:asset('tesseract-core-lstm.wasm.js'),langPath:asset(''),
      cacheMethod:'none',workerBlobURL:false,errorHandler:fail,
    }).then(async created=>{
      if (signal.aborted) { await created.terminate(); throw signal.reason; }
      return created;
    });
    worker = await Promise.race([create,failed]);
    await Promise.race([worker.setParameters({tessedit_pageseg_mode:Tesseract.PSM.SPARSE_TEXT}),failed]);
    const {data} = await Promise.race([worker.recognize(file,{}, {text:false,tsv:true}),failed]);
    return data.tsv;
  } finally {
    signal.removeEventListener('abort',abort);
    if(worker) await worker.terminate();
  }
}
