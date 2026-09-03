import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  assemble,
  combineCharacter,
  combineVowels,
  convertHangulToQwerty,
  convertQwertyToHangul,
  days,
  disassemble,
  getChoseong,
  hasBatchim,
  josa,
  numberToHangul,
  numberToHangulMixed,
  removeLastCharacter,
  romanize,
  standardizePronunciation,
  susa,
} from 'es-hangul';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const Hangul = require('hangul-js');

const HERE = path.dirname(fileURLToPath(import.meta.url));
const RESULT_PATH = path.join(HERE, 'results', 'node.json');

const TEXT = (
  '가나다라마바사아자차카타파하 한글 사랑 나라 학교 한국어 사람 대한민국 '.repeat(128)
).trim();
const JAMO_TEXT = disassemble(TEXT);
const ROMAN_TEXT = ('한글 사랑 나라 학교 한국어 대한민국 '.repeat(96)).trim();
const PRON_TEXT = ('굳이 같이 국물 신라 독립 앞문 맏형 숱하다 옷한벌 '.repeat(64)).trim();
const QWERTY_TEXT = ('dkssudgktpdy gksrmf tkfkd eogksalsrnr '.repeat(128)).trim();
const HANGUL_QWERTY_TEXT = convertQwertyToHangul(QWERTY_TEXT);
const WORDS = Array.from({ length: 64 }, () => [
  '사과',
  '하늘',
  '바다',
  '달',
  '집',
  '학교',
  '사람',
  '한국',
]).flat();
const ACRONYMS = Array.from({ length: 64 }, () => [
  'RAM',
  'API',
  'CPU',
  'GPU',
  'HTML',
  'URL',
  'JSON',
  'SQL',
]).flat();
const NUMBERS = Array.from({ length: 32 }, () => [
  0,
  1,
  2,
  9,
  10,
  11,
  20,
  21,
  99,
  100,
  101,
  1004,
  12345,
  123456780,
]).flat();
const SUSA_NUMBERS = Array.from({ length: 4 }, () => Array.from({ length: 100 }, (_, index) => index + 1)).flat();
const DAY_NUMBERS = Array.from({ length: 12 }, () => Array.from({ length: 30 }, (_, index) => index + 1)).flat();
const SEARCH_CASES = Array.from({ length: 128 }, () => [
  ['달걀', '닭'],
  ['도우미', '도움'],
  ['사과', '삭'],
  ['한글 처리 라이브러리', 'ㅎㄱ'],
]).flat();

let sink = 0;

function packageVersion(name) {
  const packagePath = path.join(HERE, 'node_modules', name, 'package.json');
  const parsed = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
  return parsed.version ?? 'unknown';
}

function consume(value) {
  if (typeof value === 'string') {
    return value.length;
  }
  if (typeof value === 'boolean') {
    return value ? 1 : 0;
  }
  if (Array.isArray(value)) {
    return value.length;
  }
  if (typeof value === 'number') {
    return value | 0;
  }
  return String(value).length;
}

