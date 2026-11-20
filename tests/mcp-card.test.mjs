import assert from 'node:assert/strict';
import test from 'node:test';
import {parseCardDate, readCardDates} from '../assets/mcp-ocr/read-card.mjs';

const min='2024-01-01', max='2024-12-31';
// Synthetic OCR output with word boxes; no patient data or real cards.
function tsv(...rows) {
  return rows.flatMap((cells,index)=>cells.flatMap(([left,text,score=95])=>{
    let x=left;
    return text.split(' ').map(word=>{
      const width=word.length*8;
      const line=[5,1,1,1,index+1,1,x,index*30,width,15,score,word].join('\t');
      x+=width+5;return line;
    });
  })).join('\n');
}
const read=rows=>readCardDates(rows,{min,max});

test('rejects ambiguous, incomplete, impossible, and out-of-range dates',()=>{
  assert.equal(parseCardDate('06/07/2024','auto',min,max),null);
  assert.equal(parseCardDate('06/07/2024','dmy',min,max),'2024-07-06');
  assert.equal(parseCardDate('06/07/2024','mdy',min,max),'2024-06-07');
  assert.equal(parseCardDate('2024-02-29','auto',min,max),'2024-02-29');
  for (const text of ['30/02/2024','01/01/25','2025-01-01','2023-12-31','28/01-2024']) {
    assert.equal(parseCardDate(text,'dmy',min,max),null);
  }
});

test('uses the given column only; leaves a row blank if its only date was due',()=>{
  const rows=tsv(
    [[10,'Vaccine name'],[210,'Due date'],[410,'Given on']],
    [[10,'BCG'],[210,'01/01/2024'],[410,'05/01/2024']],
    [[10,'OPV-0'],[210,'01/01/2024']],
    [[10,'Penta-1'],[210,'12/02/2024'],[410,'19/02/2024']],
  );
  assert.deepEqual(readCardDates(rows,{min,max,order:'dmy'}),[
    {id:'bcg',date:'2024-01-05',shared:false},
    {id:'opv0',date:null,shared:false},
    {id:'penta1',date:'2024-02-19',shared:false},
  ]);
});

test('a shared visit date is a per-dose suggestion, never a confirmed record',()=>{
  const rows=tsv(
    [[10,'Penta-1 OPV-1 fIPV-1']],
    [[10,'Date of Vaccination (mm/dd/yyyy)']],
    [[10,'02/03/2024']],
    [[10,'Next Vaccination Date: 03/20/2024']],
  );
  assert.deepEqual(read(rows),['opv1','penta1','fipv1'].map(id=>({id,date:'2024-02-03',shared:true})));
});

test('does not use upcoming appointments, missed doses, or low-confidence dates',()=>{
  assert.deepEqual(read(tsv(
    [[10,'BCG Next date of vaccination: 12/14/2024']],
    [[10,'OPV-0 Not given on 16/01/2024']],
    [[10,'Penta-1 Given on'],[170,'18/02/2024',48]],
    [[10,'IPV-1 Given on 18/02/2024']],
  )),['bcg','opv0','penta1'].map(id=>({id,date:null,shared:false})));
});

test('conflicting dates for the same dose require manual review',()=>{
  assert.deepEqual(read(tsv(
    [[10,'BCG Given on 13/01/2024']],
    [[10,'BCG Date given: 14/01/2024']],
  )),[{id:'bcg',date:null,shared:false}]);
});
