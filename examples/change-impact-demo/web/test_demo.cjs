"use strict";
/* No dependencies. Executes the exact browser inline script with a tiny DOM shim. */
const fs = require("node:fs");
const vm = require("node:vm");
const assert = require("node:assert/strict");
const path = require("node:path");
const html = fs.readFileSync(path.join(__dirname, "index.html"), "utf8");
const script = html.match(/<script>([\s\S]*?)<\/script>/);
assert.ok(script, "Inline demo script must exist");
const ids = ["scenario","result","changed","version","config","evidence","test","date","required","tested","evaluate","outcome","rationale"];
const elements = Object.fromEntries(ids.map(id => [id, {value:"",textContent:"",addEventListener(){}}]));
const context = vm.createContext({document:{getElementById:id=>elements[id]},Set,Date,Number,Object,Array});
vm.runInContext(script[1],context,{filename:"demo-inline.js"});
const evalDemo = () => vm.runInContext("evaluate()",context);
const preset = name => {elements.scenario.value=name;vm.runInContext("reset()",context);return evalDemo();};
const checks = [
 ["reuse","REUSE","R6"],["fail","REVIEW","R1"],["dependency","REVERIFY","R2"],
 ["interface","REVERIFY","R3"],["missing","REVIEW","R4"],
 ["stale","REVIEW","R5"],["scope","REVERIFY","R7"]
];
for(const [name,outcome,rule] of checks){const result=preset(name);assert.equal(result.outcome,outcome,name);assert.equal(result.rule,rule,name);}
preset("reuse");elements.result.value="FAIL";elements.changed.value="yes";assert.equal(evalDemo().rule,"R1","R1 must override R2");
preset("reuse");elements.changed.value="yes";elements.version.value="IF-A";assert.equal(evalDemo().rule,"R2","R2 must override R3");
preset("reuse");elements.version.value="IF-A";elements.evidence.value="";assert.equal(evalDemo().rule,"R3","R3 must override R4");
preset("reuse");elements.evidence.value="";elements.date.value="2024-01-01";assert.equal(evalDemo().rule,"R4","R4 must override R5");
preset("reuse");elements.date.value="2024-01-01";elements.required.value="EO_CAMERA,GIMBAL";assert.equal(evalDemo().rule,"R5","R5 must override R7");
preset("reuse");elements.required.value="EO_CAMERA,GIMBAL";assert.equal(evalDemo().rule,"R7","R7 must override R6");
console.log("13 synthetic browser demo assertions passed (7 presets + 6 precedence cases).");
