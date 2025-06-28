const fs = require("fs");

const dir = fs.readdir("input", (err, files) => {
    if (err) console.log(err)

    files.forEach(file => {
        const data = fs.readFileSync("input/"+file, 'utf-8')
        .replace(/[^А-яё0-9.,"!#?%$():\n ]/g, '')
        .replace(/^\d+\s?\n/gm,'')
        .replace(/ +/gm,' ')
        .replace(/^\n+/gm,'\n');
        fs.writeFile(`output/${file}`, data, (err) => { if (err) console.log(err) })
    })
});

console.log("Done");