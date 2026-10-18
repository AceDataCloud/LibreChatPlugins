const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const ts = require('typescript');
const dp = require('librechat-data-provider');
const root = path.resolve(__dirname, '..');
const cache = new Map();
function upstream(name) {
  if (cache.has(name)) return cache.get(name);
  const source = fs.readFileSync(path.join(__dirname, 'upstream', name + '.ts'), 'utf8');
  const compiled = ts.transpileModule(source, {compilerOptions: {module: ts.ModuleKind.CommonJS, esModuleInterop: true}}).outputText;
  const module = {exports: {}};
  const localRequire = (id) => {
    if (id.startsWith('./')) return upstream(id.slice(2));
    if (id === '~/utils/env') return {MCP_PLUGIN_SOURCE: 'plugin'};
    return require(id);
  };
  vm.runInThisContext('(function(require,module,exports){' + compiled + '\n})', {filename: name + '.ts'})(localRequire, module, module.exports);
  cache.set(name, module.exports);
  return module.exports;
}
(async () => {
  const {validateManifest} = upstream('manifest');
  const {readMcpConfig} = upstream('mcp');
  const services = JSON.parse(fs.readFileSync(path.join(root, 'services.json')));
  for (const service of services) {
    const dir = path.join(root, 'plugins', service.slug);
    const manifest = validateManifest(JSON.parse(fs.readFileSync(path.join(dir, 'plugin.json'))));
    assert.equal(manifest.status, 'ok', JSON.stringify(manifest.diagnostics));
    assert.deepEqual(manifest.diagnostics, []);
    const config = await readMcpConfig(JSON.parse(fs.readFileSync(path.join(dir, 'mcp.json'))), {realRoot:dir,dataDirectory:path.join('/tmp/ace-librechat-validation', service.slug),declaredVersion:'1.0.0'});
    assert.deepEqual(config.diagnostics, []);
    assert.equal(config.servers.length, 1);
    dp.MCPServersSchema.parse({[config.servers[0].name]:config.servers[0].options});
    assert.equal(config.servers[0].options.url, `https://${service.host}.mcp.acedata.cloud/mcp`);
    assert.equal(config.servers[0].options.headers, undefined);
    const skill = fs.readFileSync(path.join(dir,'skills',manifest.manifest.name,'SKILL.md'),'utf8');
    assert.ok(skill.includes(service.task));
    console.log('PASS native manifest/MCP parser:', service.slug);
  }
  console.log('No network, OAuth, model or media request was made. Actual LibreChat install remains separate.');
})().catch(e => {console.error(e);process.exitCode=1;});
