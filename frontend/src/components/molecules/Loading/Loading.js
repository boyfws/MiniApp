// Css
import './Loading.css'

// Components
import LoaderComp from "../../atoms/LoaderComp/LoaderComp";


const Loader = ({onFinish, loading}) => {
    return (
        <div className="loading-wrapper">
            <LoaderComp loading={loading} onFinish={onFinish}/>
        </div>
    )
}

export default Loader;
