const PrepareDataForDispl = (recommendation) => {
    if (typeof recommendation === "string") {
        return recommendation;
    }
    const res = {}
    res.full_name = recommendation.full_name;


    if (recommendation?.region) {
        res.region = recommendation.region;
    }

    const district = recommendation?.district ?? "";
    const city = recommendation?.city ?? ""
    const street = recommendation?.street ?? ""
    let house = ""

    if (street === "" || street === "None") {
         house = ""
    }
    else {
         house = recommendation?.house ?? ""
    }

    if (house === "" && street === "" && city === "" && district === "") {
        return [null, null]
    }
    else if (house === "" && street === "" && district === "") {
        return [`г ${city}`, {...res, city: city}];
    }
    else if (house === "" && street === "") {
        return [`г. ${city} ${district}`, {...res, city: city, district: district}];
    }
    else if (house === "") {
        return [`${city}, ${street}`, {...res, city: city, street: street}];
    }
    return [`${city}, ${street}, ${house}`, {...res, city: city, street: street, house: house}];
}

export default PrepareDataForDispl