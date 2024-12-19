import prepareRecomForDispl from "./prepareRecomForDispl";

function sliceAndFill(array, size) {
    const filler = ""
    const sliced = array.slice(0, size);
    const new_sliced = sliced.map(prepareRecomForDispl).filter(item => item !== null);

    const res = Array.from(new Map(new_sliced.map(item => [item, true])).keys());


    while (res.length < size) {
        res.push(filler);
    }

    return res;
}


export default sliceAndFill;