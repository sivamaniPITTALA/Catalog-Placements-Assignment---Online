// Import required modules
const fs = require('fs');

// Helper function to decode values based on the given base
const decodeValue = (value, base) => {
    return parseInt(value, base);
};

// Helper function to compute the constant term using Lagrange Interpolation
const computeConstantTerm = (points, degree) => {
    let constantTerm = 0;

    for (let i = 0; i < points.length; i++) {
        let [x_i, y_i] = points[i];
        let term = y_i;

        for (let j = 0; j < points.length; j++) {
            if (i !== j) {
                let [x_j] = points[j];
                term *= x_j / (x_j - x_i);
            }
        }

        constantTerm += term;
    }

    return Math.round(constantTerm);
};

// Main function to process the JSON test cases and compute the secret
const processTestCase = (filePath) => {
    // Read and parse JSON input
    const jsonData = JSON.parse(fs.readFileSync(filePath, 'utf-8'));

    const { keys, ...roots } = jsonData;
    const { n, k } = keys;
    const degree = k - 1; // m = k - 1

    // Decode roots into (x, y) points
    const points = Object.entries(roots).map(([key, { base, value }]) => {
        const x = parseInt(key);
        const y = decodeValue(value, parseInt(base));
        return [x, y];
    });

    // Select the minimum required points (k points)
    const selectedPoints = points.slice(0, k);

    // Compute the constant term using Lagrange Interpolation
    const secret = computeConstantTerm(selectedPoints, degree);

    return secret;
};

// Execute for both test cases
const testCase1Path = 'testcase1.json';
const testCase2Path = 'testcase2.json';

const secret1 = processTestCase(testCase1Path);
const secret2 = processTestCase(testCase2Path);

console.log('Secret for Test Case 1:', secret1);
console.log('Secret for Test Case 2:', secret2);
