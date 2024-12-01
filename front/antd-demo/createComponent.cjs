const fs = require('fs');
const path = require('path');
const resolve = require('path').resolve;

const componentName = process.argv[2];

const customPath = process.env.TARGET_DIR;

if (!componentName) {
  console.error('Por favor, provee un nombre para el componente.');
  process.exit(1);
}

const currentDir = customPath ? resolve(customPath) : process.cwd();
const componentDir = path.join(currentDir, componentName);

const camelCaseName = toCamelCase(componentName);

const jsxContent = `
import React from 'react';
import './${componentName}.css';

const ${camelCaseName} = () => {
  return (
    <div>${camelCaseName}</div>
  );
};

export default ${camelCaseName};
`;

const cssContent = `.${camelCaseName} {}`;

if (!fs.existsSync(componentDir)) {
  fs.mkdirSync(componentDir, { recursive: true });
}

fs.writeFileSync(path.join(componentDir, `${componentName}.jsx`), jsxContent);
fs.writeFileSync(path.join(componentDir, `${componentName}.css`), cssContent);

console.log(`✅ Componente ${componentName} creado en ${componentDir}`);

function toCamelCase(componentName) {
  return componentName
    .split('-') 
    .map((word, index) => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ) 
    .join('');
}