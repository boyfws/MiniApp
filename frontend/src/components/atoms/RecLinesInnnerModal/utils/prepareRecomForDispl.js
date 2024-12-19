const PrepareDataForDispl = (recommendation) => {
    if (typeof recommendation === "string") {
        return recommendation;
    }
    const city = recommendation?.city ?? ""
    const street = recommendation?.street ?? ""
    const house = recommendation?.house ?? ""

    if (house === "" && street === "" && city === "") {
        return null
    }
    else if (house === "" && street === "") {
        return city
    }
    else if (house === "") {
        return `${city}, ${street}`
    }
    return `${city}, ${street}, ${house}`
}

export default PrepareDataForDispl