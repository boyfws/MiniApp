import prepareRecomForDispl from "./prepareRecomForDispl";

function sliceAndFill(array, size) {
    const sliced = array.slice(0, size);

    const array_of_both_values = sliced.map(item => [prepareRecomForDispl(item), item]).filter(item => item[0] !== null);

    const res = [];
    const seen = new Set();

    for (const item of array_of_both_values) {
        const key = item[0]; // Используем первый элемент массива как ключ
        if (!seen.has(key)) {
            res.push(item);
            seen.add(key);
        }
    }


    while (res.length < size) {
        res.push(["", null]);
    }

    return res;
}


export default sliceAndFill;