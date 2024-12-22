// Comp
import Loader from "../../molecules/Loading/Loading";

// Utils
import onFinishRestPage from './utils/onFinishRestPage'


const LoaderWrapper = ({RestDataLoading, MenuLoading, setShowContent}) => {
    const onFinish = onFinishRestPage(setShowContent);

    const loading = RestDataLoading || MenuLoading

    return (
        <Loader loading={loading} onFinish={onFinish}/>
    )
}

export default LoaderWrapper;