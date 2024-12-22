// Comp
import Loader from "../../molecules/Loading/Loading";

// Utils
import onFinishRestPage from './utils/onFinishRestPage'


const LoaderWrapper = ({loading, setShowContent}) => {
    const onFinish = onFinishRestPage(setShowContent);

    return (
        <Loader loading={loading} onFinish={onFinish}/>
    )
}

export default LoaderWrapper;