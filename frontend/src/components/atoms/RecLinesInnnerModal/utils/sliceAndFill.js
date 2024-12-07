function sliceAndFill(array, size, filler) {
    const sliced = array.slice(0, size);

    while (sliced.length < size) {
        sliced.push(filler);
    }

    return sliced;
}


export default sliceAndFill;