const fs = require('fs');
const path = require('path');
const resolve = require('path').resolve;

const componentName = process.argv[2];

const customPath = process.env.TARGET_DIR;

if (!componentName) {
  console.error('Por favor, provee un nombre para el componente.');
  process.exit(1);
}

// Obtiene la ruta actual
const currentDir = customPath ? resolve(customPath) : process.cwd();
const componentDir = path.join(currentDir, componentName);

const camelCaseName = toCamelCase(componentName);

// Plantilla para el archivo .jsx
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

// Plantilla para el archivo css
const cssContent = `.${camelCaseName} {}`;

// Crea el directorio del componente y los archivos correspondientes
if (!fs.existsSync(componentDir)) {
  fs.mkdirSync(componentDir, { recursive: true });
}

fs.writeFileSync(path.join(componentDir, `${componentName}.jsx`), jsxContent);
fs.writeFileSync(path.join(componentDir, `${componentName}.css`), cssContent);

console.log(`✅ Componente ${componentName} creado en ${componentDir}`);

function toCamelCase(componentName) {
  return componentName
    .split('-') // Divide la cadena por los guiones
    .map((word, index) => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ) // Convierte la primera letra a mayúscula, excepto para la primera palabra
    .join(''); // Une las palabras sin espacios
}