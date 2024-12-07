// Components
import LoaderComp from "../../atoms/LoaderComp/LoaderComp";


const Loader = ({onFinish, loading}) => {
    return (
        <LoaderComp loading={loading} onFinish={onFinish}/>
    )
}

export default Loader;
