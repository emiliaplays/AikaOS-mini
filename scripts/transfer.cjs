// Project-local, loopback-only transfer between QEMU's NAT and the host.
const http = require('http');
const fs = require('fs');
const path = require('path');
const {pipeline} = require('stream');
const root = path.resolve(__dirname, '../transfer');
fs.mkdirSync(root, {recursive: true});
const server = http.createServer((req, res) => {
  const name = req.url.slice(1);
  if (!/^[a-zA-Z0-9][a-zA-Z0-9_.-]*$/.test(name)) {
    res.writeHead(400); return res.end();
  }
  const target = path.join(root, name);
  if (req.method === 'GET') {
    if (!fs.existsSync(target)) {res.writeHead(404); return res.end();}
    res.setHeader('Content-Length', fs.statSync(target).size);
    return pipeline(fs.createReadStream(target), res, () => {});
  }
  if (req.method === 'PUT') {
    if (fs.existsSync(target)) {res.writeHead(409); return res.end('Already exists');}
    return pipeline(req, fs.createWriteStream(target, {flags:'wx'}), err => {
      if (err) {res.writeHead(500); res.end(String(err));}
      else {console.log(`${name}: ${fs.statSync(target).size} bytes`); res.end('OK');}
    });
  }
  res.writeHead(405); res.end();
});
server.requestTimeout = 0;
server.listen(18087, '127.0.0.1', () => console.log('Mini transfer ready on 127.0.0.1:18087'));
