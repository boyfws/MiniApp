import prepareRecomForDispl from "./prepareRecomForDispl";

function prepareArrayWithRecom(array) {

    const array_of_both_values = array.map(item => [prepareRecomForDispl(item), item]).filter(item => item[0] !== null);

    const res = [];
    const seen = new Set();

    for (const item of array_of_both_values) {
        const key = item[0]; // Используем первый элемент массива как ключ
        if (!seen.has(key)) {
            res.push(item);
            seen.add(key);
        }
    }

    return res;
}


export default prepareArrayWithRecom;