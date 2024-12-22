// Ext lib
import RestNameRestPage from './../../atoms/RestNameRestPage/RestNameRestPage'
import RestAddressTitle from "../../atoms/RestAddressTitle/RestAddressTitle";

const HeaderRestPage = ({GeoJson, name}) => {
    return (
        <div className="headerRestPage">
            <RestNameRestPage name={name} />
            <RestAddressTitle GeoJson={GeoJson} />
        </div>
    )

}

export default HeaderRestPage;