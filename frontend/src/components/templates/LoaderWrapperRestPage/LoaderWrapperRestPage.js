// Comp
import Loader from "../../molecules/Loading/Loading";

// Ext lib
import React, { useState, useEffect } from "react";

// Utils
import onFinishRestPage from './utils/onFinishRestPage'


const LoaderWrapper = ({RestDataLoading, MenuLoading, setShowContent}) => {
    const onFinish = onFinishRestPage(setShowContent);
    const [loading, setLoading] = useState(true);


    useEffect(() => {
        setLoading(RestDataLoading || MenuLoading);
    }, [RestDataLoading, MenuLoading]);


    return (
        <Loader loading={loading} onFinish={onFinish} key={2}/>
    )
}

export default LoaderWrapper;