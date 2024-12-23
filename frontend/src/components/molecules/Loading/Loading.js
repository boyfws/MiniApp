// Css
import './Loading.css'

// Components
import LoaderComp from "../../atoms/LoaderComp/LoaderComp";


const Loader = ({onFinish, loading, key}) => {
    return (
        <div className="loading-wrapper">
            <LoaderComp loading={loading} onFinish={onFinish} key={key}/>
        </div>
    )
}

export default Loader;
