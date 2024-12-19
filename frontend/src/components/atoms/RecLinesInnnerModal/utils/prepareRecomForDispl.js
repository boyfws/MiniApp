const PrepareDataForDispl = (recommendation) => {
    if (typeof recommendation === "string") {
        return recommendation;
    }
    const city = recommendation.city
    const street = recommendation?.street ?? ""
    const house = recommendation?.house ?? ""
    let res = city
    if (street !== "") {
        res = res + ", " + street
    }

    if (house !== "") {
        res = res + ", " + house
    }
    return res
}

export default PrepareDataForDispl