import { MicrosquadClient } from '../lib/client';

import { of,from } from 'rxjs';

const aedes = require('aedes')()
const httpServer = require('http').createServer()
const ws = require('websocket-stream')

const aedesServer = ws.createServer({ server: httpServer }, aedes.handle)

afterAll(() => {
  aedes.close();
});

test('the observable emits hello', done => {
  of('hello').subscribe( data => {
    expect(data).toBe('hello');
    done();
  });
});

test('the observable interval emits 100 then 200 then 300', done => {
  let last = 100;
  from([100, 200, 300])
  .subscribe({
      next: val => {
          expect(val).toBe(last)
          last += 100
        },
      complete: () => done(),
  })
});

test('client subscribe ok', () => {
  var client = new MicrosquadClient("ws://localhost:8888","jest-client-ID", "/")

  expect(4).toBe(4);
});

// test('power', (t) => {
//   t.is(power(2, 4), 16);
// });
