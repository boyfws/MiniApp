
// Extlib
import {Subheadline} from "@telegram-apps/telegram-ui";

// Utils
import PreapareGeoJsonForDisplay from "./utils/PrepareGeoJsonForDisplay";

const RestAddressTitle = ({GeoJson}) => {
    return (
        <Subheadline>
            {PreapareGeoJsonForDisplay(GeoJson)}
        </Subheadline>
    )
}

export default RestAddressTitle;