// Comp
import Loading from "../../molecules/Loading/Loading";

// Utils
import onFinishRestPage from './utils/onFinishRestPage'


const LoaderWrapper = ({loading, setShowContent}) => {
    const onFinish = onFinishRestPage(setShowContent);

    return (
        <Loading loading={loading} onFinish={onFinish}/>
    )
}

export default LoaderWrapper;