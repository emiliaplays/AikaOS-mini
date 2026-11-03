const net = require('net');
const fs = require('fs');
const path = require('path');
const port = Number(process.argv[2]);
const command = process.argv[3] || '';
const seconds = Number(process.argv[4] || 20);
const output = process.argv[5];
const chunks = [];
const socket = net.connect(port, '127.0.0.1');
socket.on('connect', () => {if(command) socket.write('\r'+command+'\r');});
socket.on('data', chunk => {
  chunks.push(chunk);
  if(output) fs.appendFileSync(path.resolve(output),chunk);
});
socket.on('error', err => {console.error(err.message); process.exitCode = 1;});
setTimeout(() => {
  socket.destroy();
  const text = Buffer.concat(chunks).toString();
  console.log(output ? text.slice(-4000) : text);
}, seconds*1000);
