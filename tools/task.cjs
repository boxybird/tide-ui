/* Portable npm entry point; PYTHON can select an installed interpreter. */
const {spawnSync}=require('node:child_process');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const task=process.argv[2];
if(!['build','check','package','verify-history'].includes(task))throw new Error('Unknown task');
const candidates=process.env.PYTHON?[process.env.PYTHON]:['python3','python','py'];
const python=candidates.find(command=>{const r=spawnSync(command,['--version'],{encoding:'utf8',windowsHide:true});return r.status===0&&/^Python 3\./.test(r.stdout+r.stderr);});
if(!python)throw new Error('Install Python 3.10+ or set PYTHON to its executable.');
const result=spawnSync(python,['-B',path.join(root,'tools',task+'.py'),...process.argv.slice(3)],{cwd:root,stdio:'inherit',windowsHide:true});
process.exit(result.status??1);
