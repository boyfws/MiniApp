import deepEqual from "./deepEqual";

const prepare_address = (address) => {
    const district = address?.district ?? "";
    const city = address?.city ?? ""
    const street = address?.street ?? ""
    const house = address?.house ?? ""
    if (district === "" && house === "" && street === "") {
        return {city: city}
    }
    else if (house === "" && street === "") {
        return {city: city, district: district}
    }
    else if (house === "") {
        return {city: city, street: street}
    }
    return {city: city, street: street, house: house}

}


const CompareAddresses = (prop1, prop2) => {
    const a = {}
    const b = {}
    if (prop1?.region && prop2?.region) {
        a["region"] = prop1.region;
        b["region"] = prop2.region;
    }
    return deepEqual(
        {...prepare_address(prop1), ...a},
        {...prepare_address(prop2), ...b}
        )


}

export default CompareAddresses;