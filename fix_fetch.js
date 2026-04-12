const fs = require('fs');

const files = [
  { path: 'frontend/src/views/RulesView.vue', depth: '../' },
  { path: 'frontend/src/views/IdentifyView.vue', depth: '../' },
  { path: 'frontend/src/views/ConfigView.vue', depth: '../' },
  { path: 'frontend/src/components/radar/PhaseInit.vue', depth: '../../' },
  { path: 'frontend/src/components/radar/PhaseCalibrate.vue', depth: '../../' },
  { path: 'frontend/src/components/radar/PhaseTarget.vue', depth: '../../' }
];

files.forEach(({path, depth}) => {
  let content = fs.readFileSync(path, 'utf8');
  // Remove the old bad import if any
  content = content.replace(/import \{ getApiUrl \} from '@\/lib\/utils'\n?/, '');
  
  if (!content.includes('import { getApiUrl }')) {
    content = content.replace('<script setup>', `<script setup>\nimport { getApiUrl } from '${depth}lib/utils.js'`);
  }
  fs.writeFileSync(path, content);
});

// Add getApiUrl to utils.js
const utilsPath = 'frontend/src/lib/utils.js';
let utilsContent = fs.readFileSync(utilsPath, 'utf8');
if (!utilsContent.includes('getApiUrl')) {
  utilsContent += `\nexport function getApiUrl(path) {\n  const baseUrl = import.meta.env.VITE_API_URL || '';\n  return \`\${baseUrl}\${path}\`;\n}\n`;
  fs.writeFileSync(utilsPath, utilsContent);
}
