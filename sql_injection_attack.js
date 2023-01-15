const tf = require('@tensorflow/tfjs');
const csv = require('csv-parser');
const fs = require('fs');

const data = [];
fs.createReadStream("Modified_SQL_Dataset.csv")
    .pipe(csv())
        .on('data', (row) => {
            data.push(row);
        })

const inputs = data.map(row => row.input);
const labels = data.map(row => row.label);