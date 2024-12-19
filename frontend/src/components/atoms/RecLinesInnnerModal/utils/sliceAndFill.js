import prepareRecomForDispl from "./prepareRecomForDispl";

function sliceAndFill(array, size) {
    const filler = ""
    const sliced = array.slice(0, size);

    while (sliced.length < size) {
        sliced.push(filler);
    }

    return sliced.map(prepareRecomForDispl);
}


export default sliceAndFill;