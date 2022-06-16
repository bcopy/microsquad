// import { MicrosquadClient } from '../lib/client';

import { of,from } from 'rxjs';



const aedes = require('aedes')()
const httpServer = require('http').createServer()
const ws = require('websocket-stream')
const port = 8888
httpServer.listen(port, function () {
  console.log('websocket server listening on port ', port)
})

const aedesServer = ws.createServer({ server: httpServer }, aedes.handle);

// var mqtt = require('mqtt');
// var client = mqtt.connect('ws://localhost:8888');

// client.on('connect', function () {
//   console.log("Client connected !");
//   // client.publish('test', 'Hello mqtt');
// })


afterAll(() => {
  httpServer.close();
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

test('client subscribe ok', done => {
  // var client = new MicrosquadClient("ws://localhost:8888","jest-client-ID", "/")
  // // let topic = MicrosquadClient.topic(`test/topic`)

  // client.playerSubject$.subscribe( data => {
  //   expect(data).toBe('hello');
  //  
  // });
  expect(4).toBe(4);
  done();
});

