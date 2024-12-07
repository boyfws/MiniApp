// Ext lib
import { useContext } from "react";

// State
import {LoadingContext} from "../../../state_management/context/Contexts/LoadingContext";

// Handlers
import GetHandleLoadingFinish from './utils/handleLoadingFinish';

// Components
import LoaderComp from "../../atoms/LoaderComp/LoaderComp";


const Loader = ({setShowContent}) => {
    const { RestLoaded, CategoriesLoaded } = useContext(LoadingContext);
    const loading = !(RestLoaded && CategoriesLoaded);

    const onFinish = GetHandleLoadingFinish(setShowContent)
    return (
        <LoaderComp loading={loading} onFinish={onFinish}/>
    )
}

export default Loader;