function benchmark({
  feature,
  library,
  libraryVersion,
  fn,
  workUnits,
  unit,
  notes = '',
}) {
  for (let index = 0; index < 20; index += 1) {
    sink ^= consume(fn());
  }

  let loops = 1;
  while (true) {
    const start = process.hrtime.bigint();
    let localSink = 0;
    for (let index = 0; index < loops; index += 1) {
      localSink ^= consume(fn());
    }
    const elapsedNs = Number(process.hrtime.bigint() - start);
    sink ^= localSink;
    if (elapsedNs >= 30_000_000 || loops >= 1_048_576) {
      break;
    }
    loops *= 2;
  }

  const samples = [];
  for (let sample = 0; sample < 9; sample += 1) {
    const start = process.hrtime.bigint();
    let localSink = 0;
    for (let index = 0; index < loops; index += 1) {
      localSink ^= consume(fn());
    }
    const elapsedNs = Number(process.hrtime.bigint() - start);
    sink ^= localSink;
    samples.push(elapsedNs / loops / workUnits);
  }

  samples.sort((a, b) => a - b);
  const medianNs = samples[Math.floor(samples.length / 2)];

  return {
    feature,
    library,
    language: 'JavaScript',
    version: libraryVersion,
    unit,
    median_ns_per_unit: Number(medianNs.toFixed(3)),
    samples: 9,
    notes,
  };
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function main() {
  const results = [];
  const esHangulVersion = packageVersion('es-hangul');
  const hangulJsVersion = packageVersion('hangul-js');

  assert(disassemble('한글') === 'ㅎㅏㄴㄱㅡㄹ', 'es-hangul disassemble smoke test failed');
  assert(assemble(['ㅎ', 'ㅏ', 'ㄴ', 'ㄱ', 'ㅡ', 'ㄹ']) === '한글', 'es-hangul assemble smoke test failed');

  results.push(
    benchmark({
      feature: 'decompose_text',
      library: 'es-hangul',
      libraryVersion: esHangulVersion,
      fn: () => disassemble(TEXT),
      workUnits: TEXT.length,
      unit: 'char',
    }),
  );

  results.push(
    benchmark({
      feature: 'compose_text',
      library: 'es-hangul',
      libraryVersion: esHangulVersion,
      fn: () => assemble(JAMO_TEXT.split('')),
      workUnits: JAMO_TEXT.length,
      unit: 'jamo',
    }),
  );

  const composeInputs = Array.from({ length: 256 }, () => [
    ['ㅎ', 'ㅏ', 'ㄴ'],
    ['ㄱ', 'ㅡ', 'ㄹ'],
    ['ㅅ', 'ㅏ', ''],
  ]).flat();
  results.push(
    benchmark({
      feature: 'compose_character',
      library: 'es-hangul',
      libraryVersion: esHangulVersion,
      fn: () => composeInputs.map(([first, middle, last]) => combineCharacter(first, middle, last)),
      workUnits: composeInputs.length,
      unit: 'syllable',
    }),
  );

  const vowelPairs = Array.from({ length: 256 }, () => [
    ['ㅗ', 'ㅏ'],
    ['ㅗ', 'ㅐ'],
    ['ㅜ', 'ㅓ'],
    ['ㅡ', 'ㅣ'],
  ]).flat();
  results.push(
    benchmark({
      feature: 'combine_vowels',
      library: 'es-hangul',
      libraryVersion: esHangulVersion,
      fn: () => vowelPairs.map(([first, second]) => combineVowels(first, second)),
      workUnits: vowelPairs.length,
      unit: 'pair',
    }),
  );

  const editWords = Array.from({ length: 256 }, () => ['감', '값', '한글', '전화', '사과']).flat();
  results.push(
    benchmark({
      feature: 'remove_last_character',
      library: 'es-hangul',
      libraryVersion: esHangulVersion,
      fn: () => editWords.map((word) => removeLastCharacter(word)),
      workUnits: editWords.length,
      unit: 'word',
    }),
  );

  results.push(
    benchmark({
      feature: 'get_choseong',
      library: 'es-hangul',
      libraryVersion: esHangulVersion,
      fn: () => getChoseong(TEXT),
      workUnits: TEXT.length,
      unit: 'char',
    }),
  );

  assert(hasBatchim('한') === true, 'es-hangul hasBatchim true case failed');
  assert(hasBatchim('하') === false, 'es-hangul hasBatchim false case failed');
  results.push(
    benchmark({
      feature: 'has_batchim',
      library: 'es-hangul',
      libraryVersion: esHangulVersion,
      fn: () => WORDS.map((word) => hasBatchim(word)),
      workUnits: WORDS.length,
      unit: 'word',
    }),
  );

  assert(josa('하늘', '은/는') === '하늘은', 'es-hangul josa Hangul case failed');
  assert(josa('바다', '은/는') === '바다는', 'es-hangul josa Hangul case failed');
  results.push(
    benchmark({
      feature: 'josa_hangul',
      library: 'es-hangul',
      libraryVersion: esHangulVersion,
      fn: () => WORDS.map((word) => josa(word, '은/는')),
      workUnits: WORDS.length,
      unit: 'word',
    }),
  );
  results.push(
    benchmark({
      feature: 'josa_ascii_acronym',
      library: 'es-hangul',
      libraryVersion: esHangulVersion,
      fn: () => ACRONYMS.map((word) => josa(word, '은/는')),
      workUnits: ACRONYMS.length,
      unit: 'word',
    }),
  );

  assert(romanize('한글') === 'hangeul', 'es-hangul romanize smoke test failed');
  results.push(
    benchmark({
      feature: 'standardize_pronunciation',
      library: 'es-hangul',
      libraryVersion: esHangulVersion,
      fn: () => standardizePronunciation(PRON_TEXT),
      workUnits: PRON_TEXT.length,
      unit: 'char',
    }),
  );
  results.push(
    benchmark({
      feature: 'romanize',
      library: 'es-hangul',
      libraryVersion: esHangulVersion,
      fn: () => romanize(ROMAN_TEXT),
      workUnits: ROMAN_TEXT.length,
      unit: 'char',
    }),
  );

  results.push(
    benchmark({
      feature: 'number_to_hangul',
      library: 'es-hangul',
      libraryVersion: esHangulVersion,
      fn: () => NUMBERS.map((value) => numberToHangul(value)),
      workUnits: NUMBERS.length,
      unit: 'number',
    }),
  );
  results.push(
    benchmark({
      feature: 'number_to_hangul_mixed',
      library: 'es-hangul',
      libraryVersion: esHangulVersion,
      fn: () => NUMBERS.map((value) => numberToHangulMixed(value)),
      workUnits: NUMBERS.length,
      unit: 'number',
    }),
  );
  results.push(
    benchmark({
      feature: 'susa',
      library: 'es-hangul',
      libraryVersion: esHangulVersion,
      fn: () => SUSA_NUMBERS.map((value) => susa(value)),
      workUnits: SUSA_NUMBERS.length,
      unit: 'number',
    }),
  );
  results.push(
    benchmark({
      feature: 'days',
      library: 'es-hangul',
      libraryVersion: esHangulVersion,
      fn: () => DAY_NUMBERS.map((value) => days(value)),
      workUnits: DAY_NUMBERS.length,
      unit: 'number',
    }),
  );

  results.push(
    benchmark({
      feature: 'qwerty_to_hangul',
      library: 'es-hangul',
      libraryVersion: esHangulVersion,
      fn: () => convertQwertyToHangul(QWERTY_TEXT),
      workUnits: QWERTY_TEXT.length,
      unit: 'char',
    }),
  );
  results.push(
    benchmark({
      feature: 'hangul_to_qwerty',
      library: 'es-hangul',
      libraryVersion: esHangulVersion,
      fn: () => convertHangulToQwerty(HANGUL_QWERTY_TEXT),
      workUnits: HANGUL_QWERTY_TEXT.length,
      unit: 'char',
    }),
  );

  assert(Hangul.search('달걀', '닭') >= 0, 'Hangul.js search canonical case failed');
  assert(Hangul.search('도우미', '도움') >= 0, 'Hangul.js search canonical case failed');
  assert(Hangul.search('사과', '삭') >= 0, 'Hangul.js search canonical case failed');
  results.push(
    benchmark({
      feature: 'hangul_contains',
      library: 'hangul-js',
      libraryVersion: hangulJsVersion,
      fn: () => SEARCH_CASES.map(([text, query]) => Hangul.search(text, query) >= 0),
      workUnits: SEARCH_CASES.length,
      unit: 'query',
      notes: 'Hangul.search >= 0 on canonical partial-syllable cases',
    }),
  );

  fs.mkdirSync(path.dirname(RESULT_PATH), { recursive: true });
  fs.writeFileSync(
    RESULT_PATH,
    JSON.stringify(
      {
        runtime: {
          language: 'JavaScript',
          version: process.version,
          sink,
        },
        results,
      },
      null,
      2,
    ),
    'utf8',
  );

  console.log(`wrote ${results.length} JavaScript benchmark rows to ${RESULT_PATH}`);
}

main();
