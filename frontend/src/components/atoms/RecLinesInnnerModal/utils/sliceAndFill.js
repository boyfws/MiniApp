import prepareRecomForDispl from "./prepareRecomForDispl";

function sliceAndFill(array, size) {
    const filler = ""
    const sliced = array.slice(0, size);
    const new_sliced = sliced.map(prepareRecomForDispl).filter(item => item !== null);

    while (new_sliced.length < size) {
        new_sliced.push(filler);
    }

    return new_sliced;
}


export default sliceAndFill;